import argparse
import requests
import subprocess
import zipfile
import os
import sys
import shutil
from pathlib import Path

# Visual imports
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from rich.table import Table
from rich.panel import Panel

# Config import
try:
    from . import config
except ImportError:
    # Fallback if run directly without package context (for dev/debugging)
    import config

console = Console()
INSTALL_DIR = Path(".python")
ZIP_FILE = Path("python_embed.zip")

def download_file(url: str, dest_path: Path, description: str):
    """Downloads a file with a visual progress bar."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TransferSpeedColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task(description, total=total_size)
        
        with open(dest_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                progress.update(task, advance=len(chunk))

def extract_zip(zip_path: Path, extract_to: Path):
    if extract_to.exists():
        console.print(f"[yellow]Warning: Directory {extract_to} already exists and will be cleaned.[/yellow]")
        shutil.rmtree(extract_to) # Clean previous installation
    
    extract_to.mkdir(parents=True)

    with console.status(f"[bold green]Extracting files to {extract_to}...") as status:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        console.log(f"[green]✓[/green] Extraction complete.")

def configure_pth_file(install_dir: Path):
    pth_files = list(install_dir.glob("*._pth"))
    
    if not pth_files:
        console.print("[red]Error: ._pth file not found.[/red]")
        return

    pth_file = pth_files[0]
    
    # Enabling site-packages, scripts, and import site
    new_content = (
        f"{pth_file.stem.replace('._pth', '')}.zip\n"
        ".\n"
        "Scripts\n"
        "Lib\\site-packages\n"
        "import site\n"
    )
    
    with open(pth_file, "w") as f:
        f.write(new_content)
    
    console.log(f"[green]✓[/green] File {pth_file.name} configured.")

def install_pip_and_tools(install_dir: Path):
    pip_script = install_dir / "get-pip.py"
    python_exe = install_dir / "python.exe"

    if not pip_script.exists():
        download_file(config.GET_PIP_URL, pip_script, "Downloading get-pip.py")

    # Install PIP
    cmd_pip = [str(python_exe), str(pip_script), "--no-warn-script-location"]
    with console.status("[bold yellow]Installing PIP...") as status:
        subprocess.run(cmd_pip, capture_output=True, text=True, check=True)
        console.log(f"[green]✓[/green] PIP installed!")

    # Install Setuptools and Wheel
    cmd_tools = [
        str(python_exe), "-m", "pip", "install", 
        "--upgrade", "setuptools", "wheel", "--no-warn-script-location"
    ]
    with console.status("[bold yellow]Installing Setuptools and Wheel...") as status:
        try:
            subprocess.run(cmd_tools, capture_output=True, text=True, check=True)
            console.log(f"[green]✓[/green] Setuptools and Wheel installed!")
        except subprocess.CalledProcessError as e:
            console.log(f"[red]! Warning: Error installing tools: {e}. Python should still work.[/red]")
            console.log(f"Stderr: {e.stderr}")

    if pip_script.exists():
        os.remove(pip_script)

def list_versions():
    """Displays a table with available versions in config.py"""
    table = Table(title="Available Python Versions")
    table.add_column("Version", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    # Filter duplicates
    seen_urls = set()
    for alias, data in config.AVAILABLE_VERSIONS.items():
        if data['url'] not in seen_urls:
            table.add_row(alias, data['description'])
            seen_urls.add(data['url'])
        elif alias == "latest":
             table.add_row(f"-> {data['version']}", "Latest Version")

    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Automated Portable Python Installer")
    
    parser.add_argument("version", nargs="?", help="Python version to install (e.g., 3.12, latest)")
    parser.add_argument("-l", "--list", action="store_true", help="List available versions")

    args = parser.parse_args()

    console.rule("[bold blue]Python Portable Manager[/bold blue]")

    if args.list:
        list_versions()
        return

    if not args.version:
        console.print("[yellow]No version specified.[/yellow]")
        console.print("Use [cyan]pyportable --list[/cyan] to see options.")
        console.print("Or use [cyan]pyportable latest[/cyan] to install.")
        return

    if args.version not in config.AVAILABLE_VERSIONS:
        console.print(f"[bold red]Error:[/bold red] Version '{args.version}' not found in configuration.")
        console.print("Use the [cyan]--list[/cyan] flag to see available versions.")
        return

    # Start Installation
    selected_version = config.AVAILABLE_VERSIONS[args.version]
    url = selected_version['url']
    full_ver = selected_version['version']

    try:
        console.print(Panel(f"Installing: [bold green]Python {full_ver}[/bold green]\nAlias: {args.version}", expand=False))

        if not ZIP_FILE.exists():
            download_file(url, ZIP_FILE, f"Downloading Python {full_ver}")
        
        extract_zip(ZIP_FILE, INSTALL_DIR)
        configure_pth_file(INSTALL_DIR)
        install_pip_and_tools(INSTALL_DIR)

        if ZIP_FILE.exists():
            os.remove(ZIP_FILE)

        console.rule("[bold green]Installation Finished![/bold green]")
        console.print(f"\nLocation: [bold]{INSTALL_DIR.absolute()}[/bold]")
        console.print("To activate, run commands in the scripts folder or call python.exe directly.")

    except Exception as e:
        console.print(f"\n[bold red]FATAL ERROR:[/bold red] {e}")
        # Clean up in case of critical error
        if ZIP_FILE.exists(): os.remove(ZIP_FILE)

# Remove the if __name__ == "__main__": block since this is now a library module
