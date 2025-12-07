terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# SECURITY CONFIGURATION
provider "aws" {
  region  = "us-east-1"
  profile = "personal-dea-c01" # Ensuring we target the correct lab account
}