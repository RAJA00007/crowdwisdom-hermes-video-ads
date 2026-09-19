"""Hermes Ads Manager Agent (Pipeline Orchestrator & Kanban Dispatcher).

Coordinates the multi-agent execution flow across research, ad analysis,
creative concept generation, storyboard generation, and video compilation.
Compatible with Python 3.10.
"""

import logging
from typing import Any, Dict, List, Optional
from rich.console import Console

from config.settings import get_settings
from tools.apify_tool import ApifyMetaAdsTool, DEFAULT_ICP_SEARCH_QUERIES
from tools.llm_tool import HermesLLMClient

logger = logging.getLogger(__name__)
console = Console()


class AdsManagerAgent:
    """Lead campaign orchestrator implementing Hermes-style multi-agent workflow & task dispatching."""

    def __init__(
        self,
        llm_client: Optional[HermesLLMClient] = None,
        apify_tool: Optional[ApifyMetaAdsTool] = None,
    ):
        self.settings = get_settings()
        self.llm = llm_client or HermesLLMClient()
        self.apify_tool = apify_tool or ApifyMetaAdsTool()
        self.name = "AdsManagerAgent"
        self.role = "Lead Campaign Strategist and Multi-Agent Orchestrator"
        self.task_board: List[Dict[str, Any]] = []
        self.init_kanban_board()

    def get_agent_profile(self) -> Dict[str, Any]:
        """Return Hermes profile definition for AdsManager."""
        return {
            "name": self.name,
            "role": self.role,
            "model": self.llm.model,
            "responsibilities": [
                "Decompose campaign requirements into specialized agent tasks",
                "Execute Apify Meta Ad Library multi-query research for ICP angles",
                "Maintain Kanban state across pipeline stages",
                "Enforce quality gates and ensure citation traceability",
                "Coordinate final synthesis of 3 cinematic ad concepts",
            ],
        }

    def init_kanban_board(self) -> List[Dict[str, Any]]:
        """Initialize pipeline task cards in the Hermes Kanban flow."""
        self.task_board = [
            {"id": "TASK-1", "stage": "Meta Ad Research", "assigned_to": "AdsManagerAgent", "status": "pending"},
            {"id": "TASK-2", "stage": "Ad Creative & Angle Analysis", "assigned_to": "AdAnalyzerAgent", "status": "pending"},
            {"id": "TASK-3", "stage": "ICP & Market Research", "assigned_to": "ResearchAgent", "status": "pending"},
            {"id": "TASK-4", "stage": "Proprietary Data Ingestion", "assigned_to": "ResearchAgent", "status": "pending"},
            {"id": "TASK-5", "stage": "Ad Concept Ideation (3 Concepts)", "assigned_to": "CreativeAgent", "status": "pending"},
            {"id": "TASK-6", "stage": "Storyboard Scripting (30-60s)", "assigned_to": "CreativeAgent", "status": "pending"},
            {"id": "TASK-7", "stage": "OpenMontage Video Rendering", "assigned_to": "VideoAgent", "status": "pending"},
        ]
        return self.task_board

    def update_task_status(self, task_id: str, new_status: str, output_ref: Optional[str] = None) -> None:
        """Update task board state."""
        for task in self.task_board:
            if task["id"] == task_id:
                task["status"] = new_status
                if output_ref:
                    task["output_ref"] = output_ref
                break

    def run_ads_research(
        self,
        queries: Optional[List[str]] = None,
        country: str = "US",
        max_ads_per_query: int = 10,
        days_back: int = 30,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """Execute Phase 1: Meta Ad Library Research via Apify with Hermes Kanban logging."""
        search_queries = queries or DEFAULT_ICP_SEARCH_QUERIES

        # Kanban Step 1: SEARCHING
        self.update_task_status("TASK-1", "searching")
        if verbose:
            console.print("\n[bold cyan]ADS MANAGER → SEARCHING[/bold cyan]")
            console.print(f"[dim]Queries targeted for CrowdWisdomTrading ICP ({len(search_queries)} total):[/dim]")
            for q in search_queries:
                console.print(f"  • [yellow]{q}[/yellow]")

        if not self.apify_tool.is_configured():
            msg = "APIFY_API_TOKEN is not configured in .env. Please set APIFY_API_TOKEN to fetch live Meta ads."
            if verbose:
                console.print(f"[bold red]! {msg}[/bold red]")
            self.update_task_status("TASK-1", "blocked", output_ref="Missing APIFY_API_TOKEN")
            return {
                "success": False,
                "error": msg,
                "total_raw": 0,
                "total_normalized": 0,
                "raw_file": None,
                "processed_file": None,
            }

        # Kanban Step 2: COLLECTING
        self.update_task_status("TASK-1", "collecting")
        if verbose:
            console.print("\n[bold cyan]ADS MANAGER → COLLECTING[/bold cyan]")
            console.print(f"[dim]Scraping active Meta ads (last {days_back} days) using Actor '{self.apify_tool.actor_id}'...[/dim]")

        raw_items, summary = self.apify_tool.fetch_multi_query_ads(
            queries=search_queries,
            country=country,
            max_ads_per_query=max_ads_per_query,
            days_back=days_back,
        )

        raw_file = self.apify_tool.save_raw_results(raw_items, summary)
        if verbose:
            console.print(f"  [green]✓ Raw ad records saved:[/green] [white]{raw_file}[/white] ({len(raw_items)} items)")

        # Kanban Step 3: NORMALIZING
        self.update_task_status("TASK-1", "normalizing")
        if verbose:
            console.print("\n[bold cyan]ADS MANAGER → NORMALIZING[/bold cyan]")
            console.print("[dim]Extracting hooks, headlines, descriptions, media URLs, and CTA landing pages...[/dim]")

        normalized_ads, processed_file = self.apify_tool.normalize_and_save_ads(raw_items)

        # Kanban Step 4: COMPLETE
        self.update_task_status("TASK-1", "complete", output_ref=str(processed_file))
        if verbose:
            console.print("\n[bold green]ADS MANAGER → COMPLETE[/bold green]")
            console.print(f"  [green]✓ Processed ad database created:[/green] [bold white]{processed_file}[/bold white]")
            console.print(f"  • Total Normalized Ads: [bold yellow]{len(normalized_ads)}[/bold yellow]")

        return {
            "success": True,
            "total_raw": len(raw_items),
            "total_normalized": len(normalized_ads),
            "raw_file": str(raw_file),
            "processed_file": str(processed_file),
            "summary": summary,
            "ads": normalized_ads,
        }
