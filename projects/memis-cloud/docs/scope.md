# Scope: memis.cloud

## Problem and people
The owner needs a clear, reusable design for a web application whose servers and database are private. Visitors enter through a CDN. Operators need to maintain the instance and understand what has actually been verified.

## Intended result
Deliver an architecture, Terraform configuration, Copilot-compatible workflow, and understandable operating guides. The infrastructure boots a small Nginx landing page and health endpoint. Business behavior and a database schema are not specified, so the package identifies the runtime integration work rather than inventing product features.

## Confirmed requirements
The domain is memis.cloud and its DNS is hosted in Route 53. A CDN fronts an internal load balancer and private Nginx server. The VPC has three public and three private subnets, an Internet Gateway, NAT routing, a database separate from Nginx's subnet, and an S3 bucket accessible through the server's role. The workspace follows the seven-stage framework and is published publicly under memiscet.

## Success measures
An operator can trace every requested connection through diagrams, subnet tables, routes, and security groups. Terraform passes formatting, provider schema validation, and mocked configuration assertions. Every deliverable has a current plan and evidence-based review. Seven Copilot skills remain synchronized with their canonical files; prompts and documentation links validate.

## Included
An IPv4 reference deployment in us-east-1; three zonal NAT Gateways; an internal ALB; a CloudFront VPC origin; HTTPS at the edge and ALB; one private EC2 Nginx instance; Multi-AZ RDS PostgreSQL; encrypted private S3 storage with prefix-limited instance permissions; an S3 gateway endpoint; SSM maintenance access; and a live verification checklist.

## Excluded
Live AWS provisioning and DNS cutover in this repository-building task; a finished business application; application database schema and user provisioning; a production availability or recovery guarantee; interactive Copilot testing when no interactive client is available.

## Constraints
Exactly six subnets in the baseline. Preserve the framework's V1 contracts. Keep project facts out of general skills. Exclude credentials, Terraform state, saved plans, and private configuration from publication.

## Proposed decisions
Use Terraform because the source has no established infrastructure implementation and it supports reproducible provider locking and mocked tests. Use 10.64.0.0/20 for a modest initial allocation with expansion space, subject to network inventory. Use RDS PostgreSQL as a general relational default; no workload-specific superiority is claimed.

## Assumptions
The operator will supply the existing public hosted-zone ID, owns the domain, and has AWS access. The selected three us-east-1 AZ names are available in that account. A single instance is acceptable for the reference package, with its availability limit documented. The domain has no conflicting CloudFront alias assignment. Verify these before rollout.

## Open questions for rollout
Confirm account and zone ID, address overlap, budget and workload size, acceptable downtime, recovery objectives, application runtime, schema, and database-user privileges. These do not block the documented reference package; they block a production-readiness claim.
