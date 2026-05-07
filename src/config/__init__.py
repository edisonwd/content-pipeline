"""配置管理"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """全局配置"""
    
    @staticmethod
    def get(key, default=None):
        return os.environ.get(key, default)
    
    # API Keys
    GITHUB_TOKEN = get("GITHUB_TOKEN")
    NOTION_API_KEY = get("NOTION_API_KEY")
    OPENROUTER_API_KEY = get("OPENROUTER_API_KEY")
    PEXELS_API_KEY = get("PEXELS_API_KEY")
    XIAOHONGSHU_CDP_KEY = get("XIAOHONGSHU_CDP_KEY")
    
    # LLM Settings
    USE_LLAMA_CPP = get("USE_LLAMA_CPP", "false").lower() == "true"
    LLM_PROVIDER = get("LLM_PROVIDER", "openrouter")
    LLAMA_MODEL_PATH = get("LLAMA_MODEL_PATH", "~/.cache/llama/Qwen1.5-7B-Chat-GGUF/q4_k_m.gguf")
    
    # Browser
    BU_NAME = get("BU_NAME", "default")
    BU_CDP_WS = get("BU_CDP_WS", "ws://127.0.0.1:9222")
    
    # Content
    AI_SCORE_THRESHOLD = float(get("AI_SCORE_THRESHOLD", "7.5"))
    DAILY_POST_LIMIT = int(get("DAILY_POST_LIMIT", "3"))


def load_config():
    """加载当前环境配置"""
    config = Config()
    return {k: v for k, v in vars(config).items() if not k.startswith("_")}
