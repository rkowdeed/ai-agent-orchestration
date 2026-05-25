terraform {
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
}

# ECR repositories for images
resource "aws_ecr_repository" "backend" {
  name = "ai-agent-backend"
}

resource "aws_ecr_repository" "frontend" {
  name = "ai-agent-frontend"
}
