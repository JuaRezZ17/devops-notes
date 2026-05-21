variable "instance_type" {
  description = "The type of EC2 instance to deploy"
  type        = string
  default     = "t2.micro"
}

variable "environment" {
  description = "The environment for the deployment (e.g., dev, prod)"
  type        = string
}