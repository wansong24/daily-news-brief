#!/usr/bin/env python3
"""Send a Feishu interactive card from a JSON file.

Environment:
  FEISHU_APP_ID
  FEISHU_APP_SECRET
  FEISHU_CHAT_ID

Usage:
  python scripts/send_feishu_card.py card.json
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request


AUTH_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_URL = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"


def post_json(url: str, payload: dict, token: str | None = None) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: send_feishu_card.py card.json")

    app_id = require_env("FEISHU_APP_ID")
    app_secret = require_env("FEISHU_APP_SECRET")
    chat_id = require_env("FEISHU_CHAT_ID")

    with open(sys.argv[1], "r", encoding="utf-8") as file:
        card = json.load(file)

    token_response = post_json(AUTH_URL, {"app_id": app_id, "app_secret": app_secret})
    if token_response.get("code") != 0:
        raise SystemExit(json.dumps(token_response, ensure_ascii=False))

    response = post_json(
        MESSAGE_URL,
        {
            "receive_id": chat_id,
            "msg_type": "interactive",
            "content": json.dumps(card, ensure_ascii=False),
        },
        token_response["tenant_access_token"],
    )
    print(json.dumps(response, ensure_ascii=False, indent=2))
    return 0 if response.get("code") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
