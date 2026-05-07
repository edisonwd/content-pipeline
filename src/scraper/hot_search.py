"""热搜抓取模块"""
from datetime import datetime
import requests
import json


def fetch_hot_search(platform: str):
    """从指定平台抓取热搜
    
    Args:
        platform: weibo | zhihu | douyin
        
    Returns:
        List of hot search topics with title, rank, heat
    """
    
    if platform == "weibo":
        return _fetch_weibo()
    elif platform == "zhihu":
        return _fetch_zhihu()
    elif platform == "douyin":
        return _fetch_douyin()
    else:
        raise ValueError(f"Unsupported platform: {platform}")


def _fetch_weibo():
    """微博热搜 - 使用第三方 API 或 Playwright"""
    # TODO: 实现具体逻辑
    # 可以调用 https://weibo.com/ajax/hotsearch 或使用 Playwright
    pass


def _fetch_zhihu():
    """知乎热榜"""
    pass


def _fetch_douyin():
    """抖音热榜"""
    pass


if __name__ == "__main__":
    print(fetch_hot_search("weibo"))
