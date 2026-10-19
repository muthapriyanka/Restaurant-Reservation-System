locals {
  app_assets = {
    "customer-dining.jpeg"    = "${path.module}/assets/customer-dining.jpeg"
    "dining-room.jpeg"        = "${path.module}/assets/dining-room.jpeg"
    "login-dining.jpeg"       = "${path.module}/assets/login-dining.jpeg"
    "menu-table.jpeg"         = "${path.module}/assets/menu-table.jpeg"
    "register-dining.jpeg"    = "${path.module}/assets/register-dining.jpeg"
    "restaurant-details.jpeg" = "${path.module}/assets/restaurant-details.jpeg"
    "restaurant-table.jpeg"   = "${path.module}/assets/restaurant-table.jpeg"
  }
}

resource "aws_s3_bucket" "images" {
  bucket = "${var.project_name}-images-${data.aws_caller_identity.current.account_id}-${var.aws_region}"
}

resource "aws_s3_bucket_public_access_block" "images" {
  bucket                  = aws_s3_bucket.images.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "images" {
  bucket = aws_s3_bucket.images.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "images" {
  bucket = aws_s3_bucket.images.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "images" {
  bucket = aws_s3_bucket.images.id

  rule {
    id     = "abort-incomplete-uploads"
    status = "Enabled"
    filter {}

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

resource "aws_s3_object" "app_assets" {
  for_each     = local.app_assets
  bucket       = aws_s3_bucket.images.id
  key          = "app-assets/${each.key}"
  source       = each.value
  content_type = "image/jpeg"
  etag         = filemd5(each.value)
}

resource "aws_secretsmanager_secret" "app" {
  name        = "${var.project_name}/app"
  description = "JSON containing the shared JWT SECRET_KEY"
}
