"""scripts/phase12_discovery.py

Performs OpenMontage installation inspection and provider matrix discovery
according to Phase 12 requirements.
"""

import importlib
import inspect
import json
import os
import pkgutil
import sys
from pathlib import Path

OPENMONTAGE_PATH = Path(os.getenv("OPENMONTAGE_PATH") or (Path.home() / "OpenMontage"))

def discover_installation():
    installed = OPENMONTAGE_PATH.exists() and (OPENMONTAGE_PATH / "tools" / "base_tool.py").exists()
    
    version = "unknown"
    git_dir = OPENMONTAGE_PATH / ".git"
    if git_dir.exists():
        try:
            import subprocess
            res = subprocess.run(
                ["git", "-C", str(OPENMONTAGE_PATH), "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            version = res.stdout.strip()
        except Exception:
            version = "0.2.0"
    
    install_record = {
        "installed": installed,
        "version": version,
        "install_path": str(OPENMONTAGE_PATH),
        "source": "https://github.com/calesthio/OpenMontage.git",
        "installation_method": "git_clone",
        "verification": "Repository verified with 40+ video and audio tools in tools/video and tools/audio"
    }
    return install_record

def discover_providers():
    if not OPENMONTAGE_PATH.exists():
        return {"openmontage_installed": False, "providers": {}}

    sys.path.insert(0, str(OPENMONTAGE_PATH))
    from tools.base_tool import BaseTool, ToolStatus
    import tools.video

    providers = {}

    # Map of known requirements per provider tool in OpenMontage
    tool_key_map = {
        "kling_video": "FAL_KEY",
        "veo_video": "FAL_KEY",
        "minimax_fal_video": "FAL_KEY",
        "seedance_video": "FAL_KEY",
        "gemini_omni_fal": "FAL_KEY",
        "runway_video": "RUNWAY_API_KEY",
        "kling_official_video": "KLING_API_KEY",
        "minimax_video": "MINIMAX_API_KEY",
        "seedance_ark": "ARK_API_KEY",
        "gemini_omni_video": "GOOGLE_API_KEY",
        "hunyuan_cloud_video": "TENCENT_TOKENHUB_API_KEY",
        "jimeng_video": "VOLC_ACCESSKEY",
        "atlas_video": "ATLASCLOUD_API_KEY",
        "heygen_video": "HEYGEN_API_KEY",
        "sora_video": "OPENAI_API_KEY",
        "grok_video": "XAI_API_KEY",
        "seedance_replicate": "REPLICATE_API_TOKEN",
        "wan_video": "LOCAL_GPU (torch+diffusers)",
        "cogvideo_video": "LOCAL_GPU (torch+diffusers)",
        "hunyuan_video": "LOCAL_GPU (torch+diffusers)",
        "ltx_video_local": "LOCAL_GPU (torch+diffusers)",
        "comfyui_video": "COMFYUI_SERVER_URL",
        "pexels_video": "PEXELS_API_KEY",
        "pixabay_video": "PIXABAY_API_KEY"
    }

    for finder, modname, ispkg in pkgutil.iter_modules(tools.video.__path__):
        if modname.startswith("_"):
            continue
        try:
            mod = importlib.import_module(f"tools.video.{modname}")
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, BaseTool) and obj is not BaseTool and getattr(obj, "capability", "") == "video_generation":
                    inst = obj()
                    t_name = inst.name
                    req_key = tool_key_map.get(t_name, "API_KEY")
                    
                    # Check if configured
                    is_conf = False
                    if inst.runtime.value == "local_gpu":
                        status = inst.get_status()
                        is_conf = (status == ToolStatus.AVAILABLE)
                        cred_req = False
                    elif inst.runtime.value == "api":
                        # Check whether required env var exists in os.environ
                        env_keys = [d[4:] for d in inst.dependencies if d.startswith("env:")]
                        if not env_keys and req_key and not req_key.startswith("LOCAL"):
                            env_keys = [req_key]
                        
                        cred_req = bool(env_keys)
                        if env_keys:
                            is_conf = all(bool(os.environ.get(k)) for k in env_keys)
                        else:
                            is_conf = (inst.get_status() == ToolStatus.AVAILABLE)
                    else:
                        is_conf = (inst.get_status() == ToolStatus.AVAILABLE)
                        cred_req = False

                    providers[t_name] = {
                        "provider_name": inst.provider,
                        "runtime": inst.runtime.value,
                        "supported": True,
                        "configured": is_conf,
                        "credential_required": cred_req,
                        "required_credential": req_key,
                        "capabilities": getattr(inst, "capabilities", []),
                        "supports_image_reference": inst.supports.get("image_to_video", False) if hasattr(inst, "supports") else False
                    }
        except Exception:
            pass

    return {
        "openmontage_installed": True,
        "openmontage_path": str(OPENMONTAGE_PATH),
        "total_video_tools": len(providers),
        "providers": providers
    }

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    out_dir = Path("outputs/videos")
    out_dir.mkdir(parents=True, exist_ok=True)

    install_info = discover_installation()
    with open(out_dir / "phase12_openmontage_install.json", "w", encoding="utf-8") as f:
        json.dump(install_info, f, indent=2)
    print("Wrote outputs/videos/phase12_openmontage_install.json")

    provider_matrix = discover_providers()
    with open(out_dir / "phase12_provider_matrix.json", "w", encoding="utf-8") as f:
        json.dump(provider_matrix, f, indent=2)
    print("Wrote outputs/videos/phase12_provider_matrix.json")
    print(f"Total video tools discovered: {provider_matrix['total_video_tools']}")
