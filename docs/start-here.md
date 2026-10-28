# Start here: what are we building?

This repository is the blueprint and preparation kit for memis.cloud. It explains where the parts go, includes files describing how AWS could create them, and records the checks performed. It is not evidence that a website has already been deployed.

## Think of a building

Route 53 is the address book: it tells a browser where to connect. CloudFront is the public reception point. The load balancer is a dispatcher behind reception. Nginx is the private web server. The database holds structured application information, and S3 stores objects such as uploaded files.

A VPC is the private network containing the server infrastructure. Subnets are sections of that network. Public subnets have a route to the Internet Gateway; private subnets do not use that gateway directly. NAT lets a private instance initiate an outbound connection for maintenance without accepting an unsolicited inbound connection through that path.

An IAM role describes what the instance may do with AWS services. Security groups restrict network connections. A private address does not replace either control.

## What the baseline chooses

There are six subnets across three Availability Zones. Nginx is in private A. The database can use private B or C, keeping it separate from the Nginx subnet. The private load balancer shares those subnets. Each public subnet contains a NAT Gateway. S3 access uses a gateway endpoint, a private service access route.

There is only one Nginx instance. If it fails, the application can be unavailable even though other AWS components have redundancy. The [decisions](../projects/memis-cloud/docs/decisions.md) explain a nine-subnet alternative for clearer separation and application expansion.

The server initially displays a simple reference page. The real application's features and database queries still need product requirements and a runtime. The repository does not disguise the reference page as a completed business application.

## How the framework helps

The seven steps are: agree the scope, choose the architecture, describe the experience, split work into deliverables, plan one piece, create it, and review the evidence. A skill is an instruction card for one step. An artifact is a saved result. Acceptance criteria are promises that can be checked.

Every deliverable has a plan, a summary, and a review. A passing file check confirms a valid handoff; it does not prove a live system works. Checks not performed are labeled not_run. See the [validation record](validation-report.md).

## Your next step

Read the [architecture](../projects/memis-cloud/docs/architecture.md) for design details, the [Copilot tutorial](../tutorials/04-copilot-memis-cloud.md) to continue the work, or the [setup guide](../projects/memis-cloud/docs/setup.md) for technical checks. The [glossary](glossary.md) explains the remaining terms.
