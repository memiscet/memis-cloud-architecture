# Validation record

Local checks were performed on 2026-10-28 using Python 3.14.7, Terraform 1.15.5, and AWS provider 6.70.0. The provider version and package hashes are recorded in the Terraform lock file.

| Check | Result |
|---|---|
| `python scripts/verify_workspace.py` | Both current projects, original examples, local links, Copilot files, network allocation, and Python tests passed |
| `python -m unittest discover -s tests -v` | 41 tests passed: 31 original contract tests plus 10 network/Copilot integration tests |
| `python scripts/sync_copilot.py --check` | Seven generated skills match canonical files |
| `python scripts/check_copilot.py` | Seven prompts, references, hints, and three scoped instruction headers passed |
| Skill-creator quick validation | All seven canonical skill headers passed; generated files are identical |
| `terraform fmt -check -recursive` in the infrastructure directory | Passed |
| `terraform validate` in the infrastructure directory | Passed with the real provider's schema |
| `terraform test` in the infrastructure directory | Eight mocked runs passed |
| `bash -n user-data.sh.tftpl` | Bootstrap template shell syntax passed; bootstrap was not executed |
| `python -m pip check` | No broken Python dependency requirements |

## What the infrastructure tests establish

Mocked runs check zonal NAT and IGW references, six subnets, private compute placement, instance metadata/storage settings, the internal origin path, HTTPS/Host configuration, ingress identity references, DB placement, storage boundaries, optional secret/key scope, explicit DNS cutover, and expected rejection of invalid or unavailable inputs.

Five runs use mocked apply so computed identifiers can be checked after local mock evaluation; three invalid-input runs use mocked plans. All use a mocked AWS provider. No AWS resources are created by these tests, and no real credentials are required.

Early mock experiments exposed computed-ID and dynamic-key limitations. The final suite resolves mock IDs locally and uses a single certificate-validation resource with stable identity. The full final assertions pass; they were not skipped or weakened to manufacture a runtime claim.

## Checks not run

- An account-backed Terraform plan or apply.
- Live DNS, certificate issuance, CDN-to-origin TLS, target health, NAT, SSM, package updates, database TLS, or S3 authorization checks.
- Database restore, secret rotation, or measured recovery exercises.
- Interactive Copilot discovery or a complete workflow in VS Code or another Copilot client.
- Business application, browser, accessibility, load, or user-study testing.

Every live infrastructure check starts as not_run in the [live checklist](../projects/memis-cloud/artifacts/live-checklist.yaml). The [Copilot compatibility record](copilot-compatibility.md) identifies interactive gaps. The passing reviews concern the local architecture/configuration/documentation package, not live deployment success.

GitHub Actions is configured for Python 3.11/3.14 and Terraform 1.15.5 on Ubuntu. Hosted workflow results are visible in the repository's Actions tab after publication and are separate from this local record.
