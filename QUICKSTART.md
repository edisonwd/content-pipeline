# 🚀 快速开始指南

## 1. 环境配置

### 安装依赖
```bash
cd ~/content-pipeline
pip3 install -r requirements.txt
```

### 配置 API Keys
编辑 `.env` 文件（已配置百炼 API Key）：
```bash
DASHSCOPE_API_KEY=sk-023dc3bf5d5944edaed8393c35830de9  # ✅ 已配置
```

---

## 2. 测试 LLM 集成

### 运行测试脚本
```bash
python3 test_llm.py
```

**预期输出：**
```
🎯 AI 选题评分测试 (阿里云百炼)
✅ 筛选出 5 条 AI 相关选题:

1. [8.8/10] OpenAI 发布推理模型 o3，性能超越人类博士
2. [8.5/10] 通义千问发布新一代多模态大模型 Qwen2.5-VL
3. [7.6/10] AI 绘画工具 Midjourney v7 发布
...

✍️ 文章生成测试
📝 生成结果:
   标题：OpenAI 新模型 o3：超越人类博士的推理能力...
   字数：831
```

---

## 3. 使用 CLI 工具

### 查看帮助
```bash
python3 src/main.py --help
```

### 命令 1: 抓取热搜
```bash
python3 src/main.py scrape --platform weibo,zhihu,douyin
```
> ⚠️ 爬虫模块待实现，当前返回空数据

### 命令 2: 生成 AI 选题
```bash
python3 src/main.py generate --date 20260507 --output console
```

### 命令 3: 保存到 Notion（待配置）
```bash
# 1. 获取 Notion Integration Token: https://www.notion.so/my-integrations
# 2. 编辑 .env 添加 NOTION_API_KEY
# 3. 运行：
python3 src/main.py generate --date 20260507 --output notion
```

---

## 4. 自定义 LLM 模型

编辑 `.env`：
```bash
# 可选模型：qwen-max, qwen-plus, qwen-turbo
DASHSCOPE_MODEL=qwen-max
```

**模型对比：**
| 模型 | 速度 | 质量 | 价格 (元/千 tokens) |
|------|------|------|---------------------|
| qwen-max | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ¥0.04 |
| qwen-plus | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ¥0.01 |
| qwen-turbo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ¥0.003 |

---

## 5. 下一步开发

### 待实现模块
- [ ] **热搜爬虫** (scrapers/) - 微博/知乎/抖音
- [ ] **Notion 集成** (notion/) - 草稿数据库
- [ ] **配图生成** (images/) - Pexels API
- [ ] **小红书发布** (publish/) - CDP/RPA

### 优先级建议
1. **Notion 集成** - 先建立草稿库工作流
2. **Pexels 配图** - 免费图源，易实现
3. **热搜爬虫** - 需要反爬策略
4. **小红书发布** - 可先用手动发布过渡

---

## 6. 常见问题

### Q: API Key 无效？
A: 检查百炼控制台：https://bailian.console.aliyun.com/#/api-key

### Q: 余额不足？
A: 新用户送 100 万 tokens，约等于 500 篇文章

### Q: 本地测试无 API Key？
A: 会自动回退到本地规则评分（关键词匹配）

---

## 📚 相关文档

- [项目总览](README.md)
- [实现进度](IMPLEMENTATION_STATUS.md)
- [百炼 API 文档](https://help.aliyun.com/zh/dashscope/)
