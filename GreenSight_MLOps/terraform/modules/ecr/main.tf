resource "aws_ecr_repository" "tree_detection" {
  name = var.repository_name
  image_scanning_configuration {
    scan_on_push = true
  }
  tags = {
    Project = var.project_name
  }
}
