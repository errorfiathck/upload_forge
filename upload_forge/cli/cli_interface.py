import typer
import asyncio
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box
from ..core.scanner import Scanner
from ..reporting.json_report import generate_json_report
from ..reporting.html_report import generate_html_report

app = typer.Typer(help="UploadForge - Professional File Upload Vulnerability Scanner")
console = Console()

BANNER = """
[bold green]
 █    ██  ██▓███   ██▓     ▒█████   ▄▄▄      ▓█████▄      █████▒▒█████   ██▀███    ▄████ ▓█████ 
 ██  ▓██▒▓██░  ██▒▓██▒    ▒██▒  ██▒▒████▄    ▒██▀ ██▌   ▓██   ▒▒██▒  ██▒▓██ ▒ ██▒ ██▒ ▀█▒▓█   ▀ 
▓██  ▒██░▓██░ ██▓▒▒██░    ▒██░  ██▒▒██  ▀█▄  ░██   █▌   ▒████ ░▒██░  ██▒▓██ ░▄█ ▒▒██░▄▄▄░▒███   
▓▓█  ░██░▒██▄█▓▒ ▒▒██░    ▒██   ██░░██▄▄▄▄██ ░▓█▄   ▌   ░▓█▒  ░▒██   ██░▒██▀▀█▄  ░▓█  ██▓▒▓█  ▄ 
▒▒█████▓ ▒██▒ ░  ░░██████▒░ ████▓▒░ ▓█   ▓██▒░▒████▓    ░▒█░   ░ ████▓▒░░██▓ ▒██▒░▒▓███▀▒░▒████▒
░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░░ ▒░▓  ░░ ▒░▒░▒░  ▒▒   ▓▒█░ ▒▒▓  ▒     ▒ ░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ░▒   ▒ ░░ ▒░ ░
░░▒░ ░ ░ ░▒ ░     ░ ░ ▒  ░  ░ ▒ ▒░   ▒   ▒▒ ░ ░ ▒  ▒     ░       ░ ▒ ▒░   ░▒ ░ ▒░  ░   ░  ░ ░  ░
 ░░░ ░ ░ ░░         ░ ░   ░ ░ ░ ▒    ░   ▒    ░ ░  ░     ░ ░   ░ ░ ░ ▒    ░░   ░ ░ ░   ░    ░   
   ░                  ░  ░    ░ ░        ░  ░   ░                  ░ ░     ░           ░    ░  ░
                                              ░                                                 
[/bold green]
[bold white]Professional File Upload Vulnerability Scanner[/bold white]
"""

@app.command()
def scan(
    url: str = typer.Option(..., "--url", "-u", help="Target URL for file upload"),
    param: str = typer.Option("file", "--param", "-p", help="POST parameter name for the file"),
    upload_dir: str = typer.Option(None, "--upload-dir", "-d", help="Directory where files are uploaded (URL path)"),
    output: str = typer.Option("report.json", "--output", "-o", help="Output report file (json or html)"),
    proxy: str = typer.Option(None, "--proxy", help="Proxy URL (e.g., http://127.0.0.1:8080)"),
    cookie: str = typer.Option(None, "--cookie", help="Cookie string"),
    header: str = typer.Option(None, "--header", help="Header string (Key:Value)")
):
    """
    Start a scan against a target.
    """
    console.print(BANNER)
    
    panel = Panel(f"Target: [bold cyan]{url}[/bold cyan]\nParam: [bold cyan]{param}[/bold cyan]\nOutput: [bold cyan]{output}[/bold cyan]", 
                  title="[bold yellow]Scan Configuration[/bold yellow]", border_style="green", box=box.ROUNDED)
    console.print(panel)
    
    proxies = None
    if proxy:
        proxies = {"http://": proxy, "https://": proxy}

    headers = {}
    if header:
        try:
            key, val = header.split(":", 1)
            headers[key.strip()] = val.strip()
        except:
            console.print("[red]Invalid header format[/red]")

    if cookie:
        headers["Cookie"] = cookie

    scanner = Scanner()
    
    # Run async scan in sync context
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    # Wrapper to show progress
    async def run_scan_with_progress():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Scanning...", total=None)
            
            result = await scanner.scan(
                target_url=url,
                file_param=param,
                upload_dir=upload_dir,
                proxies=proxies,
                headers=headers
            )
            progress.update(task, completed=100)
            return result

    result = loop.run_until_complete(run_scan_with_progress())
    
    console.print("\n[bold]Scan completed![/bold]")
    
    stats_table = Table(title="Scan Statistics", box=box.ROUNDED)
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")
    stats_table.add_row("Total Requests", str(result.stats['total_requests']))
    stats_table.add_row("Vulnerabilities Found", str(result.stats['vulns_found']))
    stats_table.add_row("Time Taken", str(result.end_time - result.start_time))
    console.print(stats_table)
    
    if result.findings:
        findings_table = Table(title="Vulnerabilities Detected", box=box.ROUNDED, show_lines=True)
        findings_table.add_column("Risk", style="bold red")
        findings_table.add_column("Name", style="yellow")
        findings_table.add_column("Payload", style="green")
        findings_table.add_column("Proof", style="white")
        
        for finding in result.findings:
            risk_style = "red" if finding.risk_level in ["Critical", "High"] else "yellow"
            findings_table.add_row(
                f"[{risk_style}]{finding.risk_level}[/{risk_style}]",
                finding.name,
                finding.payload,
                finding.proof[:50] + "..."
            )
        console.print(findings_table)
    else:
        console.print(Panel("[green]No vulnerabilities found. Target seems secure against these payloads.[/green]", border_style="green"))

    if output.endswith(".html"):
        generate_html_report(result, output)
    else:
        generate_json_report(result, output)
    
    console.print(f"[bold green]Report saved to {output}[/bold green]")

@app.command()
def gui():
    """
    Launch the Graphical User Interface.
    """
    from ..gui.main_window import run_gui
    run_gui()

if __name__ == "__main__":
    app()
