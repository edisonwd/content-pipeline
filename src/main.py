#!/usr/bin/env python3
"""
AI Content Pipeline - 主入口
自动化内容创作与发布系统
"""

import argparse
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config.settings import load_config
from scraper.hot_search import fetch_hot_search
from llm.topic_scoring import score_topics
from llm.article_generator import generate_article
from notion.sync import save_to_notion
from publish.xiaohongshu import publish_to_xiaohongshu


def cmd_scrape(args):
    """抓取热搜"""
    print("🔍 开始抓取热搜...")
    platforms = args.platform.split(",") if args.platform else ["weibo", "zhihu", "douyin"]
    
    hot_searches = {}
    for platform in platforms:
        print(f"  → 抓取 {platform}...")
        hot_searches[platform] = fetch_hot_search(platform)
    
    # 保存到原始数据目录
    data_dir = Path("data/raw")
    data_dir.mkdir(exist_ok=True)
    
    import json
    timestamp = Path("data/raw").joinpath(f"hot_search_{args.date}.json")
    with open(timestamp, "w", encoding="utf-8") as f:
        json.dump(hot_searches, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 热搜数据已保存至 {timestamp}")
    return hot_searches


def cmd_generate(args):
    """生成 AI 选题和文章"""
    print("🤖 开始 AI 选题筛选...")
    
    # 读取热搜数据
    import json
    from pathlib import Path
    
    date = args.date or Path("data/raw").glob("hot_search_*.json").name.replace("hot_search_", "").replace(".json", "")
    raw_path = Path(f"data/raw/hot_search_{date}.json")
    
    if not raw_path.exists():
        print(f"❌ 未找到热搜数据：{raw_path}")
        return None
    
    with open(raw_path, "r", encoding="utf-8") as f:
        hot_searches = json.load(f)
    
    # 统一格式 + 去重
    all_topics = []
    for platform, topics in hot_searches.items():
        for topic in topics:
            all_topics.append({
                "title": topic["title"],
                "rank": topic.get("rank", 0),
                "platform": platform,
                "heat": topic.get("heat", 0)
            })
    
    # 排序
    all_topics.sort(key=lambda x: x.get("heat", 0), reverse=True)
    
    # LLM 评分
    scored = score_topics(all_topics[:50], threshold=args.threshold)
    
    # 输出最佳选题
    print(f"\n🎯 Top {len(scored)} AI 选题:")
    for i, topic in enumerate(scored[:10], 1):
        print(f"  {i}. [{topic['score']}] {topic['title']} (热度:{topic['heat']})")
    
    # 生成文章
    if args.output == "notion":
        print("\n📝 生成文章并保存到 Notion...")
        for topic in scored[:args.count]:
            article = generate_article(topic)
            notion_id = save_to_notion(article)
            print(f"   ✅ {topic['title']} → Notion: {notion_id}")
    
    return scored


def cmd_publish(args):
    """发布到小红书"""
    print("🚀 发布到小红书...")
    
    notion_id = args.draft_id
    result = publish_to_xiaohongshu(notion_id)
    print(f"✅ 发布结果：{result}")
    return result


def main():
    parser = argparse.ArgumentParser(description="AI 内容生产流水线")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # scrape 命令
    p_scrape = subparsers.add_parser("scrape", help="抓取热搜")
    p_scrape.add_argument("--platform", default="weibo,zhihu,douyin", help="平台列表")
    p_scrape.add_argument("--date", default=None, help="日期 (YYYYMMDD)")
    
    # generate 命令
    p_gen = subparsers.add_parser("generate", help="生成 AI 选题/文章")
    p_gen.add_argument("--date", required=True, help="热搜数据日期")
    p_gen.add_argument("--output", choices=["console", "notion"], default="notion")
    p_gen.add_argument("--threshold", type=float, default=7.5, help="评分阈值")
    p_gen.add_argument("--count", type=int, default=3, help="生成文章数量")
    
    # publish 命令
    p_pub = subparsers.add_parser("publish", help="发布到小红书")
    p_pub.add_argument("--draft-id", required=True, help="Notion 草稿 ID")
    
    args = parser.parse_args()
    
    if args.command == "scrape":
        cmd_scrape(args)
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "publish":
        cmd_publish(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
