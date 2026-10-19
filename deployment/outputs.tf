output "application_url" {
  value = "http://${aws_lb.app.dns_name}"
}

output "backend_ecr_repository" {
  value = aws_ecr_repository.backend.repository_url
}

output "frontend_ecr_repository" {
  value = aws_ecr_repository.frontend.repository_url
}

output "image_bucket" {
  value = aws_s3_bucket.images.id
}

output "application_secret" {
  value = aws_secretsmanager_secret.app.name
}

output "database_endpoint" {
  value = aws_db_instance.app.endpoint
}
