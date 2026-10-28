---
applyTo: "projects/memis-cloud/infra/**"
---

Read the project's scope, architecture, network-and-access, and decisions documents. Keep six subnets in the baseline and preserve an internal ALB with a CloudFront VPC origin. The allocation in projects/memis-cloud/network.yaml is consumed by Terraform.

Run terraform fmt, validate, and mocked tests for changed infrastructure. Keep mock-provider tests separate from real AWS plans and deployments. Never claim live TLS, permissions, or health checks passed solely because mocks passed. Keep credentials, state, saved plans, and actual tfvars out of Git.
