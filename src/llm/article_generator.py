"""
LLM 文章生成模块 - 使用阿里云百炼生成 AI 文章初稿
"""

import json
import os
from typing import Dict, Any, Optional

from .client import create_client, DashScopeClient


class ArticleGenerator:
    """AI 内容生成器 - 基于百炼 LLM 生成初稿"""

    def __init__(self, client: Optional[DashScopeClient] = None):
        self.client = client or create_client()

    def generate_article(self, topic: Dict) -> Dict[str, Any]:
        """从话题生成完整文章草稿

        Returns:
            {
                'title': '吸引人的标题',
                'content': '正文内容',
                'outline': ['大纲要点'],
                'keywords': ['关键词'],
                'image_prompt': '配图描述 (用于 Pexels/DALL·E)',
            }
        """
        if not self.client.api_key:
            print("  ⚠️ DASHSCOPE_API_KEY 未配置，使用模板生成")
            return self._template_article(topic)

        sys_prompt = """你是一位资深 AI 领域内容创作者。你的文章风格专业、易懂，适合中文社交媒体发布。

输出要求：
1. 标题吸引人但不标题党
2. 正文 800-1200 字，段落分明，有观点有分析
3. 包含：背景介绍 → 核心分析 → 趋势展望 → 读者互动
4. 文末推荐 1-2 张配图风格（用于 Pexels 搜索）

只返回 JSON，格式严格如下：
{
  "title": "标题",
  "outline": ["要点1", "要点2", "要点3"],
  "content": "完整正文...",
  "keywords": ["标签1", "标签2"],
  "image_prompt": "配图描述（英文，用于 Pexels 搜索，如: futuristic AI robot hand touching digital interface）"
}"""

        user_prompt = f"""根据以下话题写一篇适合小红书/公众号的 AI 分析文章：

话题标题：{topic.get('title', '')}
推荐理由：{topic.get('reason', topic.get('reason', ''))}
热度：{topic.get('heat', 'N/A')}🔥
来源：{topic.get('platform', 'N/A')}

文章要求：
- 目标读者：对 AI 感兴趣但不一定有技术背景的年轻人
- 语气：专业但有温度
- 长度：800-1200 字
- 结构清晰，每段有小标题

输出 JSON，不要其他文字。"""

        print("  ✍️ 调用百炼生成文章...")
        try:
            result = self.client.chat_json([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ])

            return {
                "title": result.get("title", topic.get("title", "")),
                "outline": result.get("outline", []),
                "content": result.get("content", ""),
                "keywords": result.get("keywords", []),
                "image_prompt": result.get(
                    "image_prompt",
                    f"AI technology abstract background related to {topic.get('title', 'AI')}",
                ),
            }
        except Exception as e:
            print(f"  ⚠️ 文章生成失败: {e}，使用模板")
            return self._template_article(topic)

    def _template_article(self, topic: Dict) -> Dict[str, Any]:
        """离线模板文章（API Key 未配置时的备用方案）"""
        title = topic.get("title", "AI 前沿资讯")
        return {
            "title": f"深度解读 | {title}",
            "outline": [
                f"{title} 事件概述",
                "技术背景分析",
                "对行业的影响",
                "未来趋势展望",
            ],
            "content": (
                f"# {title}\n\n"
                f"## 事件概述\n"
                f"近日，「{title}」成为热议话题。"
                f"本文从 AI 从业者的角度进行深度分析。\n\n"
                f"## 技术背景\n"
                f"这一事件反映了 AI 领域的最新发展趋势，"
                f"涉及大模型能力提升、应用场景拓展等关键方向。\n\n"
                f"## 影响分析\n"
                f"对开发者来说，这意味着新的技术栈和学习方向；"
                f"对普通用户而言，AI 正在加速融入日常生活。\n\n"
                f"## 展望\n"
                f"AI 技术仍在高速迭代，持续关注最新动态是保持竞争力的关键。\n\n"
                f"---\n"
                f"*本文由 AI 辅助生成，仅供参考。*"
            ),
            "keywords": ["AI", "大模型", "科技趋势"],
            "image_prompt": (
                f"Professional minimalist tech illustration about {title}, "
                "blue and white color scheme, clean composition"
            ),
        }


def generate_image_prompt(topic: Dict) -> str:
    """生成 Pexels 配图搜索词"""
    generator = ArticleGenerator()
    article = generator.generate_article(topic)
    return article.get("image_prompt", "technology artificial intelligence abstract")


if __name__ == "__main__":
    test_topic = {
        "title": "通义千问发布新一代多模态大模型",
        "heat": 65000,
        "platform": "weibo",
        "reason": "阿里自研大模型重大升级，多模态能力显著提升",
    }

    gen = ArticleGenerator()
    article = gen.generate_article(test_topic)

    print("📝 生成结果:")
    print(json.dumps(article, ensure_ascii=False, indent=2))
