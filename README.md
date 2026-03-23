# daily-news-brief

> OpenClaw Skill：每日新闻简报 — 飞书 JSON 2.0 高级互动卡片

## 📰 功能简介

自动生成中文每日新闻简报，通过飞书 API 发送**JSON 2.0 高级互动卡片**。

### 卡片特性
- 🎨 **Indigo 主题**标题 + **AI 生成** turquoise 标签
- 🌡️ **天气三栏布局**：气温 / 天气 / 湿度 + 穿衣建议
- 🌍🇨🇳📍🤖 **四个彩色板块**：国际/国内/本地/AI
- ✨ **今日一句** 居中紫色调背景
- 📊 自定义 RGBA 背景色，深色模式适配

### 内容规则
- 每板块 **3-4 条**新闻，按重要性排序
- 严格 **24 小时时效性**，区分「事件日期 vs 发布日期」
- 国际新闻来自 Reuters / AP / Bloomberg 等国际通讯社
- 来源和时间戳来自搜索结果，不可编造

## 🔧 依赖

- [OpenClaw](https://github.com/nicepkg/openclaw) 运行环境
- [minimax-web-search](https://github.com/wansong24/minimax-web-search) Skill（搜索引擎）
- 飞书开放平台 App（需 appId / appSecret）

## 📂 目录结构

```
daily-news-brief/
├── SKILL.md              # 主技能定义（含卡片模板和全部规则）
├── README.md             # 本文件
├── scripts/
│   └── pick_quote.py     # 名言选取脚本（避免重复）
└── references/
    ├── quote-pool.md     # 名言库
    └── source-guide.md   # 新闻来源指南
```

## 🚀 使用方式

### 1. 安装到 OpenClaw
```bash
cp -r daily-news-brief ~/.openclaw/workspace/skills/
```

### 2. 配置飞书
在 `~/.openclaw/openclaw.json` 中配置飞书 channel：
```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "your_app_id",
      "appSecret": "your_app_secret"
    }
  }
}
```

### 3. 设置定时任务
在 `~/.openclaw/cron/jobs.json` 中添加 cron job，关键配置：
```json
{
  "sessionTarget": "isolated",
  "schedule": { "expr": "30 8 * * *", "tz": "Asia/Shanghai" }
}
```

### 4. 手动触发
对 OpenClaw 说：
> 请生成并发送今天的飞书版每日新闻简报

## 📋 版本

- `v2026.03.23` — 初始版本
  - 飞书 JSON 2.0 高级互动卡片
  - 时效性验证机制（事件日期 vs 发布日期）
  - 国际通讯社来源优先
  - 重要性排序机制

## 📄 License

MIT
