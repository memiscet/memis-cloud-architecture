locals {
  network = yamldecode(file("${path.module}/../network.yaml"))
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "main" {
  cidr_block           = local.network.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = { Name = var.name }
  lifecycle {
    precondition {
      condition     = alltrue([for az in values(var.availability_zones) : contains(data.aws_availability_zones.available.names, az)])
      error_message = "Selected AZ aliases must be available in this account."
    }
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.name}-igw" }
}

resource "aws_subnet" "public" {
  for_each                = local.network.subnets
  vpc_id                  = aws_vpc.main.id
  availability_zone       = var.availability_zones[each.key]
  cidr_block              = each.value.public_cidr
  map_public_ip_on_launch = false
  tags                    = { Name = "${var.name}-public-${each.key}" }
}

resource "aws_subnet" "private" {
  for_each                = local.network.subnets
  vpc_id                  = aws_vpc.main.id
  availability_zone       = var.availability_zones[each.key]
  cidr_block              = each.value.private_cidr
  map_public_ip_on_launch = false
  tags                    = { Name = "${var.name}-private-${each.key}" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.name}-public" }
}

resource "aws_route" "public_default" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

resource "aws_route_table_association" "public" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

resource "aws_eip" "nat" {
  for_each = local.network.subnets
  domain   = "vpc"
  tags     = { Name = "${var.name}-nat-${each.key}" }
}

resource "aws_nat_gateway" "zonal" {
  for_each      = aws_subnet.public
  allocation_id = aws_eip.nat[each.key].id
  subnet_id     = each.value.id
  depends_on    = [aws_route.public_default, aws_route_table_association.public]
  tags          = { Name = "${var.name}-nat-${each.key}" }
}

resource "aws_route_table" "private" {
  for_each = local.network.subnets
  vpc_id   = aws_vpc.main.id
  tags     = { Name = "${var.name}-private-${each.key}" }
}

resource "aws_route" "private_default" {
  for_each               = aws_route_table.private
  route_table_id         = each.value.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.zonal[each.key].id
}

resource "aws_route_table_association" "private" {
  for_each       = aws_subnet.private
  subnet_id      = each.value.id
  route_table_id = aws_route_table.private[each.key].id
}
