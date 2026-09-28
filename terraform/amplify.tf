resource "aws_amplify_app" "my_app" {
  name       = "serverless-attendance"
  repository = ""
  access_token =

  //Configure the branch that Amplify will use
  build_spec = <<-EOT
      version: 1
      frontend:
        phases:
          preBuild:
            commands:
                - cd frontend
                - npm install
          build:
            commands:
                - echo "REACT_APP_API_ENDPOINT= ${aws_api_gateway_deployment.deployment.invoke_url}" >> .env.production
                - echo "REACT_APP_aws_cognito_identity_pool_id=${aws_cognito_identity_pool.my_identity_pool.id}" >> .env.production
                - echo "REACT_APP_aws_user_pools_id=${aws_cognito_user_pool.my_user_pool.id}" >> .env.production
                - echo "REACT_APP_aws_user_pools_web_client_id=${aws_cognito_user_pool_client.my_user_pool_client.id}" >> .env.production
                - npm run build
        artifacts:
            baseDirectory: frontend/build   
            files:
            - '**/*'
        cache:
          paths: 
            - node_modules/**/*
    EOT 
  depends_on = [ aws_api_gateway_deployment.deployment, aws_cognito_identity_pool.my_identity_pool, aws_cognito_user_pool.my_user_pool, aws_cognito_user_pool_client.my_user_pool_client ]  
}

resource "aws_amplify_branch" "amplify_branch" {
  app_id      = aws_amplify_app.my_app.id
  branch_name = "main"
}

