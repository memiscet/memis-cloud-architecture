resource "aws_db_subnet_group" "application" {
  name       = "${var.name}-database"
  subnet_ids = [aws_subnet.private["b"].id, aws_subnet.private["c"].id]
}

resource "aws_db_parameter_group" "application" {
  name   = "${var.name}-postgres17"
  family = "postgres17"
  parameter {
    name         = "rds.force_ssl"
    value        = "1"
    apply_method = "pending-reboot"
  }
}

resource "aws_db_instance" "application" {
  identifier                      = "${var.name}-database"
  engine                          = "postgres"
  engine_version                  = var.postgres_version
  instance_class                  = var.database_instance_class
  allocated_storage               = 20
  max_allocated_storage           = 100
  storage_type                    = "gp3"
  storage_encrypted               = true
  db_name                         = "memiscloud"
  username                        = "dbadmin"
  manage_master_user_password     = true
  db_subnet_group_name            = aws_db_subnet_group.application.name
  parameter_group_name            = aws_db_parameter_group.application.name
  vpc_security_group_ids          = [aws_security_group.database.id]
  publicly_accessible             = false
  multi_az                        = true
  backup_retention_period         = 7
  backup_window                   = "03:00-04:00"
  maintenance_window              = "sun:04:00-sun:05:00"
  deletion_protection             = true
  skip_final_snapshot             = false
  final_snapshot_identifier       = var.final_snapshot_identifier
  auto_minor_version_upgrade      = true
  copy_tags_to_snapshot           = true
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
}
