resource "aws_ses_email_identity" "email_identity" {
  email = local.email_id
}

data "local_file" "ses_email" {
  filename = "${path.module}/../SES_EMAIL.txt"
}

locals {
  email_line = data.local_file.ses_email.content
  email_id   = trim(split("=", local.email_line)[1], " ")
}

output "email_id" {
  value = local.email_id
}
