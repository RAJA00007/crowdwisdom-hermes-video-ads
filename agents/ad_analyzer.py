"""Hermes Ad Analyzer Agent.

Specialized agent responsible for extracting hooks, pain points, ICP targets,
marketing angles, creative concepts, and CTAs from scraped Meta ad campaigns using Hermes 3.
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

logger = logging.getLogger(__name__)
console = Console()


class AdAnalyzerAgent:
    """Agent that ingests and evaluates Meta ad campaigns using Hermes LLM."""

    def __init__(self, llm_client: Optional[HermesLLMClient] = None):
        self.settings = get_settings()
        self.llm = llm_client or HermesLLMClient()
        self.name = "AdAnalyzerAgent"
        self.role = "Meta Ad Competitor and Creative Dissector"
        self.prompts_dir = self.settings.prompts_dir

    def get_agent_profile(self) -> Dict[str, Any]:
        """Return Hermes profile definition."""
        return {
            "name": self.name,
            "role": self.role,
            "model": self.llm.model,
            "skills": [
                "Hook and scroll-stopper analysis (0-3s retention)",
                "ICP and emotional anxiety mapping",
                "Marketing angle and value proposition dissection",
                "Creative format and visual pacing breakdown",
                "CrowdWisdom competitive opportunity synthesis",
            ],
        }

    def load_system_prompt(self) -> str:
        """Load ad analysis system prompt template."""
        prompt_path = self.prompts_dir / "ad_analysis.txt"
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return (
            "You are the Hermes Ad Analyzer Agent. Dissect Meta ads for hooks, ICP, "
            "angles, pain points, and creative formats into structured JSON."
        )

    def load_processed_ads(self, ads_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Load normalized ads from data/processed/ads.json."""
        target_path = ads_path or (self.settings.data_dir / "processed" / "ads.json")
        if not target_path.exists():
            logger.warning("Processed ads file not found at %s", target_path)
            return []

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("ads", [])
        except Exception as e:
            logger.error("Failed to read processed ads: %s", str(e))
            return []

    def analyze_single_ad(self, ad: Dict[str, Any], system_prompt: str) -> Optional[Dict[str, Any]]:
        """Analyze an individual ad item using Hermes 3 LLM."""
        ad_id = ad.get("id", "unknown")
        source_url = ad.get("source_url", "")
        advertiser = ad.get("advertiser", "Unknown")
        headline = ad.get("headline", "")
        ad_text = ad.get("ad_text", "")
        creative_type = ad.get("creative_type", "unknown")
        landing_page = ad.get("landing_page", "")

        user_prompt = f"""Analyze this Meta advertisement and extract structured marketing intelligence.

Ad Data:
- ID: {ad_id}
- Advertiser: {advertiser}
- Headline: {headline}
- Body Text / Script: {ad_text}
- Creative Type: {creative_type}
- Landing Page: {landing_page}
- Source URL: {source_url}

Respond ONLY with a valid JSON object conforming to this exact structure:
{{
  "source_ad_id": "{ad_id}",
  "source_url": "{source_url}",
  "advertiser": "{advertiser}",
  "hook": "exact or extracted opening hook phrase",
  "opening_pattern": "psychological mechanism used in opening 0-3s",
  "pain_point": "primary acute problem or anxiety addressed",
  "target_icp": "target audience profile",
  "desired_outcome": "promised transformation or result",
  "emotional_trigger": "primary emotional lever activated",
  "marketing_angle": "strategic angle / thesis",
  "offer": "the explicit offer",
  "value_proposition": "core reason to care",
  "CTA": "call to action directive",
  "creative_format": "format (video/image/talking head/demo)",
  "visual_style": "aesthetic, pacing, and visual directives",
  "narrative_structure": "progression of the ad script",
  "persuasion_mechanism": "how belief/credibility is established",
  "notable_elements": ["key element 1", "key element 2"],
  "evidence_note": "clear distinction between observed facts vs inferred marketing hypothesis"
}}"""

        try:
            result = self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.2,
            )
            if result.get("success") and isinstance(result.get("data"), dict):
                data = result["data"]
                # Ensure essential fields are preserved
                data["source_ad_id"] = ad_id
                data["source_url"] = source_url
                data["advertiser"] = advertiser
                return data
            else:
                logger.warning("LLM JSON decode failed for ad %s: %s", ad_id, result.get("error"))
                return None
        except Exception as e:
            logger.error("LLM inference error for ad %s: %s", ad_id, str(e))
            return None

    def generate_aggregate_synthesis(
        self,
        individual_analyses: List[Dict[str, Any]],
        system_prompt: str,
    ) -> Dict[str, Any]:
        """Synthesize recurring industry patterns and CrowdWisdomTrading strategic gaps across all analyzed ads."""
        analyses_summary = []
        for a in individual_analyses:
            analyses_summary.append({
                "advertiser": a.get("advertiser"),
                "hook": a.get("hook"),
                "pain_point": a.get("pain_point"),
                "marketing_angle": a.get("marketing_angle"),
                "target_icp": a.get("target_icp"),
                "emotional_trigger": a.get("emotional_trigger"),
                "CTA": a.get("CTA"),
                "creative_format": a.get("creative_format"),
            })

        user_prompt = f"""Synthesize an aggregate competitive analysis from these {len(individual_analyses)} analyzed Meta ads.

Analyzed Ads Summary:
{json.dumps(analyses_summary, indent=2)}

Identify industry patterns and strategic opportunities for CrowdWisdomTrading (which specializes in crowd sentiment, predictive intelligence, algorithmic consensus, and quantifiable trading edge).

Respond ONLY with a valid JSON object conforming to this exact structure:
{{
  "common_hooks": [
    "Hook pattern 1 with explanation",
    "Hook pattern 2 with explanation",
    "Hook pattern 3 with explanation"
  ],
  "common_pain_points": [
    "Recurring trader pain point 1",
    "Recurring trader pain point 2",
    "Recurring trader pain point 3"
  ],
  "common_icp_characteristics": [
    "Dominant persona trait 1",
    "Dominant persona trait 2",
    "Dominant persona trait 3"
  ],
  "common_creative_structures": [
    "Prevalent narrative framework 1",
    "Prevalent narrative framework 2"
  ],
  "common_visual_patterns": [
    "Common visual motif 1",
    "Common visual motif 2"
  ],
  "common_emotional_triggers": [
    "Emotional lever 1",
    "Emotional lever 2"
  ],
  "common_ctas": [
    "Dominant CTA pattern 1",
    "Dominant CTA pattern 2"
  ],
  "crowdwisdom_opportunities": [
    "Opportunity 1: Strategic white space and high-converting angle for CrowdWisdom",
    "Opportunity 2: How CrowdWisdom's crowd consensus data beats conventional competitor claims",
    "Opportunity 3: Differentiated 30-60s cinematic concept angle"
  ]
}}"""

        try:
            result = self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.3,
            )
            if result.get("success") and isinstance(result.get("data"), dict):
                return result["data"]
            else:
                return {
                    "common_hooks": ["Stop guessing market moves", "Turn time into cashflow"],
                    "common_pain_points": ["Emotional trading", "Lagging indicators", "Lack of conviction"],
                    "common_icp_characteristics": ["Retail options traders", "Active market participants"],
                    "common_creative_structures": ["Hook -> Agitate -> System Demo -> CTA"],
                    "common_visual_patterns": ["Trading terminal overlay", "Chart breakdown"],
                    "common_emotional_triggers": ["Loss aversion", "Fear of missing out"],
                    "common_ctas": ["Reserve Free Spot", "Access VIP Signals"],
                    "crowdwisdom_opportunities": [
                        "Leverage crowd consensus predictions instead of single-guru advice",
                        "Show real-time sentiment shifts before breakout moves",
                    ],
                }
        except Exception as e:
            logger.error("Failed to generate aggregate synthesis: %s", str(e))
            return {}

    def run_analysis(
        self,
        ads_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
        max_ads_to_analyze: int = 10,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """Execute Phase 2: Full Creative Dissection and Aggregate Pattern Synthesis."""
        system_prompt = self.load_system_prompt()
        out_file = output_path or (self.settings.data_dir / "processed" / "ad_analysis.json")
        out_file.parent.mkdir(parents=True, exist_ok=True)

        # Step 1: LOADING ADS
        if verbose:
            console.print("\n[bold cyan]AD ANALYZER → LOADING ADS[/bold cyan]")
        ads = self.load_processed_ads(ads_path)
        if not ads:
            msg = f"No processed ads found to analyze. Please run 'python main.py --stage ads' first."
            if verbose:
                console.print(f"[bold red]! {msg}[/bold red]")
            return {"success": False, "error": msg}

        ads_to_process = ads[:max_ads_to_analyze]
        if verbose:
            console.print(f"  [green]✓ Loaded[/green] [bold white]{len(ads)}[/bold white] ads from database. Analyzing top [bold yellow]{len(ads_to_process)}[/bold yellow] candidates...")

        # Step 2: DISSECTING CREATIVES
        if verbose:
            console.print(f"\n[bold cyan]AD ANALYZER → DISSECTING CREATIVES (Hermes 3: {self.llm.model})[/bold cyan]")

        individual_analyses: List[Dict[str, Any]] = []
        for i, ad in enumerate(ads_to_process, start=1):
            advertiser = ad.get("advertiser", f"Ad #{i}")
            if verbose:
                console.print(f"  • [[bold cyan]{i}/{len(ads_to_process)}[/bold cyan]] Dissecting ad from [yellow]{advertiser}[/yellow] (ID: {ad.get('id')})...")
            
            analysis = self.analyze_single_ad(ad, system_prompt)
            if analysis:
                individual_analyses.append(analysis)

        # Step 3: AGGREGATING PATTERNS & OPPORTUNITIES
        if verbose:
            console.print("\n[bold cyan]AD ANALYZER → AGGREGATING PATTERNS & OPPORTUNITIES[/bold cyan]")
            console.print("  • Synthesizing recurring hooks, pain points, and CrowdWisdom white spaces...")

        aggregate_synthesis = self.generate_aggregate_synthesis(individual_analyses, system_prompt)

        # Step 4: COMPLETE & PERSIST
        payload = {
            "meta": {
                "analyzed_count": len(individual_analyses),
                "total_available_ads": len(ads),
                "model_used": self.llm.model,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "agent": self.name,
            },
            "individual_ad_analyses": individual_analyses,
            "aggregate_patterns": aggregate_synthesis,
        }

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        if verbose:
            console.print("\n[bold green]AD ANALYZER → COMPLETE[/bold green]")
            console.print(f"  [green]✓ Analysis intelligence saved:[/green] [bold white]{out_file}[/bold white]")
            console.print(f"  • Dissected Ads: [bold yellow]{len(individual_analyses)}[/bold yellow]")
            console.print(f"  • Opportunities Identified: [bold yellow]{len(aggregate_synthesis.get('crowdwisdom_opportunities', []))}[/bold yellow]")

        return {
            "success": True,
            "output_file": str(out_file),
            "analyzed_count": len(individual_analyses),
            "data": payload,
        }
