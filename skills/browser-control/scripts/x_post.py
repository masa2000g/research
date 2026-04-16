#!/usr/bin/env python3
"""
X (Twitter) 投稿スクリプト for OpenClaw browser-control skill.

Usage:
  python3 x_post.py --text "投稿内容" [--confirm] [--auto]

  --confirm: テキスト入力後、手動でPostボタンを押す（デフォルト）
  --auto:    自動でPostボタンまで押す（ユーザー承認済みの場合のみ使用すること）
"""

import argparse
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

X_URL = "https://x.com/home"
PROFILE_DIR = Path.home() / ".playwright-profiles" / "x-twitter"


def main():
    parser = argparse.ArgumentParser(description="Post to X (Twitter)")
    parser.add_argument("--text", required=True, help="Post content")
    parser.add_argument("--auto", action="store_true", help="Auto-click Post button")
    parser.add_argument("--confirm", action="store_true", default=True,
                        help="Wait for manual Post (default)")
    args = parser.parse_args()

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            headless=False,
        )
        page = ctx.new_page()
        page.goto(X_URL, wait_until="networkidle", timeout=60000)

        # 投稿ボックスを探す
        textarea = page.get_by_role("textbox").first
        textarea.click()
        textarea.fill(args.text)
        print(f"Text filled ({len(args.text)} chars)")

        if args.auto:
            # Postボタンをクリック
            post_btn = page.get_by_test_id("tweetButtonInline")
            if not post_btn.is_visible():
                post_btn = page.locator('[data-testid="tweetButton"]')
            post_btn.click()
            page.wait_for_timeout(3000)
            print("Posted successfully.")
            ctx.close()
        else:
            print("Text is ready. Please click 'Post' manually in the browser.")
            print("Press Ctrl+C when done.")
            try:
                page.wait_for_timeout(3600000)
            except KeyboardInterrupt:
                pass
            ctx.close()


if __name__ == "__main__":
    main()
