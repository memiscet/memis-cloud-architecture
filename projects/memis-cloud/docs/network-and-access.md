# Network and access reference

A subnet is a smaller address range inside the VPC. A route table chooses the next destination for traffic. A security group decides which connections a resource accepts. A private address and a restrictive security group solve different parts of the problem.

## Address allocation

Propose **10.64.0.0/20**, containing 4,096 addresses and sixteen /24 slots. Six /24 subnets leave ten slots for growth. Each /24 has 256 addresses, with AWS-reserved addresses reducing usable capacity. There is no universally optimal CIDR; compare this proposal with every connected VPC, VPN, on-premises network, and planned peering range before rollout. [AWS subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html).

The names below are default account-local AZ aliases, not globally stable physical-zone identities. Confirm availability in the destination account.

| Subnet | CIDR | Default AZ | Purpose | Route table |
|---|---|---|---|---|
| Public A | 10.64.0.0/24 | us-east-1a | NAT A and its Elastic IP | Public |
| Public B | 10.64.1.0/24 | us-east-1b | NAT B and its Elastic IP | Public |
| Public C | 10.64.2.0/24 | us-east-1c | NAT C and its Elastic IP | Public |
| Private A | 10.64.8.0/24 | us-east-1a | Nginx and ALB interface | Private A |
| Private B | 10.64.9.0/24 | us-east-1b | RDS subnet group and ALB interface | Private B |
| Private C | 10.64.10.0/24 | us-east-1c | RDS subnet group and ALB interface | Private C |

[network.yaml](../network.yaml) is the machine-readable source consumed by Terraform. Python checks verify containment, /24 sizing, and non-overlap. ALB interfaces share subnets with other resources; no claim of a dedicated subnet per tier is made.

## Route tables

| Table | Destination | Target |
|---|---|---|
| All four tables | VPC range | VPC-local routing |
| Public | 0.0.0.0/0 | Internet Gateway |
| Private A | 0.0.0.0/0 | NAT A in Public A |
| Private B | 0.0.0.0/0 | NAT B in Public B |
| Private C | 0.0.0.0/0 | NAT C in Public C |
| Each private table | Regional S3 prefix list | S3 gateway endpoint |

RDS's managed maintenance is not performed by logging into it through NAT. Its subnets share the baseline private route pattern, while its security group exposes no outbound rule and accepts only application-originated PostgreSQL connections. Security groups are stateful, so replies do not need a separate outgoing permission.

## Allowed connections

| Source | Destination | Port | Control |
|---|---|---|---|
| Viewer | CloudFront | 443; HTTP redirects | Distribution policy and certificate |
| CloudFront service-managed VPC-origin SG | Internal ALB SG | TCP 443 | SG identity reference |
| ALB SG | Application SG | TCP 80 | Matching ingress and egress rules |
| Application SG | Database SG | TCP 5432 | Matching ingress and egress rules |
| Application instance | HTTPS destinations | TCP 443 | Egress rule; NAT or S3 endpoint route |
| Operator | SSM service | HTTPS | Operator IAM and instance agent; no inbound SSH |

There is no public ALB, public instance address, public database, inbound SSH rule, or broad PostgreSQL ingress. The application HTTPS egress rule permits any destination address on port 443; it is not a domain allowlist. A stricter egress proxy or firewall would be a separate design change.

## S3, updates, and routing precedence
Application object requests take the gateway endpoint path, using the instance role. The role grants only application-prefix listing and object read/write. The endpoint policy is an additional filter, not a replacement for IAM or bucket permissions.

The endpoint also allows read-only requests to `al2023-repos-us-east-1-de612dc2/*`. Amazon Linux repositories use S3, and the specific endpoint route wins over the default NAT route. Without this exception, package bootstrap can fail even with a functioning NAT. General internet HTTPS, third-party repositories when configured, and SSM use NAT. [AWS repository access guidance](https://docs.aws.amazon.com/emr/latest/ManagementGuide/private-subnet-iampolicy.html); [Amazon Linux update behavior](https://docs.aws.amazon.com/linux/al2023/ug/managing-repos-os-updates.html).

CloudFront origin traffic does not traverse the NAT. DNS queries do not traverse the ALB. The S3 bucket itself is a regional service, not a resource placed inside a subnet.
