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
    DASHSCOPE_API_KEY = get("DASHSCOPE_API_KEY")
    PEXELS_API_KEY = get("PEXELS_API_KEY")
    XIAOHONGSHU_CDP_KEY = get("XIAOHONGSHU_CDP_KEY")
    
    # LLM Settings
    LLM_PROVIDER = get("LLM_PROVIDER", "dashscope")
    DASHSCOPE_MODEL = get("DASHSCOPE_MODEL", "qwen-max")
    
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
