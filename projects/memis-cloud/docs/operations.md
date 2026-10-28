# Maintenance, diagnosis, and recovery

This guide describes expected procedures for a future deployment. Execute account-specific commands only against the intended environment. Record observations in the [live checklist](../artifacts/live-checklist.yaml).

## Routine maintenance
Use Systems Manager Session Manager with the instance ID output. The operator needs SSM permissions and, for CLI sessions, the Session Manager plugin. No inbound SSH is configured. The instance agent reaches AWS APIs over HTTPS using NAT; optional private SSM endpoints can be added later.

On the instance, inspect `cloud-init status --long`, `/var/log/cloud-init-output.log`, and `/var/log/memis-bootstrap.log`. Run `sudo nginx -t` before a reload. Check `systemctl status nginx` and `curl --fail http://127.0.0.1/healthz`. The expected response is `ok`; this confirms Nginx only.

Amazon Linux 2023 pins a repository release. Review `dnf check-release-update` and changes before `sudo dnf upgrade --releasever=latest -y`. Plan a restart when required, especially for kernel updates. Validate health after maintenance. Prefer a tested replacement image for repeatable rollouts; replacing the sole instance interrupts service. [AL2023 update behavior](https://docs.aws.amazon.com/linux/al2023/ug/managing-repos-os-updates.html).

## Diagnostic paths

| Symptom | Inspect | Next action |
|---|---|---|
| Terraform cannot load provider plugin locally | Binary platform, permissions, sandbox socket restrictions | Run in an environment that permits Terraform provider processes; do not infer a resource schema error |
| Certificate stays pending | Public zone ID, DNS validation CNAME, delegation, certificate region | Correct validation ownership/records, then recheck issuance |
| CloudFront 502 | Origin Host forwarding, certificate coverage, listener, VPC-origin state, ALB ingress | Restore matching TLS/Host configuration and test again |
| ALB has no healthy targets | Target registration, application SG, Nginx status, /healthz | Correct bootstrap/configuration; validate before reload |
| Package installation fails | NAT route, HTTPS egress, endpoint policy, bootstrap logs | Restore the actual path; AL2023 S3 repository traffic needs the endpoint read exception |
| No SSM session | Instance role/attachment, agent status, endpoint access, operator IAM | Restore agent/connectivity or use a controlled recovery instance procedure |
| DB connection fails | Runtime presence, endpoint DNS, port 5432 rules, DB user, CA/hostname verification | Correct the identified layer; Nginx health alone is not DB evidence |
| Application secret denied | Configured secret ARN, explicit administrator deny, KMS key policy | Use the application-user secret and scoped key access; retain administrator-secret separation |
| S3 request denied | Requested prefix, instance role, bucket TLS policy, endpoint policy | Use application/ and allowed read/write actions; a delete denial is expected |
| Direct origin connection fails from outside the VPC | Internal ALB and SG configuration | Expected boundary; use the CDN path for public requests |

## Recovery
For instance failure, restore the last-known-good image/configuration and register a healthy replacement. There is one target, so downtime continues until recovery. There is no automatic compute failover in this baseline.

RDS Multi-AZ can fail over to a standby; applications must reconnect using the DB endpoint and handle interrupted connections. Backups permit restore workflows, but restored databases have a new endpoint and require validation and a controlled application change. Perform a restore exercise before setting RTO/RPO expectations. [RDS Multi-AZ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html).

S3 versioning retains older object versions, but recovery requires selecting/restoring the intended version. The application role lacks delete permission. Retention and lifecycle rules need business decisions; versioning is not a complete backup strategy.

## Retiring a deployment
ALB and RDS deletion protection intentionally block accidental removal. RDS requires a final snapshot and the bucket must be empty before removal. A unique final snapshot name is necessary. Review retention, snapshot and object ownership, dependent CloudFront resources, and DNS before changing protection. No teardown was run while creating this repository.

## Observability limits
The configuration enables EC2 detailed monitoring and PostgreSQL log exports. It does not configure a complete alarm, access-log aggregation, VPC-flow-log, or on-call service. Add those through a scoped deliverable when operational requirements are known. No live service-level measurements are available.
