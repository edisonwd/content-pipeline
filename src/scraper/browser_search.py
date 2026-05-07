#!/usr/bin/env python3
"""
AI 内容监控 - 使用 browser-harness 搜索多平台 AI 热搜
用法：python3 search_ai_content.py
"""

import json
import sys
from datetime import datetime

# AI 相关关键词
AI_KEYWORDS = [
    "AI", "人工智能", "大模型", "GPT", "ChatGPT", "OpenAI",
    "AIGC", "AI 绘画", "AI 工具", "通义千问", "Kimi",
    "Sora", "Midjourney", "Stable Diffusion", "LLM"
]


def search_weibo_ai():
    """微博 AI 热搜"""
    print("\n" + "="*60)
    print("🔍 微博热搜 - AI 相关内容")
    print("="*60)
    
    goto_url("https://s.weibo.com/top/summary")
    wait_for_load()
    wait(2)
    
    # 提取热搜榜
    hot_search = json.loads(js("""
    (function(){
      var rows = Array.from(document.querySelectorAll('#pl_top_realtimehot table td:first-child'));
      return JSON.stringify(rows.slice(1, 31).map(function(el, idx){
        var link = el.querySelector('a');
        var hot = el.querySelector('i');
        return {
          rank: idx + 1,
          title: link ? link.innerText.trim() : null,
          hot_tag: hot ? hot.className : ''
        };
      }));
    })()
    """))
    
    # 筛选 AI 相关
    ai_topics = []
    for topic in hot_search:
        title_lower = topic['title'].lower()
        if any(kw.lower() in title_lower for kw in AI_KEYWORDS):
            ai_topics.append(topic)
    
    print(f"\n发现 {len(ai_topics)} 个 AI 相关热搜:\n")
    for t in ai_topics:
        tag = "🔥" if "hot" in t.get('hot_tag', '') else ""
        print(f"  #{t['rank']:02d} {t['title']} {tag}")
    
    return ai_topics


def search_zhihu_ai():
    """知乎热榜 - AI 相关内容"""
    print("\n" + "="*60)
    print("🔍 知乎热榜 - AI 相关内容")
    print("="*60)
    
    goto_url("https://www.zhihu.com/hot")
    wait_for_load()
    wait(3)
    
    hot_list = json.loads(js("""
    (function(){
      var items = Array.from(document.querySelectorAll('.HotItem'));
      return JSON.stringify(items.slice(0, 50).map(function(el){
        var title = el.querySelector('.HotItem-title');
        var badge = el.querySelector('.HotItem-badge');
        return {
          title: title ? title.innerText.trim() : null,
          hot_value: badge ? badge.innerText.trim() : null,
          url: el.getAttribute('href')
        };
      }));
    })()
    """))
    
    # 筛选 AI 相关
    ai_topics = []
    for item in hot_list:
        title_lower = item['title'].lower()
        if any(kw.lower() in title_lower for kw in AI_KEYWORDS):
            ai_topics.append(item)
    
    print(f"\n发现 {len(ai_topics)} 个 AI 相关话题:\n")
    for t in ai_topics[:10]:
        print(f"  • {t['title']} ({t['hot_value']})")
    
    return ai_topics


def search_xiaohongshu_ai():
    """小红书 - AI 相关内容"""
    print("\n" + "="*60)
    print("🔍 小红书 - AI 相关内容")
    print("="*60)
    
    keyword = "AI 工具"
    goto_url(f"https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_explore_feed")
    wait_for_load()
    wait(3)
    
    notes = json.loads(js("""
    (function(){
      var cards = Array.from(document.querySelectorAll('.note-item'));
      return JSON.stringify(cards.slice(0, 20).map(function(el){
        var title = el.querySelector('.title');
        var user = el.querySelector('.user-name');
        var likes = el.querySelector('.interact-info');
        return {
          title: title ? title.innerText.trim() : null,
          user: user ? user.innerText.trim() : null,
          likes: likes ? likes.innerText.trim() : null,
          url: el.getAttribute('href')
        };
      }).filter(item => item.title !== null));
    })()
    """))
    
    print(f"\n发现 {len(notes)} 篇 AI 笔记:\n")
    for note in notes[:10]:
        print(f"  • {note['title']} - @{note['user']} ({note['likes']})")
    
    return notes


def main():
    """主函数 - 搜索所有平台"""
    print("="*60)
    print("🤖 AI 内容监控 - 多平台热搜搜索")
    print("="*60)
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"关键词：{', '.join(AI_KEYWORDS[:8])}...")
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'keywords': AI_KEYWORDS,
        'weibo': search_weibo_ai(),
        'zhihu': search_zhihu_ai(),
        'xiaohongshu': search_xiaohongshu_ai()
    }
    
    # 保存结果
    filename = f"ai_hot_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print(f"✅ 结果已保存到 {filename}")
    print("="*60)
    
    # 汇总
    print("\n📊 汇总:")
    print(f"  微博：{len(results['weibo'])} 个 AI 热搜")
    print(f"  知乎：{len(results['zhihu'])} 个 AI 话题")
    print(f"  小红书：{len(results['xiaohongshu'])} 篇 AI 笔记")
    
    return results


if __name__ == "__main__":
    main()
