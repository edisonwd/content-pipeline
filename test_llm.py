#!/usr/bin/env python3
"""测试 LLM 集成"""

import sys
sys.path.insert(0, 'src')

from llm.client import create_client
from llm.topic_scoring import score_topics
from llm.article_generator import ArticleGenerator
import json

# 模拟热搜数据
topics = [
    {'title': 'OpenAI 发布推理模型 o3，性能超越人类博士', 'heat': 95000, 'platform': 'weibo'},
    {'title': '某明星官宣离婚', 'heat': 89000, 'platform': 'weibo'},
    {'title': '通义千问发布新一代多模态大模型 Qwen2.5-VL', 'heat': 68000, 'platform': 'zhihu'},
    {'title': 'AI 绘画工具 Midjourney v7 发布', 'heat': 42000, 'platform': 'zhihu'},
    {'title': '特斯拉 FSD 入华获批', 'heat': 75000, 'platform': 'douyin'},
    {'title': 'Kimi 智能助手升级，支持 200 万字上下文', 'heat': 38000, 'platform': 'weibo'},
    {'title': 'NVIDIA 发布新一代 H200 GPU', 'heat': 55000, 'platform': 'zhihu'},
]

print("=" * 60)
print("🎯 AI 选题评分测试 (阿里云百炼)")
print("=" * 60)

results = score_topics(topics, threshold=6.0)
print(f"\n✅ 筛选出 {len(results)} 条 AI 相关选题:\n")

for i, t in enumerate(results, 1):
    print(f"{i}. [{t.score}/10] {t.title}")
    print(f"   热度：{t.heat}🔥 | 平台：{t.platform}")
    print(f"   标签：{', '.join(t.tags)}")
    print()

# 测试文章生成
print("\n" + "=" * 60)
print("✍️ 文章生成测试")
print("=" * 60)

if results:
    best_topic = results[0]
    print(f"\n选择最佳选题：{best_topic.title}")
    
    gen = ArticleGenerator()
    article = gen.generate_article({
        'title': best_topic.title,
        'heat': best_topic.heat,
        'platform': best_topic.platform,
        'reason': best_topic.reason,
    })
    
    print(f"\n📝 生成结果:")
    print(f"   标题：{article['title']}")
    print(f"   大纲：{len(article['outline'])} 个要点")
    print(f"   字数：{len(article['content'])}")
    print(f"   关键词：{', '.join(article['keywords'])}")
    
    # 保存
    output = {'topic': {'title': best_topic.title, 'score': best_topic.score}, 'article': article}
    with open('test_output.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 已保存到 test_output.json")
