variable "aws_region" {
  type        = string
  description = "AWS region for the deployment."
  default     = "us-east-2"
}

variable "project_name" {
  type        = string
  description = "Prefix used for AWS resources."
  default     = "restaurant-reservation"
}

variable "image_tag" {
  type        = string
  description = "Immutable backend and frontend ECR image tag."
  default     = "bootstrap"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type used by the application Auto Scaling Group."
  default     = "t3.micro"
}

variable "min_size" {
  type    = number
  default = 1
}

variable "desired_capacity" {
  type    = number
  default = 1
}

variable "max_size" {
  type    = number
  default = 3
}
