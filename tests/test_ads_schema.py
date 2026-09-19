import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.apify_tool import ApifyMetaAdsTool

def test_normalization_schema():
    tool = ApifyMetaAdsTool()
    sample_raw = [
        {
            "id": "104928502391029",
            "pageName": "Alpha Sentiment Trading",
            "adText": "Stop guessing which stocks will move tomorrow. Our AI crowd intelligence platform aggregates retail sentiment and options flow in real-time.",
            "headline": "Predict Market Sentiment in Real-Time",
            "description": "Join 50,000+ traders making data-driven entries.",
            "videoUrl": "https://video.xx.fbcdn.net/v/sample_ad_video.mp4",
            "linkUrl": "https://alphasentiment.io/signals?ref=meta_ad",
            "startDate": "2026-08-28T14:30:00Z",
            "endDate": None,
            "isActive": True,
            "platforms": ["facebook", "instagram"],
            "impressions": "50K - 100K",
            "spend": "$500 - $999",
            "adSnapshotUrl": "https://www.facebook.com/ads/library/?id=104928502391029",
            "_search_query": "market sentiment trading"
        }
    ]

    normalized, path = tool.normalize_and_save_ads(sample_raw)
    assert len(normalized) == 1
    ad = normalized[0]

    assert ad["id"] == "104928502391029"
    assert ad["advertiser"] == "Alpha Sentiment Trading"
    assert ad["headline"] == "Predict Market Sentiment in Real-Time"
    assert ad["creative_type"] == "video"
    assert ad["creative_url"] == "https://video.xx.fbcdn.net/v/sample_ad_video.mp4"
    assert ad["source_url"] == "https://www.facebook.com/ads/library/?id=104928502391029"
    assert ad["engagement_indicators"] == {"impressions": "50K - 100K", "spend": "$500 - $999"}
    assert "collected_at" in ad
    print("Schema test passed! ads.json generated at:", path)

if __name__ == "__main__":
    test_normalization_schema()
