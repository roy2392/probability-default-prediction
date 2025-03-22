resource "aws_cloudwatch_log_group" "pipeline_logs" {
  name              = var.log_group
  retention_in_days = 30

  tags = {
    Project = var.project_name
  }
}
