# 🔍 使用 browser-harness 搜索 AI 内容

本文档说明如何使用 browser-harness 从微博/知乎/小红书搜索 AI 相关内容。

## 前置条件

### 1. 安装 browser-harness

```bash
# 如果还未安装
cd ~/Developer/browser-harness
uv tool install -e .
```

### 2. 连接浏览器

```bash
# 方式 1: 使用现有 Chrome（推荐）
# 在 Chrome 中打开 chrome://inspect/#remote-debugging
# 勾选 "Allow remote debugging for this browser instance"

# 方式 2: 启动带调试端口的 Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug
```

### 3. 验证连接

```bash
browser-harness --doctor
# 应该显示:
# [ok  ] chrome running
# [ok  ] daemon alive
```

---

## Domain Skills

已创建 3 个平台的搜索技能，位于 `~/Developer/browser-harness/agent-workspace/domain-skills/`:

```
domain-skills/
├── weibo/
│   └── scraping.md      # 微博热搜搜索
├── zhihu/
│   └── scraping.md      # 知乎热榜搜索
└── xiaohongshu/
    └── scraping.md      # 小红书笔记搜索
```

每个 skill 包含:
- URL patterns
- 搜索流程
- 数据提取代码
- AI 关键词列表
- 反爬策略
- Gotchas 和注意事项

---

## 使用方法

### 方法 1: 运行集成脚本（推荐）

```bash
cd ~/content-pipeline
python3 src/scraper/browser_search.py
```

**输出示例:**
```
============================================================
🤖 AI 内容监控 - 多平台热搜搜索
============================================================
时间：2026-05-07 23:45:00
关键词：AI, 人工智能，大模型，GPT, ChatGPT, OpenAI...

============================================================
🔍 微博热搜 - AI 相关内容
============================================================

发现 3 个 AI 相关热搜:

  #05 OpenAI 发布推理模型 o3 🔥
  #12 AI 绘画工具 Midjourney v7 发布
  #28 Kimi 智能助手升级

============================================================
🔍 知乎热榜 - AI 相关内容
============================================================

发现 5 个 AI 相关话题:

  • 如何评价 OpenAI 新发布的 o3 模型？(380 万热度)
  • AI 绘画会取代设计师吗？(120 万热度)
  ...

✅ 结果已保存到 ai_hot_search_20260507_234500.json
```

### 方法 2: 单独搜索某个平台

#### 微博搜索

```bash
browser-harness -c '
import json
goto_url("https://s.weibo.com/top/summary")
wait_for_load()
wait(2)

hot_search = json.loads(js("""
(function(){
  var rows = Array.from(document.querySelectorAll("#pl_top_realtimehot table td:first-child"));
  return JSON.stringify(rows.slice(1, 31).map(function(el, idx){
    var link = el.querySelector("a");
    return {
      rank: idx + 1,
      title: link ? link.innerText.trim() : null
    };
  }));
})()
"""))

# 筛选 AI 相关
AI_KEYWORDS = ["AI", "GPT", "大模型"]
ai_topics = [t for t in hot_search if any(k in t["title"] for k in AI_KEYWORDS)]
print(json.dumps(ai_topics, ensure_ascii=False, indent=2))
'
```

#### 知乎搜索

```bash
browser-harness -c '
import json
goto_url("https://www.zhihu.com/hot")
wait_for_load()
wait(3)

hot_list = json.loads(js("""
(function(){
  var items = Array.from(document.querySelectorAll(".HotItem"));
  return JSON.stringify(items.slice(0, 50).map(function(el){
    var title = el.querySelector(".HotItem-title");
    var badge = el.querySelector(".HotItem-badge");
    return {
      title: title ? title.innerText.trim() : null,
      hot_value: badge ? badge.innerText.trim() : null
    };
  }));
})()
"""))

print(json.dumps(hot_list[:10], ensure_ascii=False, indent=2))
'
```

#### 小红书搜索

```bash
browser-harness -c '
import json
goto_url("https://www.xiaohongshu.com/search_result?keyword=AI 工具&source=web_explore_feed")
wait_for_load()
wait(3)

notes = json.loads(js("""
(function(){
  var cards = Array.from(document.querySelectorAll(".note-item"));
  return JSON.stringify(cards.slice(0, 20).map(function(el){
    var title = el.querySelector(".title");
    var user = el.querySelector(".user-name");
    var likes = el.querySelector(".interact-info");
    return {
      title: title ? title.innerText.trim() : null,
      user: user ? user.innerText.trim() : null,
      likes: likes ? likes.innerText.trim() : null
    };
  }).filter(item => item.title !== null));
})()
"""))

print(json.dumps(notes[:10], ensure_ascii=False, indent=2))
'
```

### 方法 3: 使用 Codex/Claude Code 自动执行

```bash
# 让 AI agent 自动搜索并分析
codex -p "
使用 browser-harness 搜索微博和知乎的 AI 相关热搜。
参考 ~/Developer/browser-harness/agent-workspace/domain-skills/ 中的技能文档。
提取所有 AI 相关话题，保存到 ai_topics.json，并总结趋势。
"
```

---

## 输出格式

搜索结果保存为 JSON 文件：

```json
{
  "timestamp": "2026-05-07T23:45:00",
  "keywords": ["AI", "人工智能", "大模型", ...],
  "weibo": [
    {
      "rank": 5,
      "title": "OpenAI 发布推理模型 o3",
      "hot_tag": "🔥"
    }
  ],
  "zhihu": [
    {
      "title": "如何评价 OpenAI 新发布的 o3 模型？",
      "hot_value": "380 万热度",
      "url": "/question/123456"
    }
  ],
  "xiaohongshu": [
    {
      "title": "10 个超好用的 AI 工具推荐",
      "user": "科技小姐姐",
      "likes": "1.2 万"
    }
  ]
}
```

---

## 与内容流水线集成

### 将搜索结果传给 LLM 评分

```python
# 1. 搜索热搜
from scraper.browser_search import search_weibo_ai, search_zhihu_ai

weibo_topics = search_weibo_ai()
zhihu_topics = search_zhihu_ai()

# 2. 统一格式
all_topics = []
for t in weibo_topics + zhihu_topics:
    all_topics.append({
        "title": t["title"],
        "heat": t.get("rank", 0) * 10000,  # 估算热度
        "platform": "weibo" if t in weibo_topics else "zhihu"
    })

# 3. LLM 评分
from llm.topic_scoring import score_topics
scored = score_topics(all_topics, threshold=7.0)

# 4. 生成文章
from llm.article_generator import ArticleGenerator
gen = ArticleGenerator()
article = gen.generate_article(scored[0])

print(article["title"])
```

---

## 常见问题

### Q: browser-harness 无法连接浏览器？

A: 检查 Chrome 是否开启了远程调试：
```bash
browser-harness --doctor
# 如果 chrome FAIL，手动打开 Chrome 并访问 chrome://inspect/#remote-debugging
```

### Q: 搜索结果被限制？

A: 可能触发反爬：
- 降低搜索频率（每 3-5 秒一次）
- 使用 browser-harness 的会话保持
- 登录账号（可选）

### Q: Selector 失效？

A: 平台更新导致，查看对应 skill 文档的 Gotchas 章节，或运行：
```bash
browser-harness -c "print(page_info())"
# 查看当前页面结构
```

### Q: 如何搜索其他关键词？

A: 修改 `AI_KEYWORDS` 列表：
```python
AI_KEYWORDS = ["你的关键词 1", "关键词 2"]
```

---

## 下一步

1. **定时任务**: 使用 cronjob 每小时自动搜索
2. **趋势分析**: 对比历史数据发现上升趋势
3. **自动选题**: 结合 LLM 评分自动生成选题
4. **内容生成**: 直接生成文章草稿

---

## 相关文档

- [微博搜索详解](~/Developer/browser-harness/agent-workspace/domain-skills/weibo/scraping.md)
- [知乎搜索详解](~/Developer/browser-harness/agent-workspace/domain-skills/zhihu/scraping.md)
- [小红书搜索详解](~/Developer/browser-harness/agent-workspace/domain-skills/xiaohongshu/scraping.md)
- [browser-harness 官方文档](~/Developer/browser-harness/SKILL.md)
