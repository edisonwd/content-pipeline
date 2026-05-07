"""LLM 文章生成模块"""
import json
from typing import Dict, Any


class ArticleGenerator:
    """AI 内容生成器 - 基于 LLM 生成初稿"""
    
    def __init__(self, model_provider: str = "openrouter"):
        self.provider = model_provider
        
    def generate_article(self, topic: Dict) -> Dict[str, Any]:
        """从话题生成完整文章草稿
        
        Returns:
            {
                'title': '标题',
                'content': '正文内容',
                'outline': ['大纲要点'],
                'keywords': ['关键词列表'],
                'image_prompt': '配图描述 (用于 DALL·E/Pexels)',
            }
        """
        
        prompt = f"""你是 AI 领域的内容创作者。根据以下热搜话题写一篇 800-1200 字的专业分析文章：

话题：{topic['title']}
热度：{topic['heat']}🔥
平台：{topic['platform']}
推荐理由：{topic.get('reason', '')}

要求：
1. 专业客观的 AI 行业视角
2. 包含技术背景、发展趋势、影响分析
3. 适合小红书/公众号发布的风格
4. 在文末推荐 1-2 张配图的描述

输出格式为 JSON：
{{
  "title": "吸引人但专业的标题",
  "outline": ["要点 1", "要点 2"],
  "content": "...全文内容...",
  "keywords": ["AI", "技术趋势"],
  "image_prompt": "一张现代科技感插图..."
}}

只返回 JSON，不要其他文字。"""
        
        # TODO: 调用 LLM API
        pass
        
        
def generate_image_prompt(topic: Dict) -> str:
    """生成配图提示词"""
    return f"Professional tech illustration about {topic['title']}, modern minimalist style, blue and white color scheme"


if __name__ == "__main__":
    test_topic = {
        "title": "ChatGPT-o1 推理模型发布",
        "ai_relevance": 9.5,
        "heat": 75000,
        "platform": "weibo",
        "reason": "OpenAI 最新旗舰模型，强调逻辑推理能力突破"
    }
    
    generator = ArticleGenerator()
    article = generator.generate_article(test_topic)
    
    print(json.dumps(article, indent=2, ensure_ascii=False))
