# Experience: visitors and operators

## People and goals
A visitor needs a predictable HTTPS entry. An operator needs to maintain a private service and distinguish validated files from a working deployment.

## Visitor journey
The browser resolves memis.cloud, connects to CloudFront, and follows an HTTP-to-HTTPS redirect if needed. CloudFront forwards uncached requests privately to the ALB. The ALB checks /healthz and forwards to Nginx. The bootstrap page identifies the reference service without claiming a database-backed product exists.

## Failure outcomes
No healthy target can cause a service error. The operator checks target health and bootstrap before changing DNS. A CloudFront 502 may indicate origin TLS or Host mismatch. A passing /healthz confirms Nginx only, not DB or S3 access. Product-specific readiness remains future work.

## Operator journey
Read the decisions, supply the hosted-zone ID, and validate. Inspect a real AWS plan before rollout. After separately authorized provisioning, verify HTTPS, private placement, SSM, update access, and denied connections. Record observations in the live checklist rather than inferring success from file validation.

## Updates and recovery
Use controlled maintenance or a replacement image. Check Nginx configuration before reload and keep a last-known-good image/configuration. Replacing the only instance causes downtime. Database restore and S3 version recovery require operator action and a verification exercise.

## Accessibility and practical use
The bootstrap page uses semantic HTML, readable text, and a viewport declaration. Documentation supplies tables alongside diagrams. No accessibility audit, browser study, or user research is claimed. Real application access needs belong in its product scope.

## Wording and thresholds
Health checks expect HTTP 200 from /healthz. Terraform defines actual timing settings. Backup and maintenance choices are proposed decisions rather than measured service guarantees.

## Assumptions and open questions
Domain ownership and AWS access are rollout prerequisites. Product behavior, audience, messages, and performance targets remain unspecified and are not invented here.
