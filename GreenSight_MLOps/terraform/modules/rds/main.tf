resource "aws_db_instance" "mlops_db" {
  identifier        = "${var.project_name}-db"
  instance_class    = var.instance_type
  allocated_storage = 20
  engine           = "postgres"
  password         = var.password
  username         = "admin"
  
  tags = {
    Project = var.project_name
  }
}
