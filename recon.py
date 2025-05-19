import argparse
import subprocess
import socket
import pyautogui
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

console = Console()

# Define the list of reconnaissance commands
COMMANDS = [
    "ping {domain}",
    "whois {domain}",
    "nbtscan -r {ip}",
    "fping -a {domain}",
    "tcptraceroute {domain} -f 2",
    "traceroute {domain}",
    "sslyze {domain}",
    "dnsrecon -d {domain} -D /usr/share/wordlists/dnsmap.txt -t std -x {domain}_report.xml",
    "dnstracer -r 3 -v {domain}",
    "enum4linux {ip}",
    "netmask -x {domain}",
    "netmask -b {domain}",
    "knockpy -d {domain}",
    "theHarvester -d {ip}",
    "tlssled {domain}",
]

# Additional commands (without time limit)
Com = [
    "dnsenum -v {domain}",
    "masscan -p1-65535 {ip}",
    "urlcrazy -i {domain}",
    "nmap -T4 -p- -sU {domain}"
]

def get_ip(domain):
    """Retrieve IP address of the given domain."""
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"[bold green]✔ IP Address Found:[/bold green] {ip}")
        return ip
    except socket.gaierror:
        console.print("[bold red]✖ Failed to resolve IP address.[/bold red]")
        return None

# Execute command with time limit
def run_command(command, time_limit):
    """Executes a command with a time limit and captures output."""
    try:
        result = subprocess.run(command, shell=True, timeout=time_limit, capture_output=True, text=True)
        return result.stdout.strip() + "\n" + result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "[bold yellow]⚠ TIME LIMIT EXCEEDED[/bold yellow]"

# Execute command without time limit
def run_com(command):
    """Executes a command without a time limit and captures output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() + "\n" + result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "[bold yellow]⚠ TIME LIMIT EXCEEDED[/bold yellow]"

# Main function
def main(domain, time_limit):
    """Main function to execute reconnaissance commands."""
    console.print(Panel.fit(f"[bold cyan]Starting Information Gathering on {domain}[/bold cyan]"))
    pyautogui.alert("Information Gathering Started!", "Recon Script")

    ip = get_ip(domain)
    if not ip:
        return
    
    # Save results to a file
    output_file = f"{domain}_recon.txt"
    with open(output_file, "w") as file:
        file.write(f"Reconnaissance Results for {domain}\n")
        file.write("=" * 50 + "\n")
        
        # Running commands with a time limit
        with console.status("[bold cyan]Executing reconnaissance commands...[/bold cyan]"):
            for cmd in COMMANDS:
                formatted_cmd = cmd.format(domain=domain, ip=ip)
                console.print(f"\n[bold blue]➜ Running:[/bold blue] {formatted_cmd}")
                result = run_command(formatted_cmd, time_limit)
                console.print(Panel(result, title="[bold green]Output[/bold green]", expand=True, border_style="red"))

                file.write(f"\nCommand: {formatted_cmd}\n")
                file.write(result + "\n" + "-" * 50 + "\n")

        # Running additional commands (without time limit)
        with console.status("[bold cyan]Executing additional reconnaissance commands...[/bold cyan]"):
            for cmd in Com:
                formatted_cmd = cmd.format(domain=domain, ip=ip)
                console.print(f"\n[bold blue]➜ Running:[/bold blue] {formatted_cmd}")
                result = run_com(formatted_cmd)
                console.print(Panel(result, title="[bold green]Output[/bold green]", expand=True, border_style="red"))

                file.write(f"\nCommand: {formatted_cmd}\n")
                file.write(result + "\n" + "-" * 50 + "\n")

    console.print(f"[bold green]✔ Reconnaissance completed. Results saved in:[/bold green] {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Reconnaissance Tool")
    parser.add_argument("-d", required=True, help="Target domain for reconnaissance")
    parser.add_argument("-t", type=int, default=10, help="Time limit for each command (seconds)")
    
    args = parser.parse_args()
    main(args.d, args.t)
