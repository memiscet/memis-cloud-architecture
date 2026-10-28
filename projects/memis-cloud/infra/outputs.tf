output "vpc_id" { value = aws_vpc.main.id }
output "subnet_ids" {
  value = {
    public  = { for key, subnet in aws_subnet.public : key => subnet.id }
    private = { for key, subnet in aws_subnet.private : key => subnet.id }
  }
}
output "instance_id" { value = aws_instance.nginx.id }
output "target_group_arn" { value = aws_lb_target_group.nginx.arn }
output "cloudfront_domain" { value = aws_cloudfront_distribution.application.domain_name }
output "cloudfront_distribution_id" { value = aws_cloudfront_distribution.application.id }
output "application_bucket" { value = aws_s3_bucket.application.bucket }
output "database_endpoint" { value = aws_db_instance.application.address }
output "dns_published" { value = var.publish_dns }
