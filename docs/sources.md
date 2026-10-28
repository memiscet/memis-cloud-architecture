# Official references

Consulted 2026-10-28. Verify current service support before a real rollout.

| Topic | Primary source |
|---|---|
| Private CloudFront origins, prerequisites, and service SG | [AWS VPC origins](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html) |
| Origin HTTPS certificate and Host matching | [CloudFront origin HTTPS](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-https-cloudfront-to-custom-origin.html) |
| ACM certificate region and names | [CloudFront certificate requirements](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html) |
| ALB subnets and behavior | [Application Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html) |
| Subnet capacity | [VPC subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html) |
| Database network and subnet group | [RDS in a VPC](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html) |
| Administrator password management | [RDS and Secrets Manager](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html) |
| RDS standby behavior | [Multi-AZ DB instances](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html) |
| NAT connectivity | [NAT Gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) |
| S3 private routing | [S3 gateway endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html) |
| AL2023 endpoint repository exception | [AWS private-subnet policies](https://docs.aws.amazon.com/emr/latest/ManagementGuide/private-subnet-iampolicy.html) |
| AL2023 release updates | [Amazon Linux updates](https://docs.aws.amazon.com/linux/al2023/ug/managing-repos-os-updates.html) |
| Maintenance access | [Session Manager prerequisites](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-prerequisites.html) |
| Terraform VPC-origin resource | [HashiCorp provider documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_vpc_origin) |
| Mocked tests | [Terraform provider mocking](https://developer.hashicorp.com/terraform/language/tests/mocking) |
| Copilot skills | [GitHub skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) |
| Prompt files | [VS Code prompt files](https://code.visualstudio.com/docs/agent-customization/prompt-files) |
| Scoped instructions | [VS Code custom instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |
