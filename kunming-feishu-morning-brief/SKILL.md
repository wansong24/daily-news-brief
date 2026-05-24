---
name: kunming-feishu-morning-brief
description: Generate and send a premium Chinese Feishu morning brief for a user in Kunming, Yunnan. Use when asked to create, revise, schedule, test, or push a daily news briefing with international, China, Yunnan/Kunming local, AI news, weather, clothing advice, source links, real news images, and non-repeating Mao Zedong quotes.
---

# Kunming Feishu Morning Brief

## Purpose

Create a polished mobile-first Feishu card morning brief for a user in Kunming. The brief must feel like a concise premium news magazine: important news only, each key story paired with a relevant event/person/site image, clear source attribution, local weather, practical clothing advice, and one non-repeating Mao Zedong quote.

## Workflow

1. Verify the date, timezone, and coverage window.
   - Default timezone: Asia/Shanghai.
   - Default delivery time: 08:30.
   - Default window: the previous 24 hours.
2. Collect current information from reliable sources.
   - International: AP, Reuters, BBC, Al Jazeera, Axios, official agencies.
   - China: Xinhua, CCTV, CNR, official ministry or program sites.
   - Yunnan/Kunming: Yunnan provincial sources, Kunming official/local media, China News, weather services.
   - AI: official company blogs, product newsrooms, TechCrunch/The Verge only when they provide primary reporting or clear attribution.
3. Select only important items.
   - Prefer 1-2 international, 2 China, 1-2 Yunnan/Kunming, 1-2 AI.
   - Do not pad a section with weak stories. Say that no sufficiently important item was found if needed.
4. Pair only selected stories with real, verified news-related images.
   - Use an image only when it clearly matches that exact story: event/site photo, named person photo, official press image, rescue/site image, spacecraft/launch image, product screenshot, or article `og:image` from the same article.
   - Prefer fewer images over weak matches. If the match is uncertain, omit the image and use text only.
   - Do not use abstract title cards, generic decorative images, cross-section images, keyword-only matches, or fallback images.
   - Never use an international figure/event image for a Yunnan/Kunming local story, or any other cross-topic/cross-location substitute.
5. Write each item as:
   - Bold section label/title.
   - 2-4 mobile-friendly sentences explaining what happened and why it matters.
   - A short source line with source names and links when available.
6. Add local service content.
   - Current Kunming weather, daily high/low, wind/rain risk.
   - Practical clothing advice for commuting and outdoor activity.
7. Add one Mao Zedong quote.
   - Use `references/mao-quotes.md`.
   - Track the quote number in the message or external state if available.
   - Do not repeat the prior quote when the previous number is known.
8. Send to Feishu.
   - Use `scripts/send_feishu_card.py` when a card JSON file is ready.
   - Read API credentials from environment variables, never hardcode secrets.

## Feishu Card Standard

Use an interactive card with:

- Header: `昆明晨报｜YYYY年M月D日`.
- First block: date, coverage window, Kunming weather and clothing advice.
- Then story blocks in this order: international, China, Yunnan/Kunming, AI.
- For each story with a verified image: `img` element immediately before the matching story text.
- For stories without a verified image: omit the image entirely.
- End blocks: `今日判断` and `每日一句`.
- Mobile style: short paragraphs, clear bold labels, restrained separators, no wall-of-text.

## Required Environment

For direct Feishu API sends, expect:

```bash
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_CHAT_ID=oc_xxx
```

Never commit these values. If a secret was pasted into a chat or log, advise the user to rotate it before long-term automation.

## Resources

- `scripts/send_feishu_card.py`: sends a prebuilt Feishu interactive card JSON to a chat and optionally uploads local/remote images.
- `references/card-style.md`: detailed writing and layout standard.
- `references/mao-quotes.md`: quote rotation list.
