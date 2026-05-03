resource "aws_ecr_repository" "main" {
  name                 = "log-analyse-script"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}
