"""
Main Application Entry Point
Provides CLI and API interfaces for the Research Assistant
"""
from dotenv import load_dotenv
load_dotenv()  # Must be before importing agents
import os
import sys
import argparse
import json
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown
from loguru import logger
from typing import Dict, List, Optional


from orchestrator import ResearchOrchestrator, quick_research
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank


console = Console()


def setup_environment():
    """Setup environment and check for required API keys"""
    required_keys = ["ANTHROPIC_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        console.print(f"[red]Error: Missing required API keys: {', '.join(missing_keys)}[/red]")
        console.print("\nPlease set them in your environment or .env file:")
        for key in missing_keys:
            console.print(f"  export {key}='your-key-here'")
        sys.exit(1)


def cli_interface():
    """Command-line interface for the research assistant"""
    parser = argparse.ArgumentParser(
        description="AI Research Assistant - Conduct deep research on any topic",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Research question or topic"
    )
    
    parser.add_argument(
        "--format",
        choices=["report", "article", "summary", "presentation"],
        default="report",
        help="Output format (default: report)"
    )
    
    parser.add_argument(
        "--session-id",
        help="Resume a specific session"
    )
    
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Run evaluation on the results"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show memory bank statistics"
    )
    
    parser.add_argument(
        "--related",
        help="Find related past research for a query"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    
    # Setup
    setup_environment()
    
    # Handle different modes
    if args.stats:
        show_statistics()
        return
    
    if args.related:
        show_related_research(args.related)
        return
    
    if args.interactive or not args.query:
        interactive_mode()
        return
    
    # Standard research mode
    run_research(args.query, args.format, args.session_id, args.evaluate)


def run_research(
    query: str,
    output_format: str,
    session_id: Optional[str],
    evaluate: bool
):
    """Execute a research session"""
    console.print(Panel.fit(
        f"[bold cyan]AI Research Assistant[/bold cyan]\n\n"
        f"Query: [yellow]{query}[/yellow]\n"
        f"Format: [green]{output_format}[/green]",
        border_style="cyan"
    ))
    
    orchestrator = ResearchOrchestrator()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Researching...", total=None)
        
        try:
            # Run research
            results = orchestrator.conduct_research(
                query,
                output_format=output_format,
                session_id=session_id
            )
            
            progress.update(task, description="[green]Research complete!")
            
            # Display results
            display_results(results)
            
            # Save results
            save_results(results)
            
            # Evaluate if requested
            if evaluate:
                console.print("\n[cyan]Running evaluation...[/cyan]")
                evaluator = ResearchEvaluator()
                metrics = evaluator.evaluate_research(query, results)
                display_evaluation(metrics)
            
        except Exception as e:
            progress.update(task, description="[red]Research failed!")
            console.print(f"[red]Error: {str(e)}[/red]")
            logger.exception("Research failed")
            sys.exit(1)


def display_results(results: Dict):
    """Display research results in a formatted way"""
    console.print("\n" + "="*80 + "\n")
    
    # Session info
    console.print(f"[bold]Session ID:[/bold] {results['session_id']}")
    console.print(f"[bold]Query:[/bold] {results['query']}\n")
    
    # Research summary
    summary = results['research_summary']
    console.print(Panel(
        f"[bold]Research Summary[/bold]\n\n"
        f"Sources found: {summary['total_sources']}\n"
        f"Iterations: {summary['iterations']}",
        border_style="blue"
    ))
    
    # Validation
    validation = results['validation']
    console.print(Panel(
        f"[bold]Validation[/bold]\n\n"
        f"Status: {validation.get('validation_status', 'N/A')}\n"
        f"Confidence: {validation.get('confidence_score', 'N/A')}%",
        border_style="green" if validation.get('validation_status') == 'validated' else "yellow"
    ))
    
    # Final content
    content = results['final_content']['content']
    console.print("\n[bold cyan]Generated Content:[/bold cyan]\n")
    console.print(Markdown(content))
    
    # Citations
    if results['final_content'].get('citations'):
        console.print("\n[bold]References:[/bold]")
        for i, citation in enumerate(results['final_content']['citations'], 1):
            console.print(f"{i}. {citation}")


def display_evaluation(metrics):
    """Display evaluation metrics"""
    console.print("\n" + "="*80 + "\n")
    console.print("[bold cyan]Evaluation Metrics[/bold cyan]\n")
    
    metrics_dict = metrics.to_dict()
    
    for metric, score in metrics_dict.items():
        # Color code based on score
        if score >= 80:
            color = "green"
        elif score >= 60:
            color = "yellow"
        else:
            color = "red"
        
        bar_length = int(score / 2)  # Scale to 50 chars max
        bar = "█" * bar_length + "░" * (50 - bar_length)
        
        console.print(f"{metric.capitalize():15} [{color}]{bar}[/{color}] {score:.1f}")
    
    console.print(f"\n[bold]Overall Score: {metrics.overall_score:.1f}/100[/bold]")


def save_results(results: Dict, output_dir: str = "outputs"):
    """Save results to file"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    session_id = results['session_id']
    
    # Save full JSON
    json_path = output_path / f"{session_id}.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save content as markdown
    md_path = output_path / f"{session_id}.md"
    with open(md_path, 'w') as f:
        f.write(f"# {results['query']}\n\n")
        f.write(results['final_content']['content'])
        f.write("\n\n## References\n\n")
        for i, citation in enumerate(results['final_content'].get('citations', []), 1):
            f.write(f"{i}. {citation}\n")
    
    console.print(f"\n[green]Results saved to:[/green]")
    console.print(f"  - {json_path}")
    console.print(f"  - {md_path}")


def show_statistics():
    """Display memory bank statistics"""
    memory_bank = MemoryBank()
    stats = memory_bank.get_statistics()
    
    console.print(Panel(
        f"[bold]Memory Bank Statistics[/bold]\n\n"
        f"Total memories: {stats['total_memories']}\n"
        f"Average importance: {stats['avg_importance']:.2f}\n"
        f"Completed sessions: {stats['completed_sessions']}\n"
        f"Total sources: {stats['total_sources']}",
        border_style="cyan"
    ))


def show_related_research(query: str):
    """Show related past research"""
    memory_bank = MemoryBank()
    related = memory_bank.get_related_research(query, limit=5)
    
    if not related:
        console.print("[yellow]No related research found[/yellow]")
        return
    
    console.print(f"\n[bold cyan]Related Research for:[/bold cyan] {query}\n")
    
    for i, session in enumerate(related, 1):
        console.print(f"{i}. [bold]{session['query']}[/bold]")
        console.print(f"   Session: {session['id']}")
        console.print(f"   Sources: {session.get('sources_count', 0)}\n")


def interactive_mode():
    """Interactive CLI mode"""
    console.print(Panel.fit(
        "[bold cyan]AI Research Assistant[/bold cyan]\n"
        "Interactive Mode\n\n"
        "Type 'help' for commands, 'quit' to exit",
        border_style="cyan"
    ))
    
    orchestrator = ResearchOrchestrator()
    
    while True:
        try:
            query = console.input("\n[bold cyan]Research query:[/bold cyan] ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if query.lower() == 'help':
                show_help()
                continue
            
            if query.lower() == 'stats':
                show_statistics()
                continue
            
            # Ask for format
            format_input = console.input(
                "[cyan]Format (report/article/summary/presentation) [report]:[/cyan] "
            ).strip().lower() or "report"
            
            if format_input not in ["report", "article", "summary", "presentation"]:
                format_input = "report"
            
            # Run research
            run_research(query, format_input, None, False)
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'quit' to exit.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


def show_help():
    """Show help information"""
    help_text = """
[bold cyan]Available Commands:[/bold cyan]

  [yellow]<query>[/yellow]           - Enter a research query
  [yellow]stats[/yellow]             - Show memory bank statistics
  [yellow]help[/yellow]              - Show this help message
  [yellow]quit[/yellow]              - Exit the program

[bold cyan]Examples:[/bold cyan]

  "What are the impacts of AI on healthcare?"
  "Explain quantum computing for beginners"
  "Compare renewable energy sources"
"""
    console.print(help_text)


if __name__ == "__main__":
    # Load environment variables from .env if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    cli_interface()
