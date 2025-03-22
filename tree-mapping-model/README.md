# GreenSight Mapping Solutions MLOps

## Objective:
Develop a full MLOps pipeline for tree detection using the Detectree model, encompassing data ingestion, preprocessing, model serving, post-processing, data storage, BI integration, monitoring, and validation.

## 1. Project Structure:
```
.
green_sight_mlops/
├── data/
│   ├── raw/
│   ├── processed/
│   └── validation/
├── models/
│   └── tree_model_new.pkl
├── src/
│   ├── preprocessing/
│   │   └── preprocess.py
│   ├── model_serving/
│   │   ├── Dockerfile
│   │   └── serve.py
│   ├── postprocessing/
│   │   └── postprocess.py
│   └── validation/
│       └── validate.py
├── notebooks/
│   └── Run_model.ipynb
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── scripts/
│       ├── preprocess_lambda.py
│       ├── postprocess_lambda.py
│       └── ...
├── .github/
│   └── workflows/
│       └── ci_cd.yml
├── requirements.txt
├── README.md
└── setup.sh
```
## 2. Infrastructure as Code with Terraform:
Using Terraform to provision AWS resources ensures consistency and scalability. Below are the Terraform configurations required for the architecture.