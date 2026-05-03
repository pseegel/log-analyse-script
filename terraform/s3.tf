resource "aws_s3_bucket" "logs" {
  bucket = "log-analyse-paul-tf"
  force_destroy = true
}
