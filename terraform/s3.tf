
provider "aws" {
  region = "us-east-1"
}

#Creating s3 bucket to upload the student image in a s3 bucket.
resource "aws_s3_bucket" "new-student-registration-tf" {
  bucket = "new-student-registration-tf"
  force_destroy = true

  tags = {
    Name        = "new-student-registration-tf"
    Environment = "Dev"
  }
}

#Creating bucket for student attendace authentication
resource "aws_s3_bucket" "class-images-tf" {
  bucket = "class-images-tf"
   force_destroy = true

  tags = {
    Name        = "class-images-tf"
    Environment = "Dev"
  }
}



