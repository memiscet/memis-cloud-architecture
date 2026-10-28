# Setup and deployment preparation

The repository can be inspected and tested without an AWS account. Creating resources is a separate operation that incurs charges. No live AWS deployment was performed to produce this workspace.

## Local prerequisites
Use Python 3.11+ and Terraform 1.11+ on a supported machine. From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/verify_workspace.py
terraform -chdir=projects/memis-cloud/infra init -backend=false -input=false
terraform -chdir=projects/memis-cloud/infra fmt -check -recursive
terraform -chdir=projects/memis-cloud/infra validate
terraform -chdir=projects/memis-cloud/infra test
```

On Windows, replace `python3` with `py -3`, and `.venv/bin/python` with `.venv\Scripts\python.exe`. Terraform commands stay the same. Mock tests use the Terraform test framework with a mocked AWS provider: their apply phases manipulate local mock state, not AWS resources. A mocked pass is not a successful real apply.

The provider lock file records the selected provider and verified checksums for macOS ARM64 and Linux AMD64. After a provider upgrade, refresh both platforms before committing:

```sh
terraform -chdir=projects/memis-cloud/infra providers lock -platform=darwin_arm64 -platform=linux_amd64
```

CI uses a read-only lock file and retains checksum enforcement. The AMI lookup resolves the latest AL2023 ARM64 image during a real plan, and bootstrap selects the current AL2023 package release. Review and record both for a real rollout; an immutable image pipeline is a later operational improvement.

## Supply real deployment values
Copy `infra/terraform.tfvars.example` to `infra/terraform.tfvars`. Replace the example hosted-zone ID. Confirm the zone is public and owns the chosen domain. Check existing DNS and CloudFront aliases, overlapping address ranges, account-local AZ aliases, RDS PostgreSQL 17/class availability, and VPC-origin quotas and permissions.

The default leaves `publish_dns = false`. ACM DNS validation records are still part of a real apply, but apex A/AAAA cutover is separate. Do not assume a placeholder value has been verified merely because it passes syntax checks.

Decide on a protected state location before working as a team. The configuration has no preselected backend; use an encrypted remote backend with locking and restricted access, following your account conventions. State and saved plans can expose infrastructure details. They are ignored by Git. The RDS-managed password is not an input and must not be copied into files.

## Inspect an account-backed plan
Authenticate using the account's normal AWS CLI or SSO process. From the repository root:

```sh
aws sts get-caller-identity
terraform -chdir=projects/memis-cloud/infra plan -out=reviewed.tfplan
terraform -chdir=projects/memis-cloud/infra show reviewed.tfplan
```

These real-account steps were not run for the published artifact. A plan can query AWS without creating resources. Review all changes, costs, and permissions. The executing principal needs the relevant service permissions, PassRole, and CloudFront VPC-origin service-linked-role creation where required. This is an infrastructure-provisioning identity, separate from the restricted EC2 instance role.

## Provisioning and checking, when authorized
Apply only the reviewed saved plan in the intended account:

```sh
terraform -chdir=projects/memis-cloud/infra apply reviewed.tfplan
```

Creation can take time for the database, certificate validation, and CloudFront. The VPC-origin group is looked up after origin creation; if account-specific discovery fails, inspect AWS's created group rather than manufacturing one with its reserved name.

Use outputs for the instance ID, target-group ARN, bucket, DB endpoint, and CloudFront domain. Follow the [live checklist](../artifacts/live-checklist.yaml). Test the alternate domain and Host/certificate behavior before apex cutover, using a controlled DNS or browser test setup that preserves the memis.cloud Host name; the generated CloudFront hostname alone does not prove this path.

## DNS cutover
Set `publish_dns = true`, create a fresh plan, and inspect the A/AAAA alias changes. If records already exist outside this state, import those exact records using the provider's documented Route 53 record import format and review the resulting plan. Do not enable overwriting as a shortcut. Check propagation and HTTPS after the separately authorized apply.

## Application integration
Create a separate least-privilege PostgreSQL application user through an authorized administration path. Store its credentials in a separate Secrets Manager secret and optionally configure `application_secret_arn` and its customer-managed key ARN. The EC2 role explicitly denies retrieving the RDS administrator secret. Add the actual runtime behind Nginx, verify PostgreSQL TLS with the RDS CA, and test secret rotation/reconnection. None of those business-runtime behaviors are implemented by the bootstrap page.
