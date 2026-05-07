"""Notion 集成 - 保存草稿到数据库"""
from notion_client import Client


def save_to_notion(article: dict) -> str:
    """将 AI 生成的文章保存到 Notion 草稿库
    
    Args:
        article: Dict with title, content, outline, keywords, image_prompt
        
    Returns:
        Notion page ID
    """
    
    # Load config
    from config.settings import Config
    client = Client(auth=Config.NOTION_API_KEY)
    
    # Create or get the drafts database
    # Database ID should be set in .env as NOTION_DRAFTS_DB_ID
    
    # Create a page in the drafts database
    response = client.pages.create(
        parent={"database_id": "YOUR_DATABASE_ID_HERE"},
        properties={
            "标题": {"title": [{"text": {"content": article['title']}}]},
            "状态": {"select": {"name": "草稿"}},
            "AI 评分": {"number": 8.5},  # Add scoring later
            "发布日期": {"date": None},  # Scheduled for later
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "\n".join(article.get('outline', []))}}
                    ]
                }
            },
            {
                "object": "block", 
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": article['content']}}]}
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": f"配图建议：{article.get('image_prompt', '')}"}}]
                }
            }
        ]
    )
    
    return response["id"]


if __name__ == "__main__":
    test_article = {
        "title": "ChatGPT-o1 深度评测：AI 推理能力的重大突破",
        "outline": ["o1 的推理能力介绍", "技术对比分析", "实际应用场景"],
        "content": "OpenAI 最新发布的 o1 模型在逻辑推理方面取得了显著突破...",
        "keywords": ["OpenAI", "AI 推理", "大模型"],
        "image_prompt": "Minimalist tech illustration showing AI neural network connections"
    }
    
    # Note: This requires actual NOTION_API_KEY to run
    print("需要配置 NOTION_API_KEY 才能运行")
