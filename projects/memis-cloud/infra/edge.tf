resource "aws_acm_certificate" "application" {
  domain_name       = var.domain_name
  validation_method = "DNS"
  lifecycle { create_before_destroy = true }
}

resource "aws_route53_record" "certificate_validation" {
  zone_id = var.hosted_zone_id
  name    = one(aws_acm_certificate.application.domain_validation_options).resource_record_name
  type    = one(aws_acm_certificate.application.domain_validation_options).resource_record_type
  ttl     = 60
  records = [one(aws_acm_certificate.application.domain_validation_options).resource_record_value]
}

resource "aws_acm_certificate_validation" "application" {
  certificate_arn         = aws_acm_certificate.application.arn
  validation_record_fqdns = [aws_route53_record.certificate_validation.fqdn]
}

resource "aws_lb" "application" {
  name                       = "${var.name}-alb"
  internal                   = true
  load_balancer_type         = "application"
  ip_address_type            = "ipv4"
  subnets                    = [for subnet in aws_subnet.private : subnet.id]
  security_groups            = [aws_security_group.alb.id]
  drop_invalid_header_fields = true
  enable_deletion_protection = true
}

resource "aws_lb_target_group" "nginx" {
  name        = "${var.name}-nginx"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "instance"
  health_check {
    enabled             = true
    path                = "/healthz"
    port                = "traffic-port"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_target_group_attachment" "nginx" {
  target_group_arn = aws_lb_target_group.nginx.arn
  target_id        = aws_instance.nginx.id
  port             = 80
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.application.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate_validation.application.certificate_arn
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.nginx.arn
  }
}

resource "aws_cloudfront_vpc_origin" "application" {
  vpc_origin_endpoint_config {
    name                   = "${var.name}-private-origin"
    arn                    = aws_lb.application.arn
    http_port              = 80
    https_port             = 443
    origin_protocol_policy = "https-only"
    origin_ssl_protocols {
      items    = ["TLSv1.2"]
      quantity = 1
    }
  }
  depends_on = [aws_lb_listener.https, aws_internet_gateway.main]
}

data "aws_cloudfront_cache_policy" "disabled" { name = "Managed-CachingDisabled" }
data "aws_cloudfront_origin_request_policy" "all_viewer" { name = "Managed-AllViewer" }

resource "aws_cloudfront_distribution" "application" {
  enabled         = true
  is_ipv6_enabled = true
  aliases         = [var.domain_name]
  price_class     = "PriceClass_100"
  comment         = "${var.domain_name} private VPC origin"
  origin {
    domain_name = aws_lb.application.dns_name
    origin_id   = "private-application"
    vpc_origin_config {
      vpc_origin_id = aws_cloudfront_vpc_origin.application.id
    }
  }
  default_cache_behavior {
    target_origin_id         = "private-application"
    viewer_protocol_policy   = "redirect-to-https"
    allowed_methods          = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods           = ["GET", "HEAD"]
    cache_policy_id          = data.aws_cloudfront_cache_policy.disabled.id
    origin_request_policy_id = data.aws_cloudfront_origin_request_policy.all_viewer.id
    compress                 = true
  }
  restrictions {
    geo_restriction { restriction_type = "none" }
  }
  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.application.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
  depends_on = [aws_vpc_security_group_ingress_rule.alb_from_cloudfront]
}

resource "aws_route53_record" "application" {
  for_each = var.publish_dns ? toset(["A", "AAAA"]) : toset([])
  zone_id  = var.hosted_zone_id
  name     = var.domain_name
  type     = each.value
  alias {
    name                   = aws_cloudfront_distribution.application.domain_name
    zone_id                = aws_cloudfront_distribution.application.hosted_zone_id
    evaluate_target_health = false
  }
}
