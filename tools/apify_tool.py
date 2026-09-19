"""Apify tool for querying Meta Ad Library campaigns from the last 30 days.

Preserves real source URLs and ad metadata. Compatible with Python 3.10.
"""

import json
import logging
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from apify_client import ApifyClient
from config.settings import get_settings

logger = logging.getLogger(__name__)

# Default search keywords tailored for CrowdWisdomTrading's ICP
DEFAULT_ICP_SEARCH_QUERIES = [
    "stock market prediction",
    "market sentiment trading",
    "algorithmic trading signals",
    "crowd sentiment investing",
    "financial intelligence AI trading",
    "options trading signals",
]


class ApifyMetaAdsTool:
    """Tool for retrieving and normalizing real Meta ad campaign data via Apify."""

    def __init__(self, api_token: Optional[str] = None, actor_id: Optional[str] = None):
        settings = get_settings()
        self.api_token = api_token or settings.apify_api_token
        self.actor_id = actor_id or settings.apify_meta_ads_actor_id
        self.raw_data_dir = settings.data_dir / "raw"
        self.processed_data_dir = settings.data_dir / "processed"

        if self.api_token and self.api_token != "your_apify_api_token_here":
            self.client = ApifyClient(self.api_token)
        else:
            self.client = None

    def is_configured(self) -> bool:
        """Check if Apify token is configured with a non-placeholder value."""
        return bool(self.client is not None and self.api_token and self.api_token != "your_apify_api_token_here")

    def build_meta_ad_library_url(self, query: str, country: str = "US") -> str:
        """Construct the direct Meta Ad Library search URL for a query."""
        params = {
            "active_status": "active",
            "ad_type": "all",
            "country": country,
            "q": query,
            "sort_data[direction]": "desc",
            "sort_data[mode]": "relevancy_monthly_grouped",
            "search_type": "keyword_unordered",
            "media_type": "all",
        }
        return f"https://www.facebook.com/ads/library/?{urllib.parse.urlencode(params)}"

    def fetch_ads_for_query(
        self,
        query: str,
        country: str = "US",
        max_items: int = 10,
        days_back: int = 30,
    ) -> Dict[str, Any]:
        """Execute Apify actor search for a single query."""
        if not self.is_configured():
            return {
                "success": False,
                "query": query,
                "error": "APIFY_API_TOKEN is not configured in .env",
                "items": [],
            }

        target_url = self.build_meta_ad_library_url(query, country)
        run_input = {
            "startUrls": [{"url": target_url}],
            "searchQuery": query,
            "searchTerms": [query],
            "country": country,
            "activeStatus": "active",
            "mediaType": "all",
            "maxAds": max_items,
            "resultsLimit": max_items,
            "daysBack": days_back,
        }

        try:
            # Call actor with timeout guard
            run = self.client.actor(self.actor_id).call(run_input=run_input, timeout_secs=180)
            if not run or "defaultDatasetId" not in run:
                return {
                    "success": False,
                    "query": query,
                    "error": "Apify actor did not produce a dataset ID",
                    "items": [],
                }

            items: List[Dict[str, Any]] = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                item["_search_query"] = query
                items.append(item)

            return {
                "success": True,
                "query": query,
                "target_url": target_url,
                "count": len(items),
                "items": items,
            }
        except Exception as e:
            logger.error("Apify actor run failed for query '%s': %s", query, str(e))
            return {
                "success": False,
                "query": query,
                "error": f"Apify error: {str(e)}",
                "items": [],
            }

    def fetch_multi_query_ads(
        self,
        queries: Optional[List[str]] = None,
        country: str = "US",
        max_ads_per_query: int = 10,
        days_back: int = 30,
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Search multiple ICP-focused queries across Meta Ad Library.

        Returns (raw_items_list, execution_summary).
        """
        search_queries = queries or DEFAULT_ICP_SEARCH_QUERIES
        all_raw_items: List[Dict[str, Any]] = []
        query_summaries: Dict[str, Any] = {}

        for q in search_queries:
            result = self.fetch_ads_for_query(
                query=q,
                country=country,
                max_items=max_ads_per_query,
                days_back=days_back,
            )
            query_summaries[q] = {
                "success": result.get("success", False),
                "count": result.get("count", 0),
                "error": result.get("error"),
            }
            if result.get("success") and result.get("items"):
                all_raw_items.extend(result["items"])

        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "queries_searched": search_queries,
            "total_raw_collected": len(all_raw_items),
            "query_summaries": query_summaries,
            "is_configured": self.is_configured(),
        }

        return all_raw_items, summary

    def save_raw_results(self, raw_items: List[Dict[str, Any]], summary: Dict[str, Any]) -> Path:
        """Persist raw Apify scrape response to data/raw/."""
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        raw_file = self.raw_data_dir / f"meta_ads_raw_{timestamp_str}.json"

        payload = {
            "summary": summary,
            "items": raw_items,
        }
        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return raw_file

    def normalize_ad_item(self, raw_item: Dict[str, Any], index: int) -> Optional[Dict[str, Any]]:
        """Normalize an ad item from Apify payload to standardized schema.

        Preserves source traceability and never fabricates missing metrics.
        """
        if not isinstance(raw_item, dict):
            return None

        # Inspect nested snapshot dict if present
        snapshot = raw_item.get("snapshot") if isinstance(raw_item.get("snapshot"), dict) else {}

        # Extract ad identifier
        ad_id = str(
            raw_item.get("id")
            or raw_item.get("adId")
            or raw_item.get("ad_id")
            or raw_item.get("adArchiveID")
            or f"ad_{index + 1}"
        )

        # Extract advertiser
        advertiser = (
            raw_item.get("pageName")
            or raw_item.get("advertiser_name")
            or raw_item.get("page_name")
            or snapshot.get("pageName")
            or (raw_item.get("page") or {}).get("name")
            or "Unknown Advertiser"
        )

        # Extract text / body copy
        body_obj = snapshot.get("body") if isinstance(snapshot.get("body"), dict) else {}
        ad_text = (
            raw_item.get("adText")
            or raw_item.get("body")
            or raw_item.get("ad_creative_body")
            or raw_item.get("text")
            or body_obj.get("text")
            or snapshot.get("adText")
            or ""
        )
        if isinstance(ad_text, list):
            ad_text = "\n".join(str(t) for t in ad_text if t)

        # Extract headline and description
        headline = (
            raw_item.get("headline")
            or raw_item.get("title")
            or raw_item.get("ad_creative_link_title")
            or snapshot.get("title")
            or snapshot.get("headline")
            or ""
        )
        description = (
            raw_item.get("description")
            or raw_item.get("linkDescription")
            or raw_item.get("ad_creative_link_description")
            or snapshot.get("linkDescription")
            or ""
        )

        # Extract media / creative URLs
        creative_url = None
        creative_type = "unknown"

        # Check video assets (top-level and snapshot)
        videos = raw_item.get("videos") or raw_item.get("videoUrls") or snapshot.get("videos") or []
        if isinstance(videos, list) and videos:
            v0 = videos[0]
            if isinstance(v0, str):
                creative_url = v0
            elif isinstance(v0, dict):
                creative_url = v0.get("videoHdUrl") or v0.get("videoSdUrl") or v0.get("videoUrl") or v0.get("url") or v0.get("videoPreviewImageUrl")
            creative_type = "video"
        elif raw_item.get("videoUrl") or raw_item.get("video_url") or snapshot.get("videoUrl"):
            creative_url = raw_item.get("videoUrl") or raw_item.get("video_url") or snapshot.get("videoUrl")
            creative_type = "video"

        # Check image assets if video not found
        if not creative_url:
            images = raw_item.get("images") or raw_item.get("imageUrls") or snapshot.get("images") or []
            if isinstance(images, list) and images:
                i0 = images[0]
                if isinstance(i0, str):
                    creative_url = i0
                elif isinstance(i0, dict):
                    creative_url = i0.get("imageUrl") or i0.get("url") or i0.get("originalImageUrl")
                creative_type = "image"
            elif raw_item.get("imageUrl") or raw_item.get("image_url") or snapshot.get("imageUrl"):
                creative_url = raw_item.get("imageUrl") or raw_item.get("image_url") or snapshot.get("imageUrl")
                creative_type = "image"
            elif snapshot.get("pageProfilePictureUrl"):
                creative_url = snapshot.get("pageProfilePictureUrl")
                creative_type = "image"

        # Extract destination landing page
        landing_page = (
            raw_item.get("linkUrl")
            or raw_item.get("landingPageUrl")
            or raw_item.get("ad_creative_link_url")
            or raw_item.get("url")
            or snapshot.get("linkUrl")
            or None
        )

        # Extract dates
        start_date = raw_item.get("startDate") or raw_item.get("ad_delivery_start_time") or raw_item.get("start_date") or snapshot.get("startDate")
        end_date = raw_item.get("endDate") or raw_item.get("ad_delivery_stop_time") or raw_item.get("end_date") or snapshot.get("endDate")
        is_active = raw_item.get("isActive", raw_item.get("is_active", True if not end_date else False))

        # Extract platforms
        platforms = raw_item.get("publisherPlatforms") or raw_item.get("platforms") or snapshot.get("publisherPlatforms") or ["facebook", "instagram"]
        if isinstance(platforms, str):
            platforms = [platforms]

        # Extract real engagement indicators if present (never fabricate)
        engagement: Dict[str, Any] = {}
        if "impressions" in raw_item:
            engagement["impressions"] = raw_item["impressions"]
        if "spend" in raw_item:
            engagement["spend"] = raw_item["spend"]
        if "reach" in raw_item:
            engagement["reach"] = raw_item["reach"]

        # Source URL
        source_url = (
            raw_item.get("adSnapshotUrl")
            or raw_item.get("snapshot_url")
            or (f"https://www.facebook.com/ads/library/?id={ad_id}" if ad_id else None)
        )

        search_query = raw_item.get("_search_query", "general_market")

        return {
            "id": str(ad_id),
            "advertiser": str(advertiser).strip(),
            "headline": str(headline).strip(),
            "ad_text": str(ad_text).strip(),
            "description": str(description).strip(),
            "creative_url": creative_url,
            "creative_type": creative_type,
            "landing_page": landing_page,
            "start_date": start_date,
            "end_date": end_date,
            "is_active": is_active,
            "platform": platforms,
            "engagement_indicators": engagement if engagement else None,
            "search_query": search_query,
            "source_url": source_url,
            "collected_at": datetime.now(timezone.utc).isoformat(),
        }

    def normalize_and_save_ads(self, raw_items: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Path]:
        """Normalize a collection of raw ads and save to data/processed/ads.json."""
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        processed_file = self.processed_data_dir / "ads.json"

        normalized_list: List[Dict[str, Any]] = []
        seen_ids = set()

        for idx, item in enumerate(raw_items):
            norm = self.normalize_ad_item(item, idx)
            if norm:
                # Deduplicate by ad ID or text snippet
                dedup_key = norm["id"] if norm["id"] != f"ad_{idx+1}" else norm["ad_text"][:80]
                if dedup_key not in seen_ids:
                    seen_ids.add(dedup_key)
                    normalized_list.append(norm)

        payload = {
            "meta": {
                "total_ads": len(normalized_list),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "source": "Meta Ad Library (via Apify)",
                "target_niche": "CrowdWisdomTrading Market Predictions & ICP Finance Ads",
            },
            "ads": normalized_list,
        }

        with open(processed_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return normalized_list, processed_file
