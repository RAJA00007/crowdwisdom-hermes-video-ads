"""Tavily search tool for researching ICP pain points, financial market trends, and marketing context.

Preserves source URLs and citations. Compatible with Python 3.10.
"""

import logging
from typing import Any, Dict, List, Optional
from tavily import TavilyClient
from config.settings import get_settings

logger = logging.getLogger(__name__)


class TavilyResearchTool:
    """Tool for web and market research using Tavily Search API."""

    def __init__(self, api_key: Optional[str] = None):
        settings = get_settings()
        self.api_key = api_key or settings.tavily_api_key
        if self.api_key and self.api_key != "your_tavily_api_key_here":
            self.client = TavilyClient(api_key=self.api_key)
        else:
            self.client = None

    def is_configured(self) -> bool:
        """Check if Tavily API key is configured."""
        return bool(self.client is not None and self.api_key and self.api_key != "your_tavily_api_key_here")

    def search_market_context(
        self,
        query: str,
        max_results: int = 5,
        days: int = 30,
        search_depth: str = "advanced",
    ) -> Dict[str, Any]:
        """Search market context and return structured findings with citations and dates."""
        if not self.is_configured():
            return {
                "success": False,
                "error": "TAVILY_API_KEY is not configured in .env",
                "results": [],
            }

        try:
            kwargs = {
                "query": query,
                "search_depth": search_depth,
                "max_results": max_results,
                "include_answer": True,
                "include_raw_content": False,
            }
            if days:
                kwargs["days"] = days

            response = self.client.search(**kwargs)

            results: List[Dict[str, Any]] = []
            for item in response.get("results", []):
                results.append({
                    "title": item.get("title") or "Untitled Source",
                    "url": item.get("url") or "",
                    "content": item.get("content") or "",
                    "score": item.get("score"),
                    "published_date": item.get("published_date"),
                    "source": item.get("url", "").split("/")[2] if "//" in item.get("url", "") else "Web",
                })

            return {
                "success": True,
                "query": query,
                "answer": response.get("answer"),
                "results": results,
                "source": "Tavily Search API",
            }
        except Exception as e:
            logger.error("Tavily search failed for '%s': %s", query, str(e))
            return {
                "success": False,
                "query": query,
                "error": f"Tavily search failed: {str(e)}",
                "results": [],
            }
