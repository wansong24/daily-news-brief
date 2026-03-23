---
name: daily-news-brief
description: Generate Song's fixed-format daily news brief in Chinese as a premium Feishu Interactive Card (JSON 2.0). Use when asked to produce 每日新闻简报 / 晨报 / 头条汇总. Search source: MiniMax web search skill. Structure: (1) 当地天气, (2) 国际头条, (3) 国内头条, (4) 本地头条（云南/昆明）, (5) AI头条, (6) 今日一句. Each section 2–3 items with bold headlines, source and time. Strict 24-hour freshness.
---

# Daily News Brief — 飞书高级互动卡片

## Overview

每天为 Song 生成一份精美的中文新闻简报，以 **飞书 JSON 2.0 高级互动卡片** 形式发送。

**搜索源：** MiniMax 联网搜索（`skills/minimax-web-search`）
**发送方式：** 飞书 API 直接发送（绕过 message tool 的 card 参数验证问题）
**时效性：** 严格 24 小时内新闻
**卡片版本：** JSON 2.0（需飞书客户端 ≥ 7.20）

## 完整流程

### Step 1 — 获取天气

```bash
curl -s "wttr.in/Kunming?format=%C+%t+%h+%w"
```

### Step 2 — MiniMax 联网搜索（串行执行）

**国际新闻必须用英文关键词搜索**，从国际通讯社/门户获取第一手信息：

```bash
cd /Users/song/.openclaw/workspace/skills/minimax-web-search
python3 scripts/minimax_web_search.py "2026年M月D日 国际突发新闻 Reuters AP 世界头条 今天最新" --timeout 30
python3 scripts/minimax_web_search.py "2026年M月D日国内新闻头条热点 今天最新" --timeout 30
python3 scripts/minimax_web_search.py "2026年M月D日云南昆明本地新闻 今天" --timeout 30
python3 scripts/minimax_web_search.py "2026年M月D日AI大模型科技新闻 今天最新" --timeout 30
```

**⚠️ 必须串行！并发会导致 API 超时。每条约 10-20 秒。**
**⚠️ 国际新闻搜索用英文关键词，获取 Reuters/AP/Bloomberg 等国际通讯社原始报道。**

### Step 3 — 构建 JSON 2.0 卡片并发送

用 Python 构建高级卡片 JSON，保存到 `/tmp/news_card.json`，然后用飞书 API 直接发送：

```python
import json, urllib.request, os

card = { ... }  # 构建卡片（见下方模板）

# 保存卡片 JSON
with open('/tmp/news_card.json', 'w') as f:
    json.dump(card, f, ensure_ascii=False)

# 读取飞书配置
config = json.load(open(os.path.expanduser('~/.openclaw/openclaw.json')))
feishu = config['channels']['feishu']
app_id = feishu['appId']
app_secret = feishu['appSecret']

# 获取 tenant_access_token
token_data = json.dumps({'app_id': app_id, 'app_secret': app_secret}).encode()
req = urllib.request.Request(
    'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    data=token_data, headers={'Content-Type': 'application/json'}
)
token = json.loads(urllib.request.urlopen(req).read())['tenant_access_token']

# 发送卡片消息
msg_data = json.dumps({
    'receive_id': 'ou_fa4d55bb488006129e3f36b78e78f173',
    'msg_type': 'interactive',
    'content': json.dumps(card)
}).encode()
req2 = urllib.request.Request(
    'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
    data=msg_data,
    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
)
resp = json.loads(urllib.request.urlopen(req2).read())
print('Send result:', resp.get('code'), resp.get('msg'))
```

**⚠️ 不要用 `message(action="send", channel="feishu", card=...)`，card 参数会报验证错误。必须用飞书 API 直接发送。**

## 卡片模板（JSON 2.0 高级版）

```json
{
  "schema": "2.0",
  "config": {
    "wide_screen_mode": true,
    "enable_forward": true,
    "width_mode": "default",
    "style": {
      "color": {
        "section_blue":    {"light_mode": "rgba(51,112,255,0.08)",  "dark_mode": "rgba(51,112,255,0.15)"},
        "section_pink":    {"light_mode": "rgba(245,74,69,0.08)",   "dark_mode": "rgba(245,74,69,0.15)"},
        "section_gold":    {"light_mode": "rgba(255,165,0,0.08)",   "dark_mode": "rgba(255,165,0,0.15)"},
        "section_green":   {"light_mode": "rgba(52,199,89,0.08)",   "dark_mode": "rgba(52,199,89,0.15)"},
        "weather_bg":      {"light_mode": "rgba(0,122,255,0.06)",   "dark_mode": "rgba(0,122,255,0.12)"},
        "quote_bg":        {"light_mode": "rgba(120,100,200,0.06)", "dark_mode": "rgba(120,100,200,0.12)"}
      }
    }
  },
  "header": {
    "title": {
      "tag": "plain_text",
      "content": "📰 每日新闻简报"
    },
    "subtitle": {
      "tag": "plain_text",
      "content": "YYYY年M月D日 星期X ｜ 昆明"
    },
    "text_tag_list": [
      {
        "tag": "text_tag",
        "text": {"tag": "plain_text", "content": "AI 生成"},
        "color": "turquoise"
      }
    ],
    "template": "indigo"
  },
  "body": {
    "elements": [

      "__COMMENT: ===== 天气板块 =====__",
      {
        "tag": "column_set",
        "flex_mode": "bisect",
        "background_style": "weather_bg",
        "horizontal_spacing": "default",
        "columns": [
          {
            "tag": "column",
            "width": "weighted",
            "weight": 1,
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "text_align": "center", "content": "🌡️ 气温\n**XX° / XX°**"}
            ]
          },
          {
            "tag": "column",
            "width": "weighted",
            "weight": 1,
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "text_align": "center", "content": "☁️ 天气\n**多云**"}
            ]
          },
          {
            "tag": "column",
            "width": "weighted",
            "weight": 1,
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "text_align": "center", "content": "💧 湿度\n**XX%**"}
            ]
          }
        ]
      },
      {
        "tag": "markdown",
        "content": "<font color='grey'>👔 穿衣建议：...</font>"
      },
      {"tag": "hr"},

      "__COMMENT: ===== 国际头条 =====__",
      {
        "tag": "column_set",
        "flex_mode": "none",
        "background_style": "section_blue",
        "columns": [
          {
            "tag": "column",
            "width": "auto",
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "content": "🌍"}
            ]
          },
          {
            "tag": "column",
            "width": "weighted",
            "weight": 1,
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "content": "**国际头条**"}
            ]
          }
        ]
      },
      {
        "tag": "markdown",
        "content": "**▌ 新闻标题**\n正文摘要（2-4句）\n<font color='grey'>📌 来源 ｜ 🕐 YYYY-MM-DD HH:MM</font>"
      },
      {"tag": "hr"},

      "__COMMENT: ===== 国内头条 =====__",
      {
        "tag": "column_set",
        "flex_mode": "none",
        "background_style": "section_pink",
        "columns": [
          {
            "tag": "column",
            "width": "auto",
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "content": "🇨🇳"}
            ]
          },
          {
            "tag": "column",
            "width": "weighted",
            "weight": 1,
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "content": "**国内头条**"}
            ]
          }
        ]
      },
      {
        "tag": "markdown",
        "content": "**▌ 新闻标题**\n正文摘要（2-4句）\n<font color='grey'>📌 来源 ｜ 🕐 YYYY-MM-DD HH:MM</font>"
      },
      {"tag": "hr"},

      "__COMMENT: ===== 本地头条 =====__",
      {
        "tag": "column_set",
        "flex_mode": "none",
        "background_style": "section_gold",
        "columns": [
          {
            "tag": "column",
            "width": "auto",
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "content": "📍"}
            ]
          },
          {
            "tag": "column",
            "width": "weighted",
            "weight": 1,
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "content": "**本地｜云南·昆明**"}
            ]
          }
        ]
      },
      {
        "tag": "markdown",
        "content": "**▌ 新闻标题**\n正文摘要（2-4句）\n<font color='grey'>📌 来源 ｜ 🕐 YYYY-MM-DD HH:MM</font>"
      },
      {"tag": "hr"},

      "__COMMENT: ===== AI头条 =====__",
      {
        "tag": "column_set",
        "flex_mode": "none",
        "background_style": "section_green",
        "columns": [
          {
            "tag": "column",
            "width": "auto",
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "content": "🤖"}
            ]
          },
          {
            "tag": "column",
            "width": "weighted",
            "weight": 1,
            "vertical_align": "center",
            "elements": [
              {"tag": "markdown", "content": "**AI 头条**"}
            ]
          }
        ]
      },
      {
        "tag": "markdown",
        "content": "**▌ 新闻标题**\n正文摘要（2-4句）\n<font color='grey'>📌 来源 ｜ 🕐 YYYY-MM-DD HH:MM</font>"
      },
      {"tag": "hr"},

      "__COMMENT: ===== 今日一句 =====__",
      {
        "tag": "column_set",
        "flex_mode": "none",
        "background_style": "quote_bg",
        "columns": [
          {
            "tag": "column",
            "width": "weighted",
            "weight": 1,
            "vertical_align": "center",
            "padding": "12px 16px 12px 16px",
            "elements": [
              {"tag": "markdown", "text_align": "center", "content": "✨ **今日一句**\n\n「名言内容」\n\n<font color='grey'>—— 作者</font>"}
            ]
          }
        ]
      }
    ]
  }
}
```

**⚠️ 模板中的 `__COMMENT: ...` 行仅为说明，构建 JSON 时不要包含！elements 数组中只放卡片组件对象。**

## 构建卡片的详细规则

**天气板块：**
- 三栏对齐：气温 / 天气状况 / 湿度
- 底部灰色文字穿衣建议
- 背景色 `weather_bg`（淡蓝色调）

**新闻板块（国际/国内/本地/AI 每个板块）：**
- 板块标题用 `column_set` + 对应背景色（`section_blue/pink/gold/green`），内含 emoji + 粗体分类名
- 每条新闻格式：
```
**▌ 标题**
正文（2-4句，充实有内容，信息密集）
<font color='grey'>📌 来源 ｜ 🕐 YYYY-MM-DD HH:MM</font>
```
- 每个板块 2-3 条新闻，多条之间空一行
- 板块之间用 `{"tag": "hr"}` 分割

**今日一句：**
- `column_set` 居中，`quote_bg` 紫色调淡背景
- 居中对齐：✨ 今日一句 + 名言 + 作者

## 内容规则

**每条新闻格式（在 markdown content 中）：**
```
**▌ 标题**
正文（2-4句，充实有内容，信息密集）
<font color='grey'>📌 来源 ｜ 🕐 YYYY-MM-DD HH:MM</font>
```

**板块顺序与数量（固定）：**
1. 🌡️ 天气（三栏布局 + 穿衣建议）
2. 🌍 国际头条（**3-4条**）
3. 🇨🇳 国内头条（**3-4条**）
4. 📍 本地｜云南·昆明（**3-4条**，本地新闻不足时可降为2条）
5. 🤖 AI头条（**3-4条**）
6. ✨ 今日一句（居中带背景色）

## ⚠️ 时效性验证机制（严格执行）

### 核心原则：区分「文章发布日期」和「事件发生日期」

文章今天发布 ≠ 事件今天发生。必须确保**事件本身**发生在24小时内。

### 过滤规则

1. **搜索时间锚定**：搜索关键词必须包含当天日期和"今天""最新"等限定词
2. **来源时间核实**：每条新闻的出处时间必须 **直接来自搜索结果中的日期字段**，严禁编造
3. **事件日期双重检查**（最关键）：
   - 即使文章发布于今天，如果报道的**事件**不是今天或昨天发生的，**一律丢弃**
   - 例：今天是3月23日，一篇3月23日发布的文章回顾了3月15日的3·15晚会 → **丢弃**
   - 例：今天3月23日的文章回顾上周发布的某产品 → **丢弃**
   - 关键判断：看新闻正文中提到的具体日期/时间，是否在过去24小时内
4. **丢弃「回顾/盘点/评论」类文章**：
   - 标题含"回顾""盘点""总结""复盘""一文读懂"等 → 大概率是旧事件的二次加工
   - AI板块特别注意：某模型"发布"但其实数周/数月前已发布的 → 丢弃
5. **宁缺毋滥**：如果对某条新闻是否是最新的有任何疑问，宁可不用

## 新闻重要性排序机制

按以下优先级从高到低排序：
1. **国家/全球级政策变动**（央行利率、贸易协定、战争/停火、重大法案）
2. **重大突发事件**（自然灾害、重大事故、领导人会晤）
3. **产业级影响**（万亿级市场变动、头部公司重大战略、颠覆性技术发布）
4. **行业热点**（AI大模型发布、芯片禁令、新能源突破）
5. **区域动态**（省市政策、基建进展、文旅经济）

每个板块内按重要性降序排列，最重要的放第一条。

## 新闻来源要求

### 国际新闻：必须从国际通讯社/门户获取第一手报道
- **首选**：Reuters、AP（美联社）、Bloomberg、AFP（法新社）
- **次选**：BBC、CNN、Financial Times、WSJ、The Guardian、Al Jazeera
- **可用**：新华社国际频道（仅当国际源不足时补充）
- ❌ **禁止**：不要用中国国内媒体的"国际新闻转述"作为国际板块来源

### 国内新闻：权威中央媒体+财经媒体
- 新华社、人民日报、央视、财联社、界面新闻、澎湃新闻、第一财经

### 本地新闻：云南/昆明官方+本地媒体
- 云南日报、春城晚报、昆明信息港、云南网、云南发布

### AI/科技：专业科技媒体
- 36氪、量子位、机器之心、TechCrunch、The Verge、MIT Tech Review

⚠️ 来源必须真实存在且可追溯，严禁虚构来源名称
⚠️ 国际板块的新闻来源必须是国际媒体，不能用国内媒体的国际新闻转载

**今日一句：**
- 中文名言，有价值
- 检查最近使用记录，避免重复
- 可从新闻中提取相关金句

## 质量检查清单

1. ✅ 标题使用 `indigo` 主题色
2. ✅ 副标题显示日期和星期
3. ✅ `"AI 生成"` turquoise 标签
4. ✅ `schema: "2.0"` 声明
5. ✅ 天气三栏布局（气温/天气/湿度）
6. ✅ 每个新闻板块有彩色背景标题栏
7. ✅ 5 个板块顺序正确
8. ✅ 国际/国内/本地/AI 各 **3-4 条**
9. ✅ 每条有粗体标题 + 摘要 + **真实出处+真实时间**
10. ✅ 所有新闻在 **24 小时内**（基于搜索结果中的日期，非编造）
11. ✅ 新闻按重要性降序排列
12. ✅ 来源来自权威大型门户网站
13. ✅ 今日一句居中+紫色调背景
14. ✅ 卡片 JSON 通过 `json.loads(json.dumps(card))` 验证
15. ✅ 通过飞书 API 直接发送（非 message tool）
16. ✅ **不包含** `__COMMENT` 行

## 硬性规则

- ❌ 不用 message tool 发卡片（card 参数有 bug）
- ❌ 不用 markdown/text 发送
- ❌ 天气不作为新闻条目
- ❌ 不加"影响解读""今日关注"等额外板块
- ❌ 不用过期新闻、旧闻翻炒
- ❌ 不并发搜索
- ❌ 不触发视频渲染
- ❌ elements 数组中不要放字符串（注释），只放组件对象
- ❌ 严禁编造新闻时间戳，必须从搜索结果中提取真实时间
- ❌ 严禁使用非权威来源或虚构来源名称
