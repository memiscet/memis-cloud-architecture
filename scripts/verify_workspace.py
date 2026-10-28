"""Run local workspace checks without calling AWS or an AI service."""

from ipaddress import ip_network
from pathlib import Path
import subprocess
import sys
import yaml

from check_copilot import check_copilot
from check_example import check_guide
from check_repository import check_repository
from validate import ContractError, ROOT, validate_project


def check_network(path: Path) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    vpc = ip_network(data["vpc_cidr"], strict=True)
    if vpc.version != 4 or not vpc.is_private:
        raise ValueError("VPC must use private IPv4 space")
    if set(data["subnets"]) != {"a", "b", "c"}:
        raise ValueError("Allocation must define keys a, b, c")
    subnets = [ip_network(item[key], strict=True) for item in data["subnets"].values() for key in ("public_cidr", "private_cidr")]
    if any(not subnet.subnet_of(vpc) or subnet.prefixlen != 24 for subnet in subnets):
        raise ValueError("All six /24 subnets must be inside the VPC")
    for index, subnet in enumerate(subnets):
        if any(subnet.overlaps(other) for other in subnets[index + 1:]):
            raise ValueError("Subnet ranges overlap")


def main() -> int:
    try:
        errors = check_repository() + check_copilot()
        if errors:
            raise ValueError("\n".join(errors))
        check_network(ROOT / "projects/memis-cloud/network.yaml")
        check_guide(ROOT / "examples/community-event/artifacts/welcome-guide.md")
        for project in (ROOT, ROOT / "projects/memis-cloud", ROOT / "examples/community-event"):
            for message in validate_project(project, complete=True):
                print(message)
        validate_project(ROOT / "examples/software-request")
    except (OSError, ValueError, ContractError, yaml.YAMLError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT)
    if result.returncode:
        return result.returncode
    print("Workspace checks passed. Terraform checks and interactive/live tests are separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
