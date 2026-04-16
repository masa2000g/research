#!/usr/bin/env python3
"""
Step 1: Googleアカウントにログインするためだけのスクリプト。
ブラウザが開くので手動でログイン。ログインしたらブラウザを閉じてOK。
プロファイルにログイン状態が保存される。
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

PROFILE_DIR = Path.home() / ".playwright-profiles" / "google"

def main():
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            headless=False,
            args=["--window-size=1280,900"],
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.new_page()
        page.goto("https://accounts.google.com", wait_until="domcontentloaded", timeout=30000)
        print("ブラウザが開きました。Googleアカウントにログインしてください。")
        print("ログイン完了後、ブラウザを閉じてください（自動で終了します）。")
        try:
            page.wait_for_timeout(600000)  # 10分待つ
        except Exception:
            pass
        ctx.close()

if __name__ == "__main__":
    main()
