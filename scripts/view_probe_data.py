#!/usr/bin/env python3
"""
Rich TUI Viewer for Docker Prober Utility
Displays collected host information in a beautiful, formatted interface
Falls back to plain JSON if rich is not available
"""

import json
import sys
from pathlib import Path

# Try to import rich, fall back to plain output if not available
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.tree import Tree
    from rich.syntax import Syntax
    from rich.layout import Layout
    from rich import box
    from rich.text import Text
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

def load_probe_data(filepath="probe_data.json"):
    """Load probe data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        if RICH_AVAILABLE:
            console.print(f"[red]Error: {filepath} not found[/red]")
            console.print("[yellow]Run the collection script first:[/yellow]")
            console.print("  python3 scripts/collect_host_info.py")
        else:
            print(f"Error: {filepath} not found")
            print("Run the collection script first:")
            print("  python3 scripts/collect_host_info.py")
        sys.exit(1)
    except json.JSONDecodeError as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error decoding JSON: {e}[/red]")
        else:
            print(f"Error decoding JSON: {e}")
        sys.exit(1)

def create_network_table(network_data):
    """Create a table for network information"""
    table = Table(title="Network Configuration", box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("Property", style="green")
    table.add_column("Value", style="white")
    
    table.add_row("Hostname", network_data.get("hostname", "N/A"))
    table.add_row("FQDN", network_data.get("fqdn", "N/A"))
    
    ips = network_data.get("ip_addresses", [])
    ip_str = ", ".join(ips) if isinstance(ips, list) else str(ips)
    table.add_row("IP Addresses", ip_str)
    
    return table

def create_resources_table(resources_data):
    """Create a table for resource information"""
    table = Table(title="System Resources", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Resource", style="green")
    table.add_column("Details", style="white")
    
    table.add_row("CPU Count", str(resources_data.get("cpu_count", "N/A")))
    table.add_row("CPU Info", str(resources_data.get("cpu_info", "N/A"))[:60])
    
    load_avg = resources_data.get("load_average", "N/A")
    if isinstance(load_avg, (list, tuple)):
        load_str = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
    else:
        load_str = str(load_avg)
    table.add_row("Load Average", load_str)
    
    return table

def create_os_table(os_data):
    """Create a table for OS information"""
    table = Table(title="Operating System", box=box.ROUNDED, show_header=True, header_style="bold yellow")
    table.add_column("Property", style="green")
    table.add_column("Value", style="white")
    
    table.add_row("System", os_data.get("system", "N/A"))
    table.add_row("Release", os_data.get("release", "N/A"))
    table.add_row("Machine", os_data.get("machine", "N/A"))
    table.add_row("Kernel", os_data.get("kernel_version", "N/A"))
    
    return table

def create_docker_table(docker_data):
    """Create a table for Docker information"""
    table = Table(title="Docker Environment", box=box.ROUNDED, show_header=True, header_style="bold blue")
    table.add_column("Component", style="green")
    table.add_column("Version/Status", style="white")
    
    table.add_row("Docker", docker_data.get("docker_version", "N/A"))
    table.add_row("Docker Compose", docker_data.get("docker_compose_version", "N/A"))
    table.add_row("Status", docker_data.get("docker_status", "N/A"))
    
    return table

def display_probe_data_plain(data):
    """Display probe data in plain text format (fallback when rich is not available)"""
    print("\n" + "="*60)
    print("Docker Prober Utility - Host Information")
    print("="*60)
    print(f"Collected at: {data.get('timestamp', 'Unknown')}")
    print("="*60 + "\n")
    
    # Network
    print("NETWORK CONFIGURATION:")
    network = data.get("network", {})
    print(f"  Hostname: {network.get('hostname', 'N/A')}")
    print(f"  FQDN: {network.get('fqdn', 'N/A')}")
    ips = network.get("ip_addresses", [])
    ip_str = ", ".join(ips) if isinstance(ips, list) else str(ips)
    print(f"  IP Addresses: {ip_str}")
    print()
    
    # Resources
    print("SYSTEM RESOURCES:")
    resources = data.get("resources", {})
    print(f"  CPU Count: {resources.get('cpu_count', 'N/A')}")
    print(f"  CPU Info: {str(resources.get('cpu_info', 'N/A'))[:60]}")
    load_avg = resources.get("load_average", "N/A")
    if isinstance(load_avg, (list, tuple)):
        load_str = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
    else:
        load_str = str(load_avg)
    print(f"  Load Average: {load_str}")
    print()
    
    # OS
    print("OPERATING SYSTEM:")
    os_info = data.get("os_details", {})
    print(f"  System: {os_info.get('system', 'N/A')}")
    print(f"  Release: {os_info.get('release', 'N/A')}")
    print(f"  Machine: {os_info.get('machine', 'N/A')}")
    print(f"  Kernel: {os_info.get('kernel_version', 'N/A')}")
    print()
    
    # Docker
    print("DOCKER ENVIRONMENT:")
    docker = data.get("docker_environment", {})
    print(f"  Docker: {docker.get('docker_version', 'N/A')}")
    print(f"  Docker Compose: {docker.get('docker_compose_version', 'N/A')}")
    print(f"  Status: {docker.get('docker_status', 'N/A')}")
    print()
    
    # Environment
    print("ENVIRONMENT VARIABLES:")
    env = data.get("environment_variables", {})
    for key, value in sorted(env.items()):
        print(f"  {key}: {str(value)[:50]}")
    print()
    
    print("="*60)
    print("For full details, see probe_data.json")
    print("To get colorful output, install rich: pip install rich")
    print("="*60 + "\n")

def display_probe_data(data):
    """Display probe data in a rich TUI"""
    console.clear()
    
    # Header
    header_text = Text("Docker Prober Utility", style="bold white on blue", justify="center")
    timestamp = data.get("timestamp", "Unknown")
    subheader = Text(f"Data collected at: {timestamp}", style="dim", justify="center")
    
    console.print(Panel(header_text, expand=False, border_style="blue"))
    console.print(subheader)
    console.print()
    
    # Network Configuration
    network_data = data.get("network", {})
    console.print(create_network_table(network_data))
    console.print()
    
    # System Resources
    resources_data = data.get("resources", {})
    console.print(create_resources_table(resources_data))
    console.print()
    
    # Operating System
    os_data = data.get("os_details", {})
    console.print(create_os_table(os_data))
    console.print()
    
    # Docker Environment
    docker_data = data.get("docker_environment", {})
    console.print(create_docker_table(docker_data))
    console.print()
    
    # Storage Summary
    storage_data = data.get("storage", {})
    if storage_data.get("available_space"):
        console.print(Panel(
            f"[green]Available Space:[/green]\n{storage_data.get('available_space', 'N/A')[:200]}",
            title="Storage",
            border_style="green"
        ))
        console.print()
    
    # Environment Variables
    env_data = data.get("environment_variables", {})
    if env_data:
        env_table = Table(title="Environment Variables", box=box.SIMPLE)
        env_table.add_column("Variable", style="cyan")
        env_table.add_column("Value", style="white")
        
        for key, value in sorted(env_data.items()):
            env_table.add_row(key, str(value)[:50])
        
        console.print(env_table)
        console.print()
    
    # Footer
    console.print(Panel(
        "[dim]Use this data to configure your Docker stack\nView full details in probe_data.json[/dim]",
        border_style="dim"
    ))

def main():
    """Main entry point"""
    filepath = sys.argv[1] if len(sys.argv) > 1 else "probe_data.json"
    
    data = load_probe_data(filepath)
    
    if RICH_AVAILABLE:
        display_probe_data(data)
    else:
        print("\nNote: Rich library not found. Using plain text output.")
        print("Install rich for beautiful formatted output: pip install rich\n")
        display_probe_data_plain(data)

if __name__ == "__main__":
    main()
