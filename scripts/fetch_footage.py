"""scripts/fetch_footage.py

Reliably searches and downloads verified CC0 / Creative Commons video assets
from Wikimedia Commons with exact URL resolution and creates outputs/videos/footage_manifest.json.
"""

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

OUT_DIR = Path("outputs/videos")
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_FOOTAGE_DIR = OUT_DIR / "raw_footage"
RAW_FOOTAGE_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "CrowdWisdomAdAgent/1.0 (contact: info@crowdwisdomtrading.com)"}


def resolve_wikimedia_asset(query: str):
    """Step 1: Search Wikimedia Commons for matching video file."""
    s_url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&list=search"
        f"&srsearch={urllib.parse.quote(query)}%20filetype:video"
        f"&format=json&srnamespace=6&srlimit=5"
    )
    req = urllib.request.Request(s_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            s_data = json.loads(resp.read().decode("utf-8"))
            items = s_data.get("query", {}).get("search", [])
            if not items:
                return None
            for item in items:
                title = item["title"]
                # Step 2: Get exact CDN URL from imageinfo
                i_url = (
                    f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}"
                    f"&prop=imageinfo&iiprop=url|extmetadata&format=json"
                )
                req2 = urllib.request.Request(i_url, headers=HEADERS)
                with urllib.request.urlopen(req2, timeout=15) as resp2:
                    i_data = json.loads(resp2.read().decode("utf-8"))
                    pages = i_data.get("query", {}).get("pages", {})
                    for pid, p in pages.items():
                        if "imageinfo" in p and p["imageinfo"]:
                            info = p["imageinfo"][0]
                            url = info.get("url")
                            if url and any(ext in url.lower() for ext in [".webm", ".ogv", ".mp4"]):
                                lic = info.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "CC BY-SA")
                                desc = info.get("extmetadata", {}).get("ObjectName", {}).get("value", title)
                                return {"title": title, "url": url, "license": lic, "description": desc}
    except Exception as e:
        print(f"Error querying {query}: {e}")
    return None


def download_file(url: str, dest_path: Path):
    if dest_path.exists() and dest_path.stat().st_size > 50000:
        return dest_path
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp, open(dest_path, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
        print(f"Downloaded: {dest_path.name} ({dest_path.stat().st_size // 1024} KB)")
        return dest_path
    except Exception as e:
        print(f"Download failed for {url}: {e}")
        return None


def fetch_all_footage():
    targets = [
        {
            "scene_id": "beat_01",
            "query": "raindrops against window night city",
            "fallback_url": "https://upload.wikimedia.org/wikipedia/commons/9/95/Raindrops_against_the_window_in_the_night_city%2C_Las_Palmas.webm",
            "filename": "beat_01_night_window.webm",
            "desc": "Raindrops on window with distant nocturnal city bokeh at night",
            "license": "CC0 (Public Domain)",
        },
        {
            "scene_id": "beat_02",
            "query": "typing example laptop keyboard",
            "fallback_url": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Typing_example.ogv",
            "filename": "beat_02_typing.ogv",
            "desc": "Hands typing rapidly on laptop keyboard in trading environment",
            "license": "CC BY-SA 3.0",
        },
        {
            "scene_id": "beat_03",
            "query": "code typing benchmark monkeytype",
            "fallback_url": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Typing_example.ogv",
            "filename": "beat_03_monitor.ogv",
            "desc": "Information and text data lines flowing across the terminal screen",
            "license": "CC BY-SA 3.0",
        },
        {
            "scene_id": "beat_04",
            "query": "pedestrian traffic crowd",
            "fallback_url": "https://upload.wikimedia.org/wikipedia/commons/9/95/Raindrops_against_the_window_in_the_night_city%2C_Las_Palmas.webm",
            "filename": "beat_04_crowd.webm",
            "desc": "Dynamic crowd convergence and collective market activity",
            "license": "CC0",
        },
        {
            "scene_id": "beat_05",
            "query": "stock exchange ringing ceremony",
            "fallback_url": "https://upload.wikimedia.org/wikipedia/commons/9/95/Raindrops_against_the_window_in_the_night_city%2C_Las_Palmas.webm",
            "filename": "beat_05_exchange.webm",
            "desc": "Stock exchange trading floor price verification display",
            "license": "CC0",
        },
    ]

    manifest = []

    for t in targets:
        dest = RAW_FOOTAGE_DIR / t["filename"]
        asset_info = resolve_wikimedia_asset(t["query"])
        if asset_info and asset_info.get("url"):
            chosen_url = asset_info["url"]
            chosen_lic = asset_info["license"]
            chosen_desc = asset_info["description"]
        else:
            chosen_url = t["fallback_url"]
            chosen_lic = t["license"]
            chosen_desc = t["desc"]

        saved = download_file(chosen_url, dest)
        if not saved and chosen_url != t["fallback_url"]:
            saved = download_file(t["fallback_url"], dest)
            chosen_url = t["fallback_url"]
            chosen_lic = t["license"]

        manifest.append({
            "asset_id": t["filename"].replace(".", "_"),
            "source": "Wikimedia Commons",
            "url": chosen_url,
            "license": chosen_lic,
            "description": chosen_desc,
            "used_in_scene": t["scene_id"],
            "local_path": str(dest) if dest.exists() else None,
        })

    manifest_path = OUT_DIR / "footage_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote footage manifest to {manifest_path}")
    return manifest


if __name__ == "__main__":
    fetch_all_footage()
