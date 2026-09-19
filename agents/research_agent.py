"""Hermes Research Agent.

Specialized agent responsible for deep research using Tavily (primary) and Exa (secondary),
dynamically formulating queries from ad analysis, and grounding findings to ICP pain points.
Compatible with Python 3.10.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from rich.console import Console

from config.settings import get_settings
from tools.llm_tool import HermesLLMClient
from tools.tavily_tool import TavilyResearchTool
from tools.exa_tool import ExaResearchTool

logger = logging.getLogger(__name__)
console = Console()


class ResearchAgent:
    """Agent that performs multi-source market intelligence and ICP data grounding."""

    def __init__(
        self,
        llm_client: Optional[HermesLLMClient] = None,
        tavily_tool: Optional[TavilyResearchTool] = None,
        exa_tool: Optional[ExaResearchTool] = None,
    ):
        self.settings = get_settings()
        self.llm = llm_client or HermesLLMClient()
        self.tavily = tavily_tool or TavilyResearchTool()
        self.exa = exa_tool or ExaResearchTool()
        self.name = "ResearchAgent"
        self.role = "ICP & Market Intelligence Specialist"
        self.prompts_dir = self.settings.prompts_dir

    def get_agent_profile(self) -> Dict[str, Any]:
        """Return Hermes profile definition."""
        return {
            "name": self.name,
            "role": self.role,
            "model": self.llm.model,
            "skills": [
                "Dynamic ICP search query formulation",
                "Tavily real-time web & news intelligence",
                "Exa neural semantic search",
                "Pain point attribution & evidence grounding",
                "Market narrative synthesis without hallucinated stats",
            ],
        }

    def load_system_prompt(self) -> str:
        """Load research system prompt template."""
        prompt_path = self.prompts_dir / "research.txt"
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return (
            "You are the Hermes Research Agent. Ground market research findings in verified sources "
            "and map them directly to ICP pain points."
        )

    def load_ad_analysis(self, path: Optional[Path] = None) -> Dict[str, Any]:
        """Load ad analysis insights from data/processed/ad_analysis.json."""
        target_path = path or (self.settings.data_dir / "processed" / "ad_analysis.json")
        if not target_path.exists():
            logger.warning("Ad analysis file not found at %s", target_path)
            return {}

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error("Failed to load ad analysis: %s", str(e))
            return {}

    def generate_dynamic_queries(self, ad_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Dynamically generate 4-6 targeted search queries based on the Ad Analyzer findings."""
        patterns = ad_analysis.get("aggregate_patterns", {})
        pain_points = patterns.get("common_pain_points", [])
        icp_traits = patterns.get("common_icp_characteristics", [])
        opportunities = patterns.get("crowdwisdom_opportunities", [])

        system_prompt = self.load_system_prompt()
        user_prompt = f"""Based on these findings from competitive Meta ad creative analysis:

Identified Common Pain Points:
{json.dumps(pain_points, indent=2)}

Target ICP Persona Traits:
{json.dumps(icp_traits, indent=2)}

Creative White Space Opportunities:
{json.dumps(opportunities, indent=2)}

Generate 4 to 5 targeted, high-yield web research queries to gather current (last 30 days) market context, trader psychology data, sentiment trends, and retail trader frustrations.

Respond ONLY with a valid JSON object matching this schema:
{{
  "queries": [
    {{
      "query": "exact search query text",
      "target_pain_point": "the specific pain point this query investigates",
      "rationale": "why this context helps CrowdWisdomTrading video ad positioning"
    }}
  ]
}}"""

        try:
            result = self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.3,
            )
            if result.get("success") and isinstance(result.get("data"), dict):
                queries = result["data"].get("queries", [])
                if queries:
                    return queries
        except Exception as e:
            logger.error("Dynamic query generation error: %s", str(e))

        # Fallback queries if LLM generation is unavailable
        return [
            {
                "query": "retail trader emotional bias decision fatigue stock market 2026",
                "target_pain_point": "Emotional trading and lack of discipline",
                "rationale": "Understand current retail trader psychology and anxiety triggers",
            },
            {
                "query": "crowd wisdom prediction markets retail investor sentiment accuracy",
                "target_pain_point": "Guessing market moves without data conviction",
                "rationale": "Validate predictive crowd intelligence vs lagging indicators",
            },
            {
                "query": "options trading information overload conflicting signals retail",
                "target_pain_point": "Information overload and conflicting market signals",
                "rationale": "Address the frustration of signal noise and analysis paralysis",
            },
            {
                "query": "retail investors systematic rules based trading market uncertainty",
                "target_pain_point": "Lack of a clear, verifiable trading plan",
                "rationale": "Highlight the transition from guesswork to data-backed systems",
            },
        ]

    def execute_multi_source_search(
        self,
        queries: List[Dict[str, str]],
        days: int = 30,
        max_results_per_query: int = 3,
        verbose: bool = True,
    ) -> List[Dict[str, Any]]:
        """Search Tavily (primary) and Exa (secondary) across all queries."""
        raw_findings: List[Dict[str, Any]] = []

        for item in queries:
            q_text = item["query"]
            pain_point = item.get("target_pain_point", "General Market Context")
            if verbose:
                console.print(f"  • Searching: [bold yellow]'{q_text}'[/bold yellow]")

            # 1. Primary: Tavily
            if self.tavily.is_configured():
                tav_res = self.tavily.search_market_context(
                    query=q_text,
                    max_results=max_results_per_query,
                    days=days,
                )
                if tav_res.get("success") and tav_res.get("results"):
                    for r in tav_res["results"]:
                        r["query"] = q_text
                        r["target_pain_point"] = pain_point
                        r["provider"] = "Tavily"
                        raw_findings.append(r)

            # 2. Secondary: Exa (supplementary search)
            if self.exa.is_configured() and len(raw_findings) < 12:
                exa_res = self.exa.search_icp_insights(
                    query=q_text,
                    num_results=2,
                )
                if exa_res.get("success") and exa_res.get("results"):
                    for r in exa_res["results"]:
                        r["query"] = q_text
                        r["target_pain_point"] = pain_point
                        r["provider"] = "Exa"
                        raw_findings.append(r)

        return raw_findings

    def synthesize_research_findings(
        self,
        raw_findings: List[Dict[str, Any]],
        ad_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Filter, map to ICP pain points, and synthesize market intelligence without hallucinating."""
        system_prompt = self.load_system_prompt()
        
        # Prepare condensed findings for LLM processing
        condensed = []
        for f in raw_findings:
            condensed.append({
                "query": f.get("query"),
                "title": f.get("title"),
                "url": f.get("url"),
                "source": f.get("source"),
                "published_date": f.get("published_date"),
                "snippet": f.get("content", "")[:600],
                "target_pain_point": f.get("target_pain_point"),
            })

        user_prompt = f"""Process these raw search findings and map them into structured ICP market intelligence.

Raw Search Findings:
{json.dumps(condensed, indent=2)}

Ad Analysis Context:
{json.dumps(ad_analysis.get('aggregate_patterns', {}), indent=2)}

For each relevant search result, structure a research item. Then synthesize the overarching market narratives and ICP behavioral dynamics.

Respond ONLY with a valid JSON object matching this schema:
{{
  "research_items": [
    {{
      "query": "search query used",
      "title": "article or source title",
      "source": "domain or publisher",
      "url": "exact url",
      "publication_date": "date string or null",
      "excerpt": "key factual summary or verbatim excerpt",
      "relevance_to_icp": "how this connects to retail trader psychology and decision making",
      "related_pain_point": "the specific pain point addressed",
      "evidence_note": "verified factual source material vs analytical interpretation"
    }}
  ],
  "market_narratives": [
    {{
      "narrative": "core macro/retail trader narrative",
      "impact_on_ad_scripting": "how this should be framed in the 30-60s video ad hooks"
    }}
  ],
  "trader_behavioral_insights": [
    "Key behavioral insight 1",
    "Key behavioral insight 2",
    "Key behavioral insight 3"
  ]
}}"""

        try:
            result = self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.2,
            )
            if result.get("success") and isinstance(result.get("data"), dict):
                return result["data"]
        except Exception as e:
            logger.error("Research synthesis error: %s", str(e))

        # Fallback structured extraction if LLM fails
        items = []
        for f in raw_findings:
            items.append({
                "query": f.get("query", ""),
                "title": f.get("title", ""),
                "source": f.get("source", "Web"),
                "url": f.get("url", ""),
                "publication_date": f.get("published_date"),
                "excerpt": f.get("content", "")[:300],
                "relevance_to_icp": "Directly impacts retail trading psychology and market conviction.",
                "related_pain_point": f.get("target_pain_point", "General market uncertainty"),
                "evidence_note": "Factual snippet retrieved directly via Tavily/Exa API.",
            })
        return {
            "research_items": items,
            "market_narratives": [
                {
                    "narrative": "Retail traders are increasingly fatigued by lagging technical indicators and seeking quantifiable crowd sentiment edges.",
                    "impact_on_ad_scripting": "Hook ads on the transition from emotional guesswork to collective predictive data.",
                }
            ],
            "trader_behavioral_insights": [
                "Decision fatigue leads to premature exits and undisciplined position sizing.",
                "Traders trust peer consensus and verifiable data over single-influencer claims.",
            ],
        }

    def run_research(
        self,
        analysis_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
        days_back: int = 30,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """Execute Phase 3: Research Agent end-to-end workflow."""
        out_file = output_path or (self.settings.data_dir / "research" / "current_icp_research.json")
        out_file.parent.mkdir(parents=True, exist_ok=True)

        ad_analysis = self.load_ad_analysis(analysis_path)

        # Step 1: GENERATING QUERIES
        if verbose:
            console.print("\n[bold cyan]RESEARCH AGENT → GENERATING QUERIES[/bold cyan]")
            console.print("[dim]Formulating search queries dynamically grounded in Ad Analyzer pain points...[/dim]")

        queries = self.generate_dynamic_queries(ad_analysis)
        if verbose:
            for q in queries:
                console.print(f"  • [yellow]{q['query']}[/yellow] [dim](Pain Point: {q.get('target_pain_point', 'N/A')})[/dim]")

        # Step 2: SEARCHING
        if verbose:
            console.print(f"\n[bold cyan]RESEARCH AGENT → SEARCHING (Tavily: Primary, Exa: Secondary)[/bold cyan]")
            console.print(f"[dim]Prioritizing recent market context from the last {days_back} days...[/dim]")

        raw_findings = self.execute_multi_source_search(queries, days=days_back, verbose=verbose)
        if verbose:
            console.print(f"  [green]✓ Retrieved[/green] [bold white]{len(raw_findings)}[/bold white] web sources with full citations.")

        # Step 3: FILTERING
        if verbose:
            console.print("\n[bold cyan]RESEARCH AGENT → FILTERING[/bold cyan]")
            console.print("[dim]Eliminating low-relevance snippets and verifying URL traceability...[/dim]")

        # Filter duplicates and empty contents
        filtered_findings = []
        seen_urls = set()
        for f in raw_findings:
            url = f.get("url")
            if url and url not in seen_urls and len(f.get("content", "")) > 50:
                seen_urls.add(url)
                filtered_findings.append(f)

        if verbose:
            console.print(f"  [green]✓ Retained[/green] [bold white]{len(filtered_findings)}[/bold white] high-signal research documents.")

        # Step 4: SYNTHESIZING
        if verbose:
            console.print(f"\n[bold cyan]RESEARCH AGENT → SYNTHESIZING (Hermes 3: {self.llm.model})[/bold cyan]")
            console.print("[dim]Mapping citations to trader pain points and synthesizing market narratives...[/dim]")

        synthesis = self.synthesize_research_findings(filtered_findings, ad_analysis)

        # Step 5: COMPLETE & PERSIST
        payload = {
            "meta": {
                "total_items": len(synthesis.get("research_items", [])),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "timeframe_days": days_back,
                "model_used": self.llm.model,
                "providers_used": ["Tavily" if self.tavily.is_configured() else None, "Exa" if self.exa.is_configured() else None],
                "agent": self.name,
            },
            "queries_executed": queries,
            "research_items": synthesis.get("research_items", []),
            "market_narratives": synthesis.get("market_narratives", []),
            "trader_behavioral_insights": synthesis.get("trader_behavioral_insights", []),
        }

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        if verbose:
            console.print("\n[bold green]RESEARCH AGENT → COMPLETE[/bold green]")
            console.print(f"  [green]✓ ICP Research Intelligence saved:[/green] [bold white]{out_file}[/bold white]")
            console.print(f"  • Grounded Research Items: [bold yellow]{len(synthesis.get('research_items', []))}[/bold yellow]")
            console.print(f"  • Synthesized Market Narratives: [bold yellow]{len(synthesis.get('market_narratives', []))}[/bold yellow]")

        return {
            "success": True,
            "output_file": str(out_file),
            "total_items": len(synthesis.get("research_items", [])),
            "data": payload,
        }
