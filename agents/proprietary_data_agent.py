"""Hermes Proprietary Data Agent.

Responsible for discovering, ingesting, parsing, and normalizing CrowdWisdomTrading's
proprietary dataset assets into a verifiable summary with provenance tracking.
Compatible with Python 3.10.
"""

from pathlib import Path
from typing import Any, Dict, Optional
from rich.console import Console

from config.settings import get_settings
from tools.proprietary_data_tool import ProprietaryDataTool

console = Console()


class ProprietaryDataAgent:
    """Agent that ingests and indexes proprietary CrowdWisdom market intelligence."""

    def __init__(self, data_tool: Optional[ProprietaryDataTool] = None):
        self.settings = get_settings()
        self.tool = data_tool or ProprietaryDataTool()
        self.name = "ProprietaryDataAgent"
        self.role = "CrowdWisdom Proprietary Data Specialist"

    def get_agent_profile(self) -> Dict[str, Any]:
        """Return Hermes profile definition."""
        return {
            "name": self.name,
            "role": self.role,
            "skills": [
                "Multi-format dataset discovery and ingestion (JSON, CSV, tabular)",
                "Factual data vs statistical inference boundary enforcement",
                "CrowdWisdom alpha metrics extraction (1.48M+ points, 68.4% win rate)",
                "Provenance tracking and verified field tagging",
            ],
        }

    def run_ingestion(self, verbose: bool = True) -> Dict[str, Any]:
        """Execute proprietary data ingestion and normalization workflow."""
        if verbose:
            console.print("\n[bold cyan]PROPRIETARY DATA AGENT → INGESTING[/bold cyan]")
            console.print("[dim]Scanning data/proprietary for CrowdWisdomTrading ground-truth datasets...[/dim]")

        files = self.tool.discover_files()
        if verbose:
            for f in files:
                console.print(f"  • Ingesting: [bold yellow]{f.name}[/bold yellow] ({f.stat().st_size} bytes)")

        if verbose:
            console.print("\n[bold cyan]PROPRIETARY DATA AGENT → NORMALIZING[/bold cyan]")
            console.print("[dim]Extracting crowd sentiment shift lead times, accuracy benchmarks, and signal factors...[/dim]")

        summary_payload, summary_path = self.tool.extract_and_summarize()

        if verbose:
            stats = summary_payload.get("calculated_statistics", {})
            raw = summary_payload.get("raw_factual_data", {})
            console.print("\n[bold green]PROPRIETARY DATA AGENT → COMPLETE[/bold green]")
            console.print(f"  [green]✓ Summary saved:[/green] [bold white]{summary_path}[/bold white]")
            console.print(f"  • Aggregated Trader Inputs: [bold yellow]{raw.get('total_trader_inputs_indexed', 0):,}[/bold yellow]")
            console.print(f"  • Crowd Consensus Accuracy: [bold yellow]{stats.get('crowd_consensus_directional_accuracy_pct')}%[/bold yellow] (vs Traditional Retail: {stats.get('traditional_retail_accuracy_benchmark_pct')}%)")
            console.print(f"  • Early Warning Lead Time: [bold yellow]{raw.get('sentiment_shift_lead_time_hours')} hours[/bold yellow]")

        return {
            "success": True,
            "summary_path": str(summary_path),
            "summary": summary_payload,
        }
