resource "aws_instance" "jupyter_notebook" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  tags = {
    Name    = "${var.project_name}-jupyter"
    Project = var.project_name
  }
}
