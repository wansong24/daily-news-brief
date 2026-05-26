#!/usr/bin/env python3
"""Send a Feishu interactive card from a JSON file.

Default config:
  ~/.codex/private/feishu_morning_brief.json

Optional environment override:
  FEISHU_CONFIG_FILE

Usage:
  python scripts/send_feishu_card.py card.json
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path


AUTH_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_URL = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
DEFAULT_CONFIG_FILE = Path.home() / ".codex" / "private" / "feishu_morning_brief.json"


def post_json(url: str, payload: dict, token: str | None = None) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def load_credentials() -> tuple[str, str, str]:
    config_path = Path(os.environ.get("FEISHU_CONFIG_FILE", DEFAULT_CONFIG_FILE))
    if not config_path.exists():
        raise SystemExit(f"Missing Feishu config file: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)
    app_id = config.get("FEISHU_APP_ID")
    app_secret = config.get("FEISHU_APP_SECRET")
    chat_id = config.get("FEISHU_CHAT_ID")

    missing = [
        name
        for name, value in {
            "FEISHU_APP_ID": app_id,
            "FEISHU_APP_SECRET": app_secret,
            "FEISHU_CHAT_ID": chat_id,
        }.items()
        if not value
    ]
    if missing:
        raise SystemExit(f"Missing Feishu credentials: {', '.join(missing)}")
    return app_id, app_secret, chat_id


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: send_feishu_card.py card.json")

    app_id, app_secret, chat_id = load_credentials()

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
