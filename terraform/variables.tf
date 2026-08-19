variable "aws_region" {
  type        = string
  default     = "us-west-1"
  description = "AWS Region for deployment"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Deployment environment"
}

variable "app_name" {
  type        = string
  default     = "cloudops-payment-api"
  description = "Name of the core service"
}