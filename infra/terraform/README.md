Terraform for AWS: creates ECR repositories for backend and frontend images.

Usage:

```bash
cd infra/terraform
terraform init
terraform apply -var 'aws_region=us-east-1'
```

Make sure AWS credentials are configured (`AWS_PROFILE` or env vars).
