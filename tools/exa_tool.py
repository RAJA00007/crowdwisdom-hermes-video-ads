"""Exa neural search tool for ICP deep discovery and competitor analysis.

Preserves exact URLs, publication dates, and author/source context. Compatible with Python 3.10.
"""

import logging
from typing import Any, Dict, List, Optional
from exa_py import Exa
from config.settings import get_settings

logger = logging.getLogger(__name__)


class ExaResearchTool:
    """Tool for neural web discovery using Exa AI."""

    def __init__(self, api_key: Optional[str] = None):
        settings = get_settings()
        self.api_key = api_key or settings.exa_api_key
        if self.api_key and self.api_key != "your_exa_api_key_here":
            self.client = Exa(api_key=self.api_key)
        else:
            self.client = None

    def is_configured(self) -> bool:
        """Check if Exa API key is configured."""
        return bool(self.client is not None and self.api_key and self.api_key != "your_exa_api_key_here")

    def search_icp_insights(
        self,
        query: str,
        num_results: int = 5,
    ) -> Dict[str, Any]:
        """Search neural web for ICP pain points, sentiment, and trading community discussions."""
        if not self.is_configured():
            return {
                "success": False,
                "error": "EXA_API_KEY is not configured in .env",
                "results": [],
            }

        try:
            response = self.client.search_and_contents(
                query=query,
                num_results=num_results,
                text=True,
            )

            results: List[Dict[str, Any]] = []
            for item in getattr(response, "results", []):
                url = getattr(item, "url", "")
                results.append({
                    "title": getattr(item, "title", "Untitled"),
                    "url": url,
                    "published_date": getattr(item, "published_date", None),
                    "content": getattr(item, "text", "")[:1200],
                    "source": url.split("/")[2] if "//" in url else "Exa Neural Web",
                })

            return {
                "success": True,
                "query": query,
                "results": results,
                "source": "Exa Neural Search",
            }
        except Exception as e:
            logger.error("Exa search failed for '%s': %s", query, str(e))
            return {
                "success": False,
                "query": query,
                "error": f"Exa search failed: {str(e)}",
                "results": [],
            }
