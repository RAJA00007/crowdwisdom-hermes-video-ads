"""Settings and environment variable handling for CrowdWisdomTrading Video Ads Agent.

Fully compatible with Python 3.10 using pydantic-settings.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Project Paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data")
    outputs_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "outputs")
    prompts_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "prompts")

    # Hermes / OpenRouter LLM Settings
    openrouter_api_key: Optional[str] = Field(default=None, alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL")
    hermes_model: str = Field(default="nousresearch/hermes-3-llama-3.1-70b", alias="HERMES_MODEL")
    llm_temperature: float = Field(default=0.7, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=4096, alias="LLM_MAX_TOKENS")

    # Meta Ads Scraper (Apify)
    apify_api_token: Optional[str] = Field(default=None, alias="APIFY_API_TOKEN")
    apify_meta_ads_actor_id: str = Field(default="apify/facebook-ads-scraper", alias="APIFY_META_ADS_ACTOR_ID")

    # Market Research APIs
    tavily_api_key: Optional[str] = Field(default=None, alias="TAVILY_API_KEY")
    exa_api_key: Optional[str] = Field(default=None, alias="EXA_API_KEY")

    # Video Production (OpenMontage)
    openmontage_bin_path: Optional[str] = Field(default=None, alias="OPENMONTAGE_BIN_PATH")
    video_output_resolution: str = Field(default="1080x1920", alias="VIDEO_OUTPUT_RESOLUTION")
    video_default_duration_sec: int = Field(default=45, alias="VIDEO_DEFAULT_DURATION_SEC")

    def ensure_directories(self) -> None:
        """Ensure all data and output directories exist."""
        subdirs = [
            self.data_dir / "raw",
            self.data_dir / "processed",
            self.data_dir / "research",
            self.outputs_dir / "ads",
            self.outputs_dir / "scripts",
            self.outputs_dir / "videos",
        ]
        for path in subdirs:
            path.mkdir(parents=True, exist_ok=True)

    def check_api_keys_status(self) -> dict:
        """Returns a dict of configured API keys (boolean flags only, never secrets)."""
        return {
            "OPENROUTER_API_KEY": bool(self.openrouter_api_key and self.openrouter_api_key != "your_openrouter_api_key_here"),
            "APIFY_API_TOKEN": bool(self.apify_api_token and self.apify_api_token != "your_apify_api_token_here"),
            "TAVILY_API_KEY": bool(self.tavily_api_key and self.tavily_api_key != "your_tavily_api_key_here"),
            "EXA_API_KEY": bool(self.exa_api_key and self.exa_api_key != "your_exa_api_key_here"),
        }


@lru_cache()
def get_settings() -> Settings:
    """Singleton getter for application settings."""
    settings = Settings()
    settings.ensure_directories()
    return settings
