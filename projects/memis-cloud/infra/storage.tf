data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "application" {
  bucket        = "${var.name}-${data.aws_caller_identity.current.account_id}-us-east-1"
  force_destroy = false
}

resource "aws_s3_bucket_public_access_block" "application" {
  bucket                  = aws_s3_bucket.application.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "application" {
  bucket = aws_s3_bucket.application.id
  rule { object_ownership = "BucketOwnerEnforced" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "application" {
  bucket = aws_s3_bucket.application.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}

resource "aws_s3_bucket_versioning" "application" {
  bucket = aws_s3_bucket.application.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_policy" "tls" {
  bucket = aws_s3_bucket.application.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "DenyInsecureTransport"
      Effect    = "Deny"
      Principal = "*"
      Action    = "s3:*"
      Resource  = [aws_s3_bucket.application.arn, "${aws_s3_bucket.application.arn}/*"]
      Condition = { Bool = { "aws:SecureTransport" = "false" } }
    }]
  })
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [for table in aws_route_table.private : table.id]
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = "*"
      Action    = ["s3:ListBucket", "s3:GetObject", "s3:PutObject"]
      Resource  = [aws_s3_bucket.application.arn, "${aws_s3_bucket.application.arn}/application/*"]
      }, {
      Sid       = "ReadAmazonLinuxRepository"
      Effect    = "Allow"
      Principal = "*"
      Action    = ["s3:GetObject"]
      Resource  = "arn:aws:s3:::al2023-repos-us-east-1-de612dc2/*"
    }]
  })
}
