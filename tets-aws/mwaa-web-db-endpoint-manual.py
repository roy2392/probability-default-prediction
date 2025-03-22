# This Python file uses the following encoding: utf-8
'''
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from __future__ import print_function
import boto3
import argparse
import sys
import json

ENV_NAME = ""
REGION = ""

def get_environment_and_network_details(input_env_name, ec2_client):
    '''method to get environment, print that information to stdout, and prompt the use to send it to support'''
    # get mwaa environment
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.get_environment
    mwaa = boto3.client('mwaa', region_name=REGION)
    environment = mwaa.get_environment(Name=input_env_name)['Environment']
    network_subnet_ids = environment['NetworkConfiguration']['SubnetIds']
    securityGroupIds = environment['NetworkConfiguration']['SecurityGroupIds']
    webserverAccessMode = environment['WebserverAccessMode']
    network_subnets = ec2_client.describe_subnets(SubnetIds=network_subnet_ids)['Subnets']
    return environment, network_subnet_ids , network_subnets[0]['VpcId'], securityGroupIds, webserverAccessMode

if __name__ == '__main__':
    if sys.version_info[0] < 3:
        print("python2 detected, please use python3. Will try to run anyway")
    parser = argparse.ArgumentParser()
    parser.add_argument('--envname', required=True, help="name of the MWAA environment")
    parser.add_argument('--region', default=boto3.session.Session().region_name,required=False, help="region, Ex: us-east-1")
    parser.add_argument('--profile', default='default',required=False, help="AWS CLI profile, Ex: dev")
    parser.add_argument('--WebserverVPCendpointservice',required=True, help="Please check the network details section in AWS MWAA console for Webserver VPC endpoint service and include arn here")
    parser.add_argument('--DatabaseVPCendpointservice',required=True, help="Please check the network details section in AWS MWAA console for Database VPC endpoint service and include arn here")
    parser.add_argument('--CeleryexecutorqueueARN',required=True, help="Please check the network details section in AWS MWAA console for Celery executor queue and include arn here")
    args, _ = parser.parse_known_args()
    ENV_NAME = args.envname
    REGION = args.region
    PROFILE = args.profile
    try :
        boto3.setup_default_session(profile_name=PROFILE)
        ec2 = boto3.client('ec2', region_name=REGION)
        env, subnetIds, vpcId, securityGroupIds, webserverAccessMode = get_environment_and_network_details(ENV_NAME, ec2)
        name=ENV_NAME
        celeryExecutorQueue=args.CeleryexecutorqueueARN
        databaseVpcEndpointService=args.DatabaseVPCendpointservice
        webserverVpcEndpointService=None
        if webserverAccessMode=="PRIVATE_ONLY":   
            webserverVpcEndpointService=args.WebserverVPCendpointservice
        response = ec2.describe_vpc_endpoints(
            VpcEndpointIds=[],
            Filters=[
                {"Name": "vpc-id", "Values": [vpcId]},
                {"Name": "service-name", "Values": ["*.sqs"]},
                ],
            MaxResults=1000
        )
        sqsVpcEndpoint=None
        for r in response['VpcEndpoints']:
            if subnetIds[0] in r['SubnetIds'] or subnetIds[1] in r['SubnetIds']:
                # We are filtering describe by service name, so this must be SQS
                sqsVpcEndpoint=r
                break

        if sqsVpcEndpoint:
            print("Found SQS endpoint: " + sqsVpcEndpoint['VpcEndpointId'])
            #print(sqsVpcEndpoint)
            pd = json.loads(sqsVpcEndpoint['PolicyDocument'])
            for s in pd['Statement']:
                if s['Effect']=='Allow':
                    resource = s['Resource']
                    #print(resource)
                    if '*' in resource:
                        print("'*' already allowed")
                    elif celeryExecutorQueue in resource: 
                        print("'"+celeryExecutorQueue+"' already allowed")                
                    else:
                        s['Resource'].append(celeryExecutorQueue)
                        print("Updating SQS policy to " + str(pd))

                        ec2.modify_vpc_endpoint(
                            VpcEndpointId=sqsVpcEndpoint['VpcEndpointId'],
                            PolicyDocument=json.dumps(pd)
                            )
                    break
                
        # create MWAA database endpoint if not exist
        print("creating endpoint to " + databaseVpcEndpointService)
        responsedb = ec2.describe_vpc_endpoints(
            VpcEndpointIds=[],
            Filters=[
                {"Name": "vpc-id", "Values": [vpcId]},
                {"Name": "service-name", "Values": [databaseVpcEndpointService]},
                ],
            MaxResults=1000
        )
        if len(responsedb['VpcEndpoints']) >  0:
            print(databaseVpcEndpointService+" already exist...skipping")
        else:        
            endpointName=name+"-database"
            response = ec2.create_vpc_endpoint(
                VpcEndpointType='Interface',
                VpcId=vpcId,
                ServiceName=databaseVpcEndpointService,
                SubnetIds=subnetIds,
                SecurityGroupIds=securityGroupIds,
                TagSpecifications=[
                    {
                        "ResourceType": "vpc-endpoint",
                        "Tags": [
                            {
                                "Key": "Name",
                                "Value": endpointName
                            },
                        ]
                    },
                ],           
            )
            print("created VPCE: " + response['VpcEndpoint']['VpcEndpointId'])


        # create MWAA web server endpoint (if private webserver mode and not exist)
        if webserverVpcEndpointService:
            print("creating endpoint to " + webserverVpcEndpointService)
            responseweb = ec2.describe_vpc_endpoints(
                VpcEndpointIds=[],
                Filters=[
                    {"Name": "vpc-id", "Values": [vpcId]},
                    {"Name": "service-name", "Values": [webserverVpcEndpointService]},
                    ],
                MaxResults=1000
            )
            if len(responseweb['VpcEndpoints']) >  0:
                print(webserverVpcEndpointService+" already exist...skipping")
            else:
                endpointName=name+"-webserver"
                response = ec2.create_vpc_endpoint(
                    VpcEndpointType='Interface',
                    VpcId=vpcId,
                    ServiceName=webserverVpcEndpointService,
                    SubnetIds=subnetIds,
                    SecurityGroupIds=securityGroupIds,
                    TagSpecifications=[
                        {
                            "ResourceType": "vpc-endpoint",
                            "Tags": [
                                {
                                    "Key": "Name",
                                    "Value": endpointName
                                },
                            ]
                        },
                    ],                  
                )
                print("created VPCE: " + response['VpcEndpoint']['VpcEndpointId'])
    except Exception as e:
        print(e)