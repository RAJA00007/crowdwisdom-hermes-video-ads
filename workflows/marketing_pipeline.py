"""Hermes Multi-Agent Marketing Pipeline.

Orchestrates the 6-stage end-to-end execution flow:
1. Apify Meta Ad Research (Last 30 days)
2. Ad Hook, Angle & CTA Analysis
3. Tavily/Exa Market & ICP Context Deep Dive
4. CrowdWisdomTrading Proprietary Data Grounding
5. 3 Differentiated Cinematic Ad Concepts & Structured Storyboards
6. 30-60s Cinematic Video Production via OpenMontage
"""

from typing import Any, Dict, Optional
from agents.ads_manager import AdsManagerAgent
from agents.ad_analyzer import AdAnalyzerAgent
from agents.research_agent import ResearchAgent
from agents.proprietary_data_agent import ProprietaryDataAgent
from agents.creative_agent import CreativeAgent
from agents.storyboard_agent import StoryboardAgent
from agents.video_agent import VideoAgent
from tools.llm_tool import HermesLLMClient


class MarketingPipeline:
    """Master workflow orchestrating the multi-agent system with human-readable JSON outputs."""

    def __init__(self, llm_client: Optional[HermesLLMClient] = None):
        self.llm = llm_client or HermesLLMClient()
        self.manager = AdsManagerAgent(llm_client=self.llm)
        self.analyzer = AdAnalyzerAgent(llm_client=self.llm)
        self.researcher = ResearchAgent(llm_client=self.llm)
        self.proprietary = ProprietaryDataAgent()
        self.creative = CreativeAgent(llm_client=self.llm)
        self.storyboard = StoryboardAgent(llm_client=self.llm)
        self.video = VideoAgent()

    def get_pipeline_summary(self) -> Dict[str, Any]:
        """Return the pipeline stages and agent assignments."""
        return {
            "pipeline": "CrowdWisdomTrading Video Ads Multi-Agent Pipeline",
            "framework": "Hermes Agent Framework (Nous Research / OpenRouter)",
            "agents": [
                self.manager.get_agent_profile(),
                self.analyzer.get_agent_profile(),
                self.researcher.get_agent_profile(),
                self.proprietary.get_agent_profile(),
                self.creative.get_agent_profile(),
                self.storyboard.get_agent_profile(),
                self.video.get_agent_profile(),
            ],
            "kanban_tasks": self.manager.init_kanban_board(),
        }

    def execute_stage_ads(
        self,
        queries: Optional[list] = None,
        max_ads_per_query: int = 5,
        days_back: int = 30,
    ) -> Dict[str, Any]:
        """Programmatically execute Phase 1: Meta Ad Research."""
        return self.manager.run_ads_research(
            queries=queries,
            max_ads_per_query=max_ads_per_query,
            days_back=days_back,
        )

    def execute_stage_analysis(
        self,
        ads_path: Optional[str] = None,
        output_path: Optional[str] = None,
        max_ads_to_analyze: int = 10,
    ) -> Dict[str, Any]:
        """Programmatically execute Phase 2: Ad Analysis & Opportunity Synthesis."""
        from pathlib import Path
        return self.analyzer.run_analysis(
            ads_path=Path(ads_path) if ads_path else None,
            output_path=Path(output_path) if output_path else None,
            max_ads_to_analyze=max_ads_to_analyze,
        )

    def execute_stage_research(
        self,
        analysis_path: Optional[str] = None,
        output_path: Optional[str] = None,
        days_back: int = 30,
    ) -> Dict[str, Any]:
        """Programmatically execute Phase 3: Research Agent ICP Deep Dive."""
        from pathlib import Path
        return self.researcher.run_research(
            analysis_path=Path(analysis_path) if analysis_path else None,
            output_path=Path(output_path) if output_path else None,
            days_back=days_back,
        )

    def execute_stage_creative(self) -> Dict[str, Any]:
        """Programmatically execute Phase 4: Proprietary Data Ingestion -> Creative Director -> Storyboard Generator."""
        # 1. Ingest proprietary data
        prop_res = self.proprietary.run_ingestion()
        
        # 2. Develop 3 concepts
        creative_res = self.creative.run_creative_ideation()
        
        # 3. Generate 3 full storyboards
        storyboard_res = self.storyboard.run_storyboard_generation(
            concepts=creative_res.get("concepts", []),
            proprietary_summary=prop_res.get("summary", {}),
        )
        
        return {
            "success": True,
            "proprietary_data": prop_res,
            "creative_concepts": creative_res,
            "storyboards": storyboard_res,
        }

    def execute_stage_video(
        self,
        concept_idx: Optional[int] = None,
        all_concepts: bool = False,
        test_shot: bool = False,
    ) -> Dict[str, Any]:
        """Programmatically execute Phase 6: Video Agent Cinematic Video Production."""
        if test_shot:
            return self.video.generate_single_test_shot()
        elif all_concepts or concept_idx is None:
            return self.video.produce_all_videos()
        else:
            cid = f"concept_{concept_idx:02d}"
            return self.video.produce_concept_video(cid)
