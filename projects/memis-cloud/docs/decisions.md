# Decisions, alternatives, and unresolved rollout questions

## Decision record

| Topic | Baseline | Why | Tradeoff or alternative |
|---|---|---|---|
| Region | us-east-1 | Supported VPC-origin region and one region for edge/origin certificate | Other regions need a separate us-east-1 viewer certificate provider |
| Address range | 10.64.0.0/20; six /24s | Modest capacity with ten spare /24 slots | Inventory must confirm no overlapping connected ranges |
| Subnets | Three public plus three private | Meets the requested count | ALB shares private subnets with application/database roles |
| Database placement | RDS subnet group in private B/C | Separate from Nginx A, cross-AZ DB placement | Application remains concentrated in A |
| Origin | Internal ALB through a CloudFront VPC origin | Keeps origin resources private | Feature and account prerequisites must be checked |
| NAT | One public NAT and Elastic IP per AZ | Avoid one shared zonal outbound dependency | Three hourly NAT charges plus processing and address charges |
| Compute | One ARM EC2 instance running Nginx | Minimal reference service matching the requirement | Single application failure point; no seamless replacement |
| Database | PostgreSQL 17 Multi-AZ DB instance | General relational default with standby | Workload, version, class, budget, and restore objectives need confirmation |
| Storage | Private versioned SSE-S3 bucket and gateway endpoint | No application-bucket public access; avoids NAT for regional S3 | Old versions cost money; lifecycle retention needs business input |
| Cache | Caching disabled by default | Unknown application semantics, including authenticated responses | Add narrowly defined static caching for performance later |
| TLS | Viewer-to-edge and edge-to-ALB HTTPS | Public and origin transport protected | ALB-to-Nginx HTTP; instance TLS is an explicit enhancement |
| IaC | Terraform with provider lock and mocked tests | Source framework has no existing IaC implementation | Mock tests do not verify account permissions or live services |

## Six versus nine subnets
The six-subnet baseline meets the requested count and keeps RDS out of the Nginx subnet. Security groups separate roles, but ALB interfaces share those private subnets. Calling this three dedicated tiers in three AZs would be inaccurate.

A nine-subnet alternative provides three public, three private application, and three isolated database subnets. It permits an application Auto Scaling Group across AZs and database route tables without NAT defaults. Choosing it requires an explicit scope/plan revision; it is not hidden in the supplied Terraform.

## Cost model
Estimate three NAT hourly charges, processed NAT bytes, public IPv4 addresses, ALB hours/capacity units, CloudFront usage, EC2, EBS, detailed monitoring, Multi-AZ RDS, backups, Secrets Manager, S3 objects/versions/requests, and applicable data transfer. The S3 gateway endpoint avoids NAT processing for its regional S3 traffic; it does not make S3 free. Use current [AWS pricing](https://aws.amazon.com/pricing/) and [the calculator](https://calculator.aws/) with actual region, usage, retention, and commitments. No invented monthly total is provided.

A single NAT can reduce fixed cost, but introduces a shared zonal dependency and possible cross-AZ transfer. Single-AZ RDS reduces resilience. Neither change is silently applied. Three NATs do not make the one-instance application highly available.

## Rollout decisions still owned by the user
Confirm AWS account, zone ID, current DNS records, address conflicts, three AZs, domain alias availability, traffic shape, database sizing, downtime tolerance, retention, recovery objectives, and the actual runtime and its database user. Configure the runtime's TLS verification and secret refresh before using the DB for product data. An account-backed plan, deployment, and recovery exercise are still needed to assess operational readiness.
