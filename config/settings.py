import json
import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseModel

class LLMConfig(BaseModel):
    model: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_tokens: int = 2048

class AppConfig(BaseModel):
    llm: dict[str, LLMConfig]  # Supports multiple providers

class Config:
    """Singleton config manager with lazy loading."""
    
    _instance = None
    _config: AppConfig | None = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load()
    
    def _load(self):
        config_path = Path(__file__).parent / "config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        
        with open(config_path) as f:
            data = json.load(f)
        
        self._config = AppConfig(**data)
    
    @property
    def llm(self) -> dict[str, LLMConfig]:
        return self._config.llm
    
    def get_llm_config(self, provider: str) -> LLMConfig:
        return self._config.llm.get(provider)

@lru_cache()
def get_config() -> Config:
    """Returns singleton Config instance."""
    return Config()