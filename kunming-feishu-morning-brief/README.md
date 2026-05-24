# 昆明飞书图文晨报 Skill

这是一个 Codex Skill，用于生成并推送适合手机端阅读的飞书晨报。

## 能做什么

- 每天生成过去 24 小时内的重要新闻晨报
- 覆盖国际新闻、国内新闻、云南/昆明本地新闻、AI 新闻
- 每条重点新闻配对应新闻图片，而不是栏目标题图
- 加入昆明天气、穿衣建议、今日判断
- 最后附一条不重复的毛泽东语录
- 通过飞书机器人发送为高级感图文卡片

## 使用方式

把本目录作为 Codex Skill 使用，触发语可以是：

- `生成今天的昆明飞书晨报`
- `推送一份晨报到飞书`
- `调整晨报模板`
- `把每天 8:30 的晨报改成这个图文格式`

## 飞书配置

长期使用时，不要把密钥写进代码或提交到 GitHub。请用环境变量：

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="oc_xxx"
```

发送已有卡片 JSON：

```bash
python scripts/send_feishu_card.py card.json
```

## 安全提醒

如果 App Secret 曾经发在聊天、截图、日志或仓库里，请去飞书开放平台重置密钥后再用于长期自动推送。

## 目录

```text
kunming-feishu-morning-brief/
├── SKILL.md
├── README.md
├── references/
│   ├── card-style.md
│   └── mao-quotes.md
└── scripts/
    └── send_feishu_card.py
```
