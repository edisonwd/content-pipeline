"""AI 选题评分模块"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class TopicScore(BaseModel):
    """单个话题的 AI 评分结果"""
    title: str = Field(..., description="话题标题")
    score: float = Field(..., description="综合评分 (0-10)")
    ai_relevance: float = Field(..., description="AI 相关性 (0-10)")
    heat: int = Field(..., description="热度值")
    platform: str = Field(..., description="来源平台")
    rank: int = Field(..., description="排名")
    tags: List[str] = Field(default_factory=list, description="AI 相关标签")
    reason: str = Field(..., description="推荐理由")
    

def score_topics(topics: List[Dict], threshold: float = 7.5) -> List[TopicScore]:
    """使用 LLM 评分并筛选热门 AI 话题
    
    Args:
        topics: List of raw topic dicts with 'title', 'heat', 'platform'
        threshold: Score threshold for filtering
        
    Returns:
        List of scored topics sorted by score descending
    """
    
    # TODO: 集成 LLM API (OpenRouter/Llama-cpp)
    # Prompt 示例:
    # "分析以下热搜话题的 AI/科技相关度，评分 0-10"
    # "输出 JSON: {{title, ai_relevance, heat, platform, tags, reason}}"
    
    pass
    

def generate_prompt(topics: List[Dict]) -> str:
    """生成 LLM prompt"""
    base_prompt = """You are an expert content strategist specializing in AI/tech topics. 
Analyze these hot search topics from Chinese social media and rate their relevance to AI technology.
For each topic, provide:
1. AI_RELEVANCE_SCORE (0-10)
2. REASON (brief explanation)
3. TAGS (relevant AI keywords)

Return ONLY a JSON list without markdown or extra text.

Topics to analyze:
"""
    
    for i, topic in enumerate(topics[:50], 1):
        base_prompt += f"\n{i}. [{topic.get('heat')}🔥] {topic['title']} ({topic['platform']})\n"
    
    return base_prompt + "\n\nFormat as valid JSON array:\n[\n  {\n    \"title\": \"\",\n    \"ai_relevance\": 0,\n    \"reason\": \"\",\n    \"tags\": []\n  }\n]"


# Quick test (without actual LLM)
if __name__ == "__main__":
    test_topics = [
        {"title": "ChatGPT 新特性", "heat": 52000, "platform": "weibo"},
        {"title": "某明星离婚", "heat": 89000, "platform": "weibo"},
        {"title": "AI 绘画工具评测", "heat": 12000, "platform": "zhihu"},
    ]
    
    print(generate_prompt(test_topics))
