# Every run uses mocks: no AWS account, credentials, or resource provisioning.
mock_provider "aws" {
  mock_data "aws_availability_zones" {
    defaults = { names = ["us-east-1a", "us-east-1b", "us-east-1c"] }
  }
  mock_data "aws_caller_identity" {
    defaults = { account_id = "123456789012" }
  }
  mock_data "aws_ssm_parameter" {
    defaults = { value = "ami-0123456789abcdef0" }
  }
  mock_data "aws_security_group" {
    defaults = { id = "sg-0123456789abcdef0" }
  }
  mock_data "aws_cloudfront_cache_policy" {
    defaults = { id = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad" }
  }
  mock_data "aws_cloudfront_origin_request_policy" {
    defaults = { id = "216adef6-5c7f-47e4-b989-5492eafa07d3" }
  }
  mock_resource "aws_acm_certificate" {
    defaults = {
      arn = "arn:aws:acm:us-east-1:123456789012:certificate/00000000-0000-0000-0000-000000000000"
      domain_validation_options = [{
        domain_name           = "memis.cloud"
        resource_record_name  = "_example.memis.cloud"
        resource_record_type  = "CNAME"
        resource_record_value = "_example.acm-validations.aws."
      }]
    }
  }
  mock_resource "aws_acm_certificate_validation" {
    defaults = { certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/00000000-0000-0000-0000-000000000000" }
  }
  mock_resource "aws_lb" {
    defaults = {
      arn      = "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/memis-cloud/0000000000000000"
      dns_name = "internal-example.us-east-1.elb.amazonaws.com"
    }
  }
  mock_resource "aws_lb_target_group" {
    defaults = { arn = "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/nginx/0000000000000000" }
  }
  mock_resource "aws_s3_bucket" {
    defaults = { arn = "arn:aws:s3:::memis-cloud-123456789012-us-east-1" }
  }
  mock_resource "aws_db_instance" {
    defaults = {
      master_user_secret = [{
        secret_arn    = "arn:aws:secretsmanager:us-east-1:123456789012:secret:rds-admin-example"
        kms_key_id    = "00000000-0000-0000-0000-000000000000"
        secret_status = "active"
      }]
    }
  }
}

variables {
  hosted_zone_id = "Z0000000000000"
}

run "network_and_private_placement" {
  command = apply
  assert {
    condition     = length(aws_subnet.public) == 3 && length(aws_subnet.private) == 3
    error_message = "The baseline must have exactly three public and three private subnets."
  }
  assert {
    condition     = alltrue([for key, route in aws_route.private_default : route.nat_gateway_id == aws_nat_gateway.zonal[key].id && route.route_table_id == aws_route_table.private[key].id])
    error_message = "Each private subnet's default must use its zonal NAT."
  }
  assert {
    condition     = aws_route.public_default.gateway_id == aws_internet_gateway.main.id && alltrue([for key, nat in aws_nat_gateway.zonal : nat.subnet_id == aws_subnet.public[key].id])
    error_message = "Public routes must reach the IGW and NATs must occupy public subnets."
  }
  assert {
    condition     = aws_instance.nginx.associate_public_ip_address == false && aws_instance.nginx.subnet_id == aws_subnet.private["a"].id
    error_message = "Nginx must be private in subnet A."
  }
  assert {
    condition     = aws_instance.nginx.metadata_options[0].http_tokens == "required" && aws_instance.nginx.root_block_device[0].encrypted
    error_message = "The instance needs IMDSv2 and encrypted root storage."
  }
}

run "private_origin_and_tls" {
  command = apply
  assert {
    condition     = aws_lb.application.internal && length(aws_lb.application.subnets) == 3
    error_message = "The ALB must be internal across three private subnets."
  }
  assert {
    condition     = aws_cloudfront_vpc_origin.application.vpc_origin_endpoint_config[0].origin_protocol_policy == "https-only" && aws_lb_listener.https.port == 443
    error_message = "CloudFront must use HTTPS to the origin's HTTPS listener."
  }
  assert {
    condition     = one(aws_cloudfront_distribution.application.origin).vpc_origin_config[0].vpc_origin_id == aws_cloudfront_vpc_origin.application.id && aws_cloudfront_distribution.application.default_cache_behavior[0].origin_request_policy_id == data.aws_cloudfront_origin_request_policy.all_viewer.id
    error_message = "The distribution must select the VPC origin and preserve viewer Host for certificate matching."
  }
  assert {
    condition     = aws_vpc_security_group_ingress_rule.alb_from_cloudfront.referenced_security_group_id == data.aws_security_group.cloudfront_service.id && aws_vpc_security_group_ingress_rule.application_from_alb.referenced_security_group_id == aws_security_group.alb.id
    error_message = "Origin and application ingress must be restricted by security-group identity."
  }
  assert {
    condition     = length(aws_route53_record.application) == 0
    error_message = "Default configuration must leave apex DNS cutover explicit."
  }
}

run "database_and_storage_boundaries" {
  command = apply
  assert {
    condition     = toset(aws_db_subnet_group.application.subnet_ids) == toset([aws_subnet.private["b"].id, aws_subnet.private["c"].id]) && !contains(aws_db_subnet_group.application.subnet_ids, aws_subnet.private["a"].id)
    error_message = "Database subnet group must use B/C and exclude Nginx subnet A."
  }
  assert {
    condition     = !aws_db_instance.application.publicly_accessible && aws_db_instance.application.storage_encrypted && aws_db_instance.application.multi_az && aws_db_instance.application.manage_master_user_password
    error_message = "RDS must be private, encrypted, Multi-AZ and manage its administrator password."
  }
  assert {
    condition     = aws_vpc_security_group_ingress_rule.database_from_application.from_port == 5432 && aws_vpc_security_group_ingress_rule.database_from_application.referenced_security_group_id == aws_security_group.application.id
    error_message = "Database access must be limited to the application security group."
  }
  assert {
    condition     = aws_s3_bucket_public_access_block.application.block_public_policy && aws_s3_bucket_public_access_block.application.restrict_public_buckets && aws_s3_bucket_versioning.application.versioning_configuration[0].status == "Enabled"
    error_message = "Application storage must block public access and retain versions."
  }
  assert {
    condition     = length(aws_iam_role_policy.application_secret) == 0 && jsondecode(aws_iam_role_policy.deny_administrator_secret.policy).Statement[0].Effect == "Deny" && jsondecode(aws_iam_role_policy.deny_administrator_secret.policy).Statement[0].Resource == aws_db_instance.application.master_user_secret[0].secret_arn
    error_message = "The default instance role must not retrieve the administrator secret."
  }
  assert {
    condition     = toset(jsondecode(aws_iam_role_policy.storage.policy).Statement[1].Action) == toset(["s3:GetObject", "s3:PutObject"]) && endswith(jsondecode(aws_iam_role_policy.storage.policy).Statement[1].Resource, "/application/*")
    error_message = "Storage permission must be read/write only within application/."
  }
  assert {
    condition     = length(aws_vpc_endpoint.s3.route_table_ids) == 3 && jsondecode(aws_vpc_endpoint.s3.policy).Statement[1].Resource == "arn:aws:s3:::al2023-repos-us-east-1-de612dc2/*" && toset(jsondecode(aws_vpc_endpoint.s3.policy).Statement[1].Action) == toset(["s3:GetObject"])
    error_message = "The endpoint must serve private routes and retain read-only AL2023 repository access for bootstrap."
  }
}

run "explicit_dns_cutover" {
  command = apply
  variables { publish_dns = true }
  assert {
    condition     = toset(keys(aws_route53_record.application)) == toset(["A", "AAAA"])
    error_message = "An explicit cutover must publish both CloudFront aliases."
  }
}

run "scoped_application_secret" {
  command = apply
  variables {
    application_secret_arn         = "arn:aws:secretsmanager:us-east-1:123456789012:secret:application-example"
    application_secret_kms_key_arn = "arn:aws:kms:us-east-1:123456789012:key/00000000-0000-0000-0000-000000000000"
  }
  assert {
    condition     = length(aws_iam_role_policy.application_secret) == 1 && jsondecode(aws_iam_role_policy.application_secret[0].policy).Statement[0].Resource == var.application_secret_arn
    error_message = "Optional secret access must be limited to the configured application secret."
  }
  assert {
    condition     = jsondecode(aws_iam_role_policy.application_secret_key[0].policy).Statement[0].Resource == var.application_secret_kms_key_arn && jsondecode(aws_iam_role_policy.application_secret_key[0].policy).Statement[0].Condition.StringEquals["kms:ViaService"] == "secretsmanager.us-east-1.amazonaws.com"
    error_message = "Optional key access must be restricted to its key and Secrets Manager use."
  }
}

run "reject_duplicate_zones" {
  command = plan
  variables {
    availability_zones = { a = "us-east-1a", b = "us-east-1a", c = "us-east-1c" }
  }
  expect_failures = [var.availability_zones]
}

run "reject_invalid_name" {
  command = plan
  variables { name = "INVALID_NAME" }
  expect_failures = [var.name]
}

run "reject_unavailable_zone" {
  command = plan
  variables {
    availability_zones = { a = "us-east-1a", b = "us-east-1b", c = "us-east-1z" }
  }
  expect_failures = [aws_vpc.main]
}
