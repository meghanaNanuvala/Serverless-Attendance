# / Resources
resource "aws_cognito_user_pool" "my_user_pool" {
  name = "my_user_pool"

  username_attributes = ["email"]
  auto_verified_attributes = ["email"]
  password_policy {
    minimum_length = 6
  }

  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_subject = "Account Confirmation"
    email_message = "Your confirmation code is {####}"
  }

  schema {
    attribute_data_type      = "String"
    developer_only_attribute = false
    mutable                  = true
    name                     = "email"
    required                 = true

    string_attribute_constraints {
      min_length = 1
      max_length = 256
    }
  }
}

resource "aws_cognito_user_pool_client" "my_user_pool_client" {
  name = "my_user_pool_client"

  user_pool_id = aws_cognito_user_pool.my_user_pool.id
  generate_secret = false
  refresh_token_validity = 90
  prevent_user_existence_errors = "ENABLED"
  explicit_auth_flows         = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_CUSTOM_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]
  
}

resource "aws_cognito_identity_pool" "my_identity_pool" {
  identity_pool_name = "my_identity_pool"
  allow_unauthenticated_identities = false

  cognito_identity_providers {
    client_id               = aws_cognito_user_pool_client.my_user_pool_client.id
    provider_name           = aws_cognito_user_pool.my_user_pool.endpoint
    server_side_token_check = true
  }
}

resource "aws_cognito_identity_pool_roles_attachment" "roles_attachment" {
  identity_pool_id = aws_cognito_identity_pool.my_identity_pool.id

  roles = {
    "authenticated" = aws_iam_role.authenticated_role.arn
  }
}

resource "aws_iam_role" "authenticated_role" {
  name               = "Cognito_AuthenticatedRole"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement": [{
      "Effect"   : "Allow",
      "Principal": {
        "Federated": "cognito-identity.amazonaws.com"
      },
      "Action"   : "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "cognito-identity.amazonaws.com:aud": aws_cognito_identity_pool.my_identity_pool.id
        },
        "ForAnyValue:StringLike": {
          "cognito-identity.amazonaws.com:amr": "authenticated"
        }
      }
    }]
  })

  # Define policies for the authenticated role as necessary
}

resource "aws_iam_role_policy_attachment" "cognito_policy_attachment" {
  role       = aws_iam_role.authenticated_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonCognitoReadOnly"
}



