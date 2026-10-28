variable "name" {
  description = "Short resource prefix; lowercase letters, digits and internal hyphens."
  type        = string
  default     = "memis-cloud"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,18}[a-z0-9]$", var.name)) && !strcontains(var.name, "--")
    error_message = "Use 3-20 lowercase characters, starting with a letter and ending with a letter or digit; avoid consecutive hyphens."
  }
}

variable "domain_name" {
  description = "Apex name for this reference configuration."
  type        = string
  default     = "memis.cloud"
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]*\\.[a-z]{2,}$", var.domain_name))
    error_message = "Use a lowercase DNS name."
  }
}

variable "hosted_zone_id" {
  description = "ID of the existing public Route 53 zone. No zone is created."
  type        = string
  validation {
    condition     = can(regex("^Z[A-Z0-9]{5,}$", var.hosted_zone_id))
    error_message = "Supply an existing public hosted-zone ID beginning with Z."
  }
}

variable "publish_dns" {
  description = "Create apex A/AAAA aliases only when ready for DNS cutover."
  type        = bool
  default     = false
}

variable "availability_zones" {
  description = "Three distinct us-east-1 AZ aliases available in the target account."
  type        = map(string)
  default = {
    a = "us-east-1a"
    b = "us-east-1b"
    c = "us-east-1c"
  }
  validation {
    condition = (
      toset(keys(var.availability_zones)) == toset(["a", "b", "c"]) &&
      length(toset(values(var.availability_zones))) == 3 &&
      alltrue([for az in values(var.availability_zones) : can(regex("^us-east-1[a-z]$", az))])
    )
    error_message = "Supply keys a, b, c with three different us-east-1 AZ names."
  }
}

variable "instance_type" {
  description = "ARM-compatible EC2 type for the AL2023 ARM64 image."
  type        = string
  default     = "t4g.small"
  validation {
    condition     = can(regex("^[a-z][a-z0-9]*g[a-z]*\\.[a-z0-9]+$", var.instance_type))
    error_message = "Select an ARM Graviton family, such as t4g.small, to match the AMI."
  }
}

variable "postgres_version" {
  description = "PostgreSQL 17 version available in the selected account/region."
  type        = string
  default     = "17"
  validation {
    condition     = can(regex("^17(\\.[0-9]+)?$", var.postgres_version))
    error_message = "Use PostgreSQL 17 to match the parameter-group family."
  }
}

variable "database_instance_class" {
  type        = string
  description = "RDS class; confirm availability and workload sizing before apply."
  default     = "db.t4g.small"
}

variable "application_secret_arn" {
  description = "Optional existing application-user secret. Never use the RDS administrator secret here."
  type        = string
  default     = null
  validation {
    condition     = var.application_secret_arn == null ? true : can(regex("^arn:aws:secretsmanager:us-east-1:[0-9]{12}:secret:.+$", var.application_secret_arn))
    error_message = "Use an application secret ARN in us-east-1, or null."
  }
}

variable "application_secret_kms_key_arn" {
  description = "Optional customer-managed key protecting the application secret."
  type        = string
  default     = null
  validation {
    condition = var.application_secret_kms_key_arn == null ? true : (
      var.application_secret_arn != null && can(regex("^arn:aws:kms:us-east-1:[0-9]{12}:key/.+$", var.application_secret_kms_key_arn))
    )
    error_message = "A secret key ARN requires an application secret ARN and must be in us-east-1."
  }
}

variable "final_snapshot_identifier" {
  description = "Unique final DB snapshot name; change if an earlier snapshot already uses this name."
  type        = string
  default     = "memis-cloud-final"
}
