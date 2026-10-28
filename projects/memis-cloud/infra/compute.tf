data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64"
}

resource "aws_iam_role" "application" {
  name = "${var.name}-instance"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.application.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy" "storage" {
  name = "application-storage"
  role = aws_iam_role.application.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Action    = ["s3:ListBucket"]
        Resource  = aws_s3_bucket.application.arn
        Condition = { StringLike = { "s3:prefix" = ["application/", "application/*"] } }
      },
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = "${aws_s3_bucket.application.arn}/application/*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "application_secret" {
  count = var.application_secret_arn == null ? 0 : 1
  name  = "application-secret"
  role  = aws_iam_role.application.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["secretsmanager:GetSecretValue"]
      Resource = var.application_secret_arn
    }]
  })
}

resource "aws_iam_role_policy" "application_secret_key" {
  count = var.application_secret_kms_key_arn == null ? 0 : 1
  name  = "application-secret-key"
  role  = aws_iam_role.application.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["kms:Decrypt"]
      Resource  = var.application_secret_kms_key_arn
      Condition = { StringEquals = { "kms:ViaService" = "secretsmanager.us-east-1.amazonaws.com" } }
    }]
  })
}

resource "aws_iam_instance_profile" "application" {
  name = "${var.name}-instance"
  role = aws_iam_role.application.name
}

resource "aws_iam_role_policy" "deny_administrator_secret" {
  name = "deny-database-administrator-secret"
  role = aws_iam_role.application.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Deny"
      Action   = ["secretsmanager:GetSecretValue"]
      Resource = aws_db_instance.application.master_user_secret[0].secret_arn
    }]
  })
}

resource "aws_instance" "nginx" {
  ami                         = nonsensitive(data.aws_ssm_parameter.al2023.value)
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.private["a"].id
  associate_public_ip_address = false
  vpc_security_group_ids      = [aws_security_group.application.id]
  iam_instance_profile        = aws_iam_instance_profile.application.name
  user_data                   = templatefile("${path.module}/user-data.sh.tftpl", { domain_name = var.domain_name })
  user_data_replace_on_change = true
  monitoring                  = true
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  root_block_device {
    encrypted   = true
    volume_type = "gp3"
    volume_size = 20
  }
  tags = { Name = "${var.name}-nginx" }
  # Boot only after the outbound route and role attachment are usable.
  depends_on = [aws_route.private_default, aws_route_table_association.private, aws_iam_role_policy_attachment.ssm, aws_iam_role_policy.storage, aws_iam_role_policy.deny_administrator_secret, aws_vpc_endpoint.s3]
}
