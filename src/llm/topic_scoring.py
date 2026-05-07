"""
AI 选题评分模块 - 使用 OpenRouter LLM 智能筛选热搜话题
"""

import json
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from .client import create_client, DashScopeClient


class TopicScore(BaseModel):
    """单个话题的 AI 评分结果"""
    title: str = Field(..., description="话题标题")
    score: float = Field(..., description="综合评分 (0-10)")
    ai_relevance: float = Field(..., description="AI 相关性 (0-10)")
    heat: int = Field(..., description="热度值")
    platform: str = Field(..., description="来源平台")
    rank: int = Field(0, description="排名")
    tags: List[str] = Field(default_factory=list, description="AI 相关标签")
    reason: str = Field("", description="推荐理由")


def score_topics(
    topics: List[Dict],
    threshold: float = 7.5,
    client: Optional[DashScopeClient] = None,
) -> List[TopicScore]:
    """
    使用 LLM 评分并筛选热门 AI 话题
    
    Args:
        topics: 热搜话题列表，每项含 title, heat, platform
        threshold: 评分阈值，低于此值不返回
        client: OpenRouter 客户端（可选，自动创建）
        
    Returns:
        按评分降序排列的 TopicScore 列表
    """
    if not topics:
        return []
    
    client = client or create_client()
    
    # 检查 API Key
    if not client.api_key:
        print("  ⚠️ DASHSCOPE_API_KEY 未配置，使用本地规则评分")
        return _local_score(topics, threshold)
    
    # 构建系统 prompt
    sys_prompt = """你是一位资深 AI 内容策展人。你的任务是分析中文热搜话题并评估其 AI/科技内容创作价值。

评分维度（每项 1-10 分）：
1. **AI 相关性**: 话题与人工智能、机器学习、大模型、AI 应用等直接相关程度
2. **内容稀缺性**: 这个话题是否有独特分析角度
3. **讨论热度**: 话题本身的热度价值

综合评分 = AI相关性×0.6 + 内容稀缺性×0.25 + 热度价值×0.15

要求：
- 只选择 AI 相关性 >= 5 的话题（有 AI 分析价值）
- 对所有 50 个话题进行评分
- 返回 JSON 格式：{"topics": [...]}

重要：只输出 JSON，不要其他文字。"""
    
    # 构建用户 prompt
    topics_text = "\n".join([
        f"{i+1}. [{t.get('heat', 0)}🔥] {t['title']} ({t.get('platform', 'unknown')})"
        for i, t in enumerate(topics[:50])
    ])
    
    user_prompt = f"""分析以下 {min(len(topics), 50)} 条热搜话题，评估其 AI 内容创作价值：

{topics_text}

返回 JSON 格式：
{{"topics": [
  {{"title": "话题原文", "ai_relevance": 0-10, "scarcity": 0-10, "reason": "简短推荐理由(中文)", "tags": ["标签1", "标签2"]}}
]}}"""

    print("  🤖 调用 LLM 评分...")
    try:
        result = client.chat_json([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ])
        
        scored = []
        for item in result.get("topics", []):
            title = item.get("title", "")
            ai_rel = float(item.get("ai_relevance", 0))
            scarcity = float(item.get("scarcity", 5))
            
            # 计算综合评分
            final_score = round(ai_rel * 0.6 + scarcity * 0.25 + 5 * 0.15, 1)
            
            # 找到原始话题的热度
            original = next((t for t in topics if t["title"] == title), {})
            heat = original.get("heat", 0)
            
            if final_score >= threshold:
                scored.append(TopicScore(
                    title=title,
                    score=final_score,
                    ai_relevance=ai_rel,
                    heat=heat,
                    platform=item.get("platform", original.get("platform", "unknown")),
                    tags=item.get("tags", []),
                    reason=item.get("reason", ""),
                ))
        
        # 按评分降序
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored
        
    except Exception as e:
        print(f"  ⚠️ LLM 评分出错: {e}，回退到本地规则评分")
        return _local_score(topics, threshold)


def _local_score(topics: List[Dict], threshold: float = 7.5) -> List[TopicScore]:
    """本地规则评分（不依赖 LLM）"""
    # AI 相关关键词
    ai_keywords = [
        "AI", "人工智能", "大模型", "GPT", "ChatGPT", "OpenAI", "LLM",
        "机器学习", "深度学", "神经网络", "Stable Diffusion", "Midjourney",
        "Sora", "Claude", "Gemini", "Copilot", "通义", "文心一言",
        "智谱", "百川", "月之暗面", "Kimi", "豆包", "元", "Agent",
        "RAG", "Fine-tune", "量化", "推理", "训练", "数据集",
        "NVIDIA", "GPU", "H100", "算力", "芯片", "半导体",
        "自动驾驶", "机器人", "NLP", "CV", "多模态",
    ]
    
    scored = []
    for topic in topics:
        title = topic.get("title", "")
        title_lower = title.lower()
        
        # 计算 AI 相关性
        matched_keywords = [kw for kw in ai_keywords if kw.lower() in title_lower]
        ai_relevance = min(10, len(matched_keywords) * 2 + 3)
        
        if ai_relevance >= 5:
            heat = topic.get("heat", 0)
            heat_score = min(10, heat / 10000)
            final_score = round(ai_relevance * 0.7 + heat_score * 0.3, 1)
            
            if final_score >= threshold:
                scored.append(TopicScore(
                    title=title,
                    score=final_score,
                    ai_relevance=ai_relevance,
                    heat=heat,
                    platform=topic.get("platform", "unknown"),
                    tags=matched_keywords,
                    reason=f"匹配关键词: {', '.join(matched_keywords)}",
                ))
    
    scored.sort(key=lambda x: x.score, reverse=True)
    return scored


if __name__ == "__main__":
    # 测试
    test_topics = [
        {"title": "ChatGPT 新特性：支持语音对话", "heat": 52000, "platform": "weibo"},
        {"title": "某明星官宣离婚", "heat": 89000, "platform": "weibo"},
        {"title": "AI 绘画工具 Midjourney v7 发布", "heat": 18000, "platform": "zhihu"},
        {"title": "特斯拉 FSD 无人驾驶全量推送", "heat": 35000, "platform": "douyin"},
        {"title": "天气预报：周末降温", "heat": 12000, "platform": "weibo"},
        {"title": "OpenAI 发布推理模型 o3", "heat": 75000, "platform": "weibo"},
    ]
    
    print("🧪 测试 AI 选题评分...")
    results = score_topics(test_topics, threshold=6.0)
    
    print(f"\n📊 评分结果 (阈值 6.0):")
    for i, t in enumerate(results, 1):
        print(f"\n  {i}. [{t.score}] {t.title}")
        print(f"     AI 相关性: {t.ai_relevance}/10 | 热度: {t.heat}")
        print(f"     推荐理由: {t.reason}")
        print(f"     标签: {', '.join(t.tags)}")
