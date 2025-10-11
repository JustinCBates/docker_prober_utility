#!/usr/bin/env python3
"""
Host Information Collection Script
Collects critical host information for Docker stack configuration
and stores it in probe_data.json
"""

import json
import os
import platform
import socket
import subprocess
import sys
from datetime import datetime


def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        return f"Error: {str(e)}"


def collect_host_info():
    """Collect comprehensive host information"""
    info = {
        "timestamp": datetime.now().isoformat(),
        "network": {},
        "resources": {},
        "os_details": {},
        "docker_environment": {},
        "environment_variables": {},
        "storage": {},
        "proxy_dns": {},
        "locale": {},
    }

    # Network Configuration
    info["network"]["hostname"] = socket.gethostname()
    info["network"]["fqdn"] = socket.getfqdn()
    try:
        info["network"]["ip_addresses"] = socket.gethostbyname_ex(socket.gethostname())[2]
    except:
        info["network"]["ip_addresses"] = []
    
    info["network"]["network_interfaces"] = run_command("ip -br addr show") or run_command("ifconfig -a")
    info["network"]["open_ports"] = run_command("ss -tuln") or run_command("netstat -tuln")
    info["network"]["firewall_status"] = run_command("sudo iptables -L -n") or "N/A"

    # Resource Availability
    info["resources"]["cpu_count"] = os.cpu_count()
    info["resources"]["cpu_info"] = run_command("lscpu | grep 'Model name'")
    info["resources"]["memory_info"] = run_command("free -h")
    info["resources"]["swap_info"] = run_command("swapon --show")
    info["resources"]["disk_usage"] = run_command("df -h")
    info["resources"]["load_average"] = os.getloadavg() if hasattr(os, 'getloadavg') else "N/A"

    # Operating System Details
    info["os_details"]["system"] = platform.system()
    info["os_details"]["release"] = platform.release()
    info["os_details"]["version"] = platform.version()
    info["os_details"]["machine"] = platform.machine()
    info["os_details"]["processor"] = platform.processor()
    info["os_details"]["distribution"] = run_command("cat /etc/os-release")
    info["os_details"]["kernel_version"] = run_command("uname -r")

    # Docker Environment
    info["docker_environment"]["docker_version"] = run_command("docker --version")
    info["docker_environment"]["docker_compose_version"] = run_command("docker-compose --version") or run_command("docker compose version")
    info["docker_environment"]["docker_status"] = run_command("systemctl is-active docker") or run_command("service docker status")
    info["docker_environment"]["docker_info"] = run_command("docker info --format '{{json .}}'")

    # Environment Variables (selective - don't expose secrets)
    safe_env_vars = ["PATH", "HOME", "USER", "SHELL", "LANG", "TZ"]
    for var in safe_env_vars:
        info["environment_variables"][var] = os.environ.get(var, "N/A")

    # Storage and Mount Points
    info["storage"]["mount_points"] = run_command("mount")
    info["storage"]["disk_info"] = run_command("lsblk")
    info["storage"]["available_space"] = run_command("df -h /")

    # Proxy and DNS Settings
    info["proxy_dns"]["http_proxy"] = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy", "N/A")
    info["proxy_dns"]["https_proxy"] = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy", "N/A")
    info["proxy_dns"]["no_proxy"] = os.environ.get("NO_PROXY") or os.environ.get("no_proxy", "N/A")
    info["proxy_dns"]["dns_servers"] = run_command("cat /etc/resolv.conf | grep nameserver")

    # Time Zone and Locale
    info["locale"]["timezone"] = run_command("timedatectl show --property=Timezone --value") or os.environ.get("TZ", "N/A")
    info["locale"]["locale"] = os.environ.get("LANG", "N/A")
    info["locale"]["current_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return info


def save_to_json(data, filepath="probe_data.json"):
    """Save collected data to JSON file"""
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Host information saved to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving to {filepath}: {e}", file=sys.stderr)
        return False


def main():
    """Main execution function"""
    print("Collecting host information...")
    host_info = collect_host_info()
    
    # Determine output path
    output_file = sys.argv[1] if len(sys.argv) > 1 else "probe_data.json"
    
    if save_to_json(host_info, output_file):
        print("Collection complete!")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
