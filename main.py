"""CrowdWisdomTrading Video Ads Agent - Main CLI Entrypoint.

Multi-agent system built on the Hermes agent framework / OpenRouter.
Compatible with Python 3.10.
"""

import sys
import os
import argparse
from typing import Any, Dict, List, Optional

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config.settings import get_settings
from tools.llm_tool import HermesLLMClient
from workflows.marketing_pipeline import MarketingPipeline

console = Console(force_terminal=True)


def display_banner() -> None:
    """Display application header banner."""
    console.print(
        Panel.fit(
            "[bold cyan]CrowdWisdomTrading Video Ads Agent[/bold cyan]\n"
            "[dim]Hermes Multi-Agent Framework • Meta Ad Intelligence • OpenMontage Production[/dim]\n"
            f"[dim green]Python {sys.version.split()[0]} Environment[/dim green]",
            border_style="cyan",
        )
    )


def show_environment_status() -> None:
    """Display current environment variables and API readiness."""
    settings = get_settings()
    status = settings.check_api_keys_status()

    table = Table(title="Environment & API Configuration Status", show_header=True, header_style="bold magenta")
    table.add_column("Service / API Key", style="cyan")
    table.add_column("Required For", style="white")
    table.add_column("Status", style="bold")

    descriptions = {
        "OPENROUTER_API_KEY": "Hermes LLM (NousResearch Hermes-3) Agent Reasoning",
        "APIFY_API_TOKEN": "Scraping Last 30 Days Meta Ads Library",
        "TAVILY_API_KEY": "ICP Market Trends & Competitor Web Intelligence",
        "EXA_API_KEY": "Neural Semantic Search & Community Discussion Discovery",
    }

    for key, is_set in status.items():
        state_str = "[green][OK] Configured[/green]" if is_set else "[yellow][!] Missing (Set in .env)[/yellow]"
        table.add_row(key, descriptions.get(key, "General Integration"), state_str)

    console.print(table)
    console.print(f"[dim]Hermes Model:[/dim] [bold yellow]{settings.hermes_model}[/bold yellow]")
    console.print(f"[dim]Base URL:[/dim] [bold yellow]{settings.openrouter_base_url}[/bold yellow]")


def run_connectivity_test() -> None:
    """Perform a live Hermes LLM / OpenRouter connectivity test."""
    console.print("\n[bold cyan]Initiating Hermes / OpenRouter Connectivity Check...[/bold cyan]")
    client = HermesLLMClient()
    result = client.test_connection()

    if result.get("success"):
        console.print(
            Panel(
                f"[bold green][SUCCESS] Hermes LLM Connection Verified[/bold green]\n\n"
                f"- [bold]Model:[/bold] {result.get('model')}\n"
                f"- [bold]Endpoint:[/bold] {result.get('endpoint')}\n"
                f"- [bold]Response:[/bold] '{result.get('response')}'\n"
                f"- [bold]Tokens Used:[/bold] {result.get('usage', {})}",
                title="Hermes Diagnostic Passed",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                f"[bold yellow][PENDING CONFIG] Hermes LLM Not Connected[/bold yellow]\n\n"
                f"- [bold]Reason:[/bold] {result.get('error')}\n"
                f"- [bold]Target Model:[/bold] {result.get('model')}\n"
                f"- [bold]Base URL:[/bold] {result.get('endpoint')}\n\n"
                f"[italic cyan]To activate: Copy .env.example to .env and set OPENROUTER_API_KEY[/italic cyan]",
                title="Configuration Status",
                border_style="yellow",
            )
        )


def show_pipeline_architecture() -> None:
    """Show the multi-agent Kanban architecture and pipeline layout."""
    pipeline = MarketingPipeline()
    summary = pipeline.get_pipeline_summary()

    table = Table(title="Hermes Multi-Agent Roster & Profiles", show_header=True, header_style="bold blue")
    table.add_column("Agent Name", style="bold cyan")
    table.add_column("Role", style="white")
    table.add_column("Capabilities / Specialization", style="dim")

    for agent in summary["agents"]:
        skills_str = ", ".join(agent.get("skills", agent.get("responsibilities", [])))
        table.add_row(agent["name"], agent["role"], skills_str)

    console.print(table)

    kanban_table = Table(title="Pipeline Kanban Flow & Stages", show_header=True, header_style="bold green")
    kanban_table.add_column("Task ID", style="bold")
    kanban_table.add_column("Pipeline Stage", style="white")
    kanban_table.add_column("Assigned Agent", style="cyan")
    kanban_table.add_column("Status", style="yellow")

    for task in summary["kanban_tasks"]:
        kanban_table.add_row(task["id"], task["stage"], task["assigned_to"], task["status"])

    console.print(kanban_table)


def run_stage_ads(max_ads: int = 5) -> None:
    """Execute Phase 1: Ads Manager Agent Meta Ad Research."""
    from agents.ads_manager import AdsManagerAgent
    
    console.print(
        Panel(
            "[bold cyan]Phase 1: Ads Manager Agent (Apify Meta Ad Library Scraper)[/bold cyan]\n"
            "[dim]Targeting CrowdWisdomTrading ICP keywords across active 30-day Meta ad campaigns[/dim]",
            border_style="cyan",
        )
    )
    manager = AdsManagerAgent()
    result = manager.run_ads_research(max_ads_per_query=max_ads)

    if result.get("success"):
        table = Table(title="Recent Meta Ad Intelligence (Sample Extracted)", show_header=True, header_style="bold green")
        table.add_column("Advertiser", style="bold cyan")
        table.add_column("Headline", style="white")
        table.add_column("Query", style="yellow")
        table.add_column("Creative Type", style="magenta")
        table.add_column("Source", style="dim")

        for ad in result.get("ads", [])[:8]:
            table.add_row(
                ad.get("advertiser", "")[:25],
                ad.get("headline", "")[:35],
                ad.get("search_query", "")[:20],
                ad.get("creative_type", ""),
                ad.get("source_url", "")[:30] + "..." if ad.get("source_url") else "N/A",
            )
        console.print(table)


def run_stage_analyze(max_ads: int = 5) -> None:
    """Execute Phase 2: Ad Analyzer Agent (Creative Dissection & Pattern Synthesis)."""
    from agents.ad_analyzer import AdAnalyzerAgent

    console.print(
        Panel(
            "[bold cyan]Phase 2: Ad Analyzer Agent (Hermes 3 Creative Dissector)[/bold cyan]\n"
            "[dim]Extracting hooks, angles, emotional triggers, CTAs, and synthesizing CrowdWisdom opportunities[/dim]",
            border_style="cyan",
        )
    )
    analyzer = AdAnalyzerAgent()
    result = analyzer.run_analysis(max_ads_to_analyze=max_ads)

    if result.get("success"):
        data = result.get("data", {})
        individual = data.get("individual_ad_analyses", [])
        aggregate = data.get("aggregate_patterns", {})

        if individual:
            table = Table(title="Dissected Meta Ad Hooks & Angles (Sample)", show_header=True, header_style="bold magenta")
            table.add_column("Advertiser", style="bold cyan")
            table.add_column("Opening Hook (0-3s)", style="white")
            table.add_column("Acute Pain Point", style="yellow")
            table.add_column("Marketing Angle", style="green")
            table.add_column("CTA", style="bold red")

            for item in individual[:5]:
                table.add_row(
                    item.get("advertiser", "")[:20],
                    item.get("hook", "")[:40],
                    item.get("pain_point", "")[:35],
                    item.get("marketing_angle", "")[:25],
                    item.get("CTA", "")[:20],
                )
            console.print(table)

        if aggregate:
            opps = aggregate.get("crowdwisdom_opportunities", [])
            if opps:
                opp_text = "\n\n".join(f"• [bold yellow]{opp}[/bold yellow]" for opp in opps)
                console.print(
                    Panel(
                        opp_text,
                        title="CrowdWisdomTrading Strategic White Space & Creative Opportunities",
                        border_style="green",
                    )
                )


def run_stage_research() -> None:
    """Execute Phase 3: Research Agent (Tavily/Exa Market & ICP Context Intelligence)."""
    from agents.research_agent import ResearchAgent

    console.print(
        Panel(
            "[bold cyan]Phase 3: Research Agent (Tavily & Exa Market Intelligence)[/bold cyan]\n"
            "[dim]Grounding ICP pain points, trader psychology, and market narratives in 30-day verified sources[/dim]",
            border_style="cyan",
        )
    )
    researcher = ResearchAgent()
    result = researcher.run_research()

    if result.get("success"):
        data = result.get("data", {})
        items = data.get("research_items", [])
        narratives = data.get("market_narratives", [])

        if items:
            table = Table(title="Grounded ICP Market Research Findings (Sample)", show_header=True, header_style="bold blue")
            table.add_column("Title / Source", style="bold cyan")
            table.add_column("Related Pain Point", style="yellow")
            table.add_column("Relevance to ICP", style="white")
            table.add_column("URL", style="dim")

            for it in items[:5]:
                title_src = f"{it.get('title', '')[:30]}\n[dim]({it.get('source', '')})[/dim]"
                table.add_row(
                    title_src,
                    it.get("related_pain_point", "")[:35],
                    it.get("relevance_to_icp", "")[:45],
                    it.get("url", "")[:35] + "..." if it.get("url") else "N/A",
                )
            console.print(table)

        if narratives:
            narrative_text = "\n\n".join(
                f"• [bold white]{n.get('narrative')}[/bold white]\n  [dim green]↳ Video Ad Hook Angle:[/dim green] [italic yellow]{n.get('impact_on_ad_scripting')}[/italic yellow]"
                for n in narratives
            )
            console.print(
                Panel(
                    narrative_text,
                    title="Key Market Narratives for Video Ad Framing",
                    border_style="green",
                )
            )


def run_stage_creative() -> None:
    """Execute Phase 5: Proprietary Data Ingestion + Creative Intelligence + Storyboard Generation."""
    from workflows.marketing_pipeline import MarketingPipeline

    console.print(
        Panel(
            "[bold cyan]Phase 5: Proprietary Data Ingestion + Creative Intelligence + Storyboard Generation[/bold cyan]\n"
            "[dim]Transforming market research and CrowdWisdom proprietary data into THREE 30-60s cinematic ad concepts[/dim]",
            border_style="cyan",
        )
    )
    pipeline = MarketingPipeline()
    result = pipeline.execute_stage_creative()

    if result.get("success"):
        storyboards = result.get("storyboards", {}).get("storyboards", [])
        validation = result.get("storyboards", {}).get("validation", {})

        # Concept Overview Table
        table = Table(title="Generated 30–60s Cinematic Ad Production Storyboards", show_header=True, header_style="bold magenta")
        table.add_column("Concept ID", style="bold cyan")
        table.add_column("Concept Title", style="bold white")
        table.add_column("Cinematic Genre", style="yellow")
        table.add_column("Duration", style="green")
        table.add_column("Scenes", style="magenta")
        table.add_column("Proprietary Data Anchored", style="cyan")
        table.add_column("Validation", style="bold green")

        for sb in storyboards:
            # find proprietary data scene
            prop_field = "None"
            scenes = sb.get("scenes", sb.get("shots", []))
            for scene in scenes:
                if scene.get("data_field"):
                    prop_field = f"{scene.get('data_field').split('.')[-1]} ({scene.get('data_value', '')})"
                    break

            cid = sb.get("concept_id", "")
            is_valid = True
            for cr in validation.get("concept_results", []):
                if cr.get("concept_id") == cid:
                    is_valid = cr.get("valid", True)
                    break

            valid_str = "[green]✓ Passed (0 errors)[/green]" if is_valid else "[red]✗ Issues Detected[/red]"

            table.add_row(
                cid,
                sb.get("title", ""),
                sb.get("genre", ""),
                f"{sb.get('total_duration_sec', 0)}s",
                f"{len(scenes)} scenes",
                prop_field,
                valid_str,
            )
        console.print(table)

        # Highlight Visual Hooks
        hooks_text = ""
        for sb in storyboards:
            cid = sb.get("concept_id", "").upper()
            title = sb.get("title", "")
            meta = sb.get("concept_metadata", {})
            hook_vis = meta.get("hook_visual") or meta.get("visual_hook") or sb.get("scenes", [{}])[0].get("visual", "")
            hook_cam = meta.get("hook_camera", "35mm anamorphic")
            hook_light = meta.get("hook_lighting", "Low-key chiaroscuro")
            hook_reason = meta.get("hook_reason", "Immediate high-tension scroll stopper")
            vo = sb.get("scenes", [{}])[0].get("voiceover", "")

            hooks_text += (
                f"[bold yellow]• [{cid}] {title}[/bold yellow]\n"
                f"  [dim white]Hook Visual (0-3s):[/dim white] {hook_vis}\n"
                f"  [dim cyan]Camera & Lighting:[/dim cyan] {hook_cam} | {hook_light}\n"
                f"  [dim magenta]Hook Strategic Reason:[/dim magenta] {hook_reason}\n"
                f"  [dim green]↳ Opening Voiceover:[/dim green] [italic]'{vo}'[/italic]\n\n"
            )

        console.print(
            Panel(
                hooks_text.strip(),
                title="Cinematic Visual Hooks (First 1–3 Seconds — High-Impact & Sound-Off Ready)",
                border_style="green",
            )
        )


def run_stage_video(concept_idx: Optional[int] = None, all_concepts: bool = False, test_shot: bool = False) -> None:
    """Execute Phase 6: Video Agent Cinematic Video Production."""
    from workflows.marketing_pipeline import MarketingPipeline

    console.print(
        Panel(
            "[bold cyan]Phase 6: Video Agent Cinematic Video Production[/bold cyan]\n"
            "[dim]Turning Phase 5 storyboards into 30–60s 1080x1920 cinematic MP4 advertisements[/dim]",
            border_style="cyan",
        )
    )
    pipeline = MarketingPipeline()
    result = pipeline.execute_stage_video(
        concept_idx=concept_idx,
        all_concepts=all_concepts,
        test_shot=test_shot,
    )


def main() -> None:
    """Main entrypoint router."""
    parser = argparse.ArgumentParser(
        description="CrowdWisdomTrading Video Ads Agent (Hermes Framework)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--test-hermes",
        "--test-llm",
        action="store_true",
        dest="test_hermes",
        help="Run live connectivity diagnostic against OpenRouter / Hermes model",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Display environment variables and configured API status",
    )
    parser.add_argument(
        "--pipeline",
        action="store_true",
        help="Display multi-agent Kanban architecture and workflow roster",
    )
    parser.add_argument(
        "--stage",
        type=str,
        choices=["ads", "analyze", "analysis", "research", "script", "creative", "video", "qa", "all"],
        help="Execute a specific pipeline stage ('--stage ads', '--stage research', '--stage script', '--stage video', '--stage qa')",
    )
    parser.add_argument(
        "--concept",
        type=int,
        choices=[1, 2, 3],
        help="Target concept ID for video production (1, 2, or 3)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="all_concepts",
        help="Produce all 3 video ad concepts",
    )
    parser.add_argument(
        "--test-shot",
        action="store_true",
        help="Execute Section 19 single-shot test verification before full run",
    )
    parser.add_argument(
        "--max-ads",
        type=int,
        default=5,
        help="Max ads to process per query or analysis batch (default: 5)",
    )

    args = parser.parse_args()
    display_banner()

    if args.stage == "video":
        run_stage_video(
            concept_idx=args.concept,
            all_concepts=args.all_concepts or (args.concept is None and not args.test_shot),
            test_shot=args.test_shot,
        )
    elif args.stage in ("script", "creative"):
        run_stage_creative()
    elif args.stage == "qa":
        import subprocess
        res = subprocess.run([sys.executable, "tests/test_phase14_production.py"])
        sys.exit(res.returncode)
    elif args.stage == "research":
        run_stage_research()
    elif args.stage in ("analyze", "analysis"):
        run_stage_analyze(max_ads=args.max_ads)
    elif args.stage == "ads":
        run_stage_ads(max_ads=args.max_ads)
    elif args.test_hermes:
        run_connectivity_test()
    elif args.status:
        show_environment_status()
    elif args.pipeline:
        show_pipeline_architecture()
    else:
        # Default run shows status and pipeline architecture
        show_environment_status()
        console.print()
        show_pipeline_architecture()
        console.print()
        run_connectivity_test()


if __name__ == "__main__":
    main()
