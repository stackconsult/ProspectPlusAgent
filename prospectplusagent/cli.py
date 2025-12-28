"""Command-line interface for ProspectPlusAgent."""

import click
import asyncio
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
import httpx
from typing import Optional
import sys

from prospectplusagent.config import settings

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """ProspectPlusAgent CLI - Manage prospects from the command line."""
    pass


@cli.command()
@click.option('--host', default='localhost', help='Server host')
@click.option('--port', default=8080, help='Server port')
def serve(host: str, port: int):
    """Start the ProspectPlusAgent server."""
    console.print(Panel.fit(
        f"[bold blue]Starting ProspectPlusAgent Server[/bold blue]\n"
        f"Host: {host}\n"
        f"Port: {port}\n"
        f"Environment: {settings.environment}",
        border_style="blue"
    ))
    
    import uvicorn
    from prospectplusagent.main import app
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=settings.debug
    )


@cli.command()
@click.option('--base-url', default='http://localhost:8080', help='API base URL')
def status(base_url: str):
    """Check server status."""
    async def check_status():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/health")
                data = response.json()
                
                console.print(Panel.fit(
                    f"[bold green]✓ Server is healthy[/bold green]\n"
                    f"Version: {data['version']}\n"
                    f"Environment: {data['environment']}",
                    border_style="green"
                ))
        except Exception as e:
            console.print(f"[bold red]✗ Server is not responding:[/bold red] {e}")
    
    asyncio.run(check_status())


@cli.group()
def prospect():
    """Manage prospects."""
    pass


@prospect.command()
@click.option('--base-url', default='http://localhost:8080', help='API base URL')
@click.option('--limit', default=20, help='Number of prospects to list')
@click.option('--status', help='Filter by status')
@click.option('--priority', help='Filter by priority')
def list(base_url: str, limit: int, status: Optional[str], priority: Optional[str]):
    """List all prospects."""
    async def list_prospects():
        try:
            params = {'limit': limit}
            if status:
                params['status'] = status
            if priority:
                params['priority'] = priority
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/api/prospects", params=params)
                prospects = response.json()
                
                if not prospects:
                    console.print("[yellow]No prospects found[/yellow]")
                    return
                
                table = Table(title=f"Prospects ({len(prospects)} total)")
                table.add_column("Company", style="cyan")
                table.add_column("Contact", style="green")
                table.add_column("Email", style="blue")
                table.add_column("Status", style="yellow")
                table.add_column("Priority", style="magenta")
                table.add_column("Score", style="red")
                
                for p in prospects:
                    score = f"{p['score']*100:.0f}%" if p.get('score') else "N/A"
                    table.add_row(
                        p['company_name'],
                        p['contact_name'],
                        p['email'],
                        p['status'],
                        p['priority'],
                        score
                    )
                
                console.print(table)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
    
    asyncio.run(list_prospects())


@prospect.command()
@click.option('--base-url', default='http://localhost:8080', help='API base URL')
@click.option('--company', required=True, help='Company name')
@click.option('--contact', required=True, help='Contact name')
@click.option('--email', required=True, help='Email address')
@click.option('--phone', help='Phone number')
@click.option('--industry', help='Industry')
@click.option('--status', default='new', help='Status')
@click.option('--priority', default='medium', help='Priority')
@click.option('--notes', help='Notes')
def add(base_url: str, company: str, contact: str, email: str, **kwargs):
    """Add a new prospect."""
    async def add_prospect():
        try:
            data = {
                'company_name': company,
                'contact_name': contact,
                'email': email,
                'status': kwargs['status'],
                'priority': kwargs['priority'],
                'tags': []
            }
            
            # Add optional fields
            for key in ['phone', 'industry', 'notes']:
                if kwargs.get(key):
                    data[key] = kwargs[key]
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{base_url}/api/prospects/",
                    json=data
                )
                
                if response.status_code == 201:
                    prospect = response.json()
                    console.print(Panel.fit(
                        f"[bold green]✓ Prospect added successfully![/bold green]\n"
                        f"ID: {prospect['id']}\n"
                        f"Company: {prospect['company_name']}\n"
                        f"Contact: {prospect['contact_name']}",
                        border_style="green"
                    ))
                else:
                    error = response.json()
                    console.print(f"[bold red]Error:[/bold red] {error.get('detail', 'Unknown error')}")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
    
    asyncio.run(add_prospect())


@cli.command()
@click.option('--base-url', default='http://localhost:8080', help='API base URL')
@click.argument('query')
def chat(base_url: str, query: str):
    """Chat with the AI agent."""
    async def send_query():
        try:
            console.print(f"\n[bold blue]You:[/bold blue] {query}\n")
            
            with Progress() as progress:
                task = progress.add_task("[cyan]Agent thinking...", total=None)
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{base_url}/api/agent/chat",
                        json={'query': query}
                    )
                    data = response.json()
                
                progress.stop()
            
            console.print(Panel.fit(
                f"[bold green]Agent:[/bold green]\n\n{data['response']}\n\n"
                f"Confidence: {data['confidence']*100:.0f}%",
                border_style="green"
            ))
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
    
    asyncio.run(send_query())


@cli.command()
@click.option('--base-url', default='http://localhost:8080', help='API base URL')
def analytics(base_url: str):
    """Show analytics overview."""
    async def show_analytics():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/api/analytics/overview")
                data = response.json()
                
                # Create status table
                status_table = Table(title="By Status")
                status_table.add_column("Status", style="cyan")
                status_table.add_column("Count", style="green")
                
                for status, count in data['by_status'].items():
                    status_table.add_row(status, str(count))
                
                # Create priority table
                priority_table = Table(title="By Priority")
                priority_table.add_column("Priority", style="cyan")
                priority_table.add_column("Count", style="green")
                
                for priority, count in data['by_priority'].items():
                    priority_table.add_row(priority, str(count))
                
                # Display summary
                console.print(Panel.fit(
                    f"[bold blue]Analytics Overview[/bold blue]\n\n"
                    f"Total Prospects: {data['total_prospects']}\n"
                    f"Conversion Rate: {data['conversion_rate']*100:.1f}%\n"
                    f"Average Score: {data['avg_score']*100:.0f}%" if data['avg_score'] else "N/A",
                    border_style="blue"
                ))
                
                console.print("\n")
                console.print(status_table)
                console.print("\n")
                console.print(priority_table)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
    
    asyncio.run(show_analytics())


@cli.command()
def init():
    """Initialize the database and configuration."""
    console.print("[bold blue]Initializing ProspectPlusAgent...[/bold blue]")
    
    try:
        from prospectplusagent.core.database import init_db
        init_db()
        console.print("[bold green]✓ Database initialized successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]✗ Error initializing database:[/bold red] {e}")
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    import os
    if not os.path.exists('.env'):
        console.print("[yellow]Creating .env file from template...[/yellow]")
        try:
            import shutil
            shutil.copy('.env.example', '.env')
            console.print("[bold green]✓ .env file created! Please update it with your API keys.[/bold green]")
        except Exception as e:
            console.print(f"[yellow]Warning: Could not create .env file: {e}[/yellow]")
    
    console.print("\n[bold green]✓ Initialization complete![/bold green]")
    console.print("\nNext steps:")
    console.print("1. Update your .env file with API keys")
    console.print("2. Run 'prospectplus serve' to start the server")
    console.print("3. Visit http://localhost:8080 in your browser")


if __name__ == '__main__':
    cli()
