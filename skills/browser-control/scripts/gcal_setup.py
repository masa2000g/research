#!/usr/bin/env python3
"""
Google Cloud Console で Calendar API プロジェクトをセッ��アップするスクリプト。
Playwrightで可能な範囲を自動化し、手動操作が必要な部分はガイドする。

Step 1: Google Cloud Console にログイン状態を確認
Step 2: プロジェクト作成
Step 3: Calendar API 有効化
Step 4: OAuth同意画面設定
Step 5: OAuth クライアントID作成 → credentials.json 保存
"""

import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout

PROFILE_DIR = Path.home() / ".playwright-profiles" / "google"
CREDS_OUTPUT = Path.home() / ".openclaw" / "credentials" / "google-calendar-oauth.json"
PROJECT_ID = "openclaw-calendar"


def wait_and_log(page, msg, seconds=3):
    print(f"  → {msg}")
    page.wait_for_timeout(seconds * 1000)


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

        # Step 1: Googleログイン確認
        print("=" * 60)
        print("Step 1: Googleアカウントのログイン確認")
        print("=" * 60)
        page.goto("https://accounts.google.com", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)

        # ログインしているか確認
        url = page.url
        if "signin" in url or "ServiceLogin" in url:
            print("\n⚠️  Googleにログインしていません。")
            print("   ブラウザ画面でGoogleアカウントにログインしてください。")
            print("   ログイン完了後、Enterキーを押してください...")
            input()
            page.wait_for_timeout(2000)
        else:
            print("✅ Googleにログイン済み")

        # Step 2: Google Cloud Console → プロジェクト作成
        print("\n" + "=" * 60)
        print("Step 2: Google Cloud Console でプロジェクト作成")
        print("=" * 60)

        page.goto(
            "https://console.cloud.google.com/projectcreate",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        page.wait_for_timeout(5000)

        # 利用規約が出る場合
        try:
            terms_checkbox = page.locator("input[type='checkbox']").first
            if terms_checkbox.is_visible(timeout=3000):
                terms_checkbox.check()
                page.wait_for_timeout(1000)
                agree_btn = page.locator("button:has-text('Agree'), button:has-text('同意')")
                if agree_btn.is_visible(timeout=2000):
                    agree_btn.click()
                    page.wait_for_timeout(3000)
        except PwTimeout:
            pass

        # プロジェクト名入力
        try:
            name_input = page.locator("input[aria-label*='Project name'], input[aria-label*='プロジェクト名'], input#p6ntest-name-input")
            if name_input.is_visible(timeout=5000):
                name_input.fill("")
                name_input.fill(PROJECT_ID)
                wait_and_log(page, f"プロジェクト名: {PROJECT_ID}", 2)

                # 作成ボタン
                create_btn = page.locator("button:has-text('Create'), button:has-text('作成')")
                if create_btn.is_visible(timeout=3000):
                    create_btn.click()
                    wait_and_log(page, "プロジェクト作成中...", 10)
                    print("✅ プロジェクト作成リクエスト送信")
                else:
                    print("⚠️  作成ボタンが見つかりません。手動で作成してください。")
            else:
                print("⚠️  プロジェクト名入力欄が見つかりません。")
                print("   既にプロジェクトが存在するか、UIが変わっている可能性があります。")
        except PwTimeout:
            print("⚠️  プロジェクト作成ページの読み込み���タイムアウト。手動で進めてください。")

        # Step 3: Calendar API 有効化
        print("\n" + "=" * 60)
        print("Step 3: Google Calendar API を有効化")
        print("=" * 60)

        page.goto(
            f"https://console.cloud.google.com/apis/library/calendar-json.googleapis.com?project={PROJECT_ID}",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        page.wait_for_timeout(5000)

        try:
            enable_btn = page.locator("button:has-text('Enable'), button:has-text('有効にする')")
            if enable_btn.is_visible(timeout=5000):
                enable_btn.click()
                wait_and_log(page, "Calendar API を有効化中...", 8)
                print("✅ Calendar API 有効化リクエスト送信")
            else:
                manage_btn = page.locator("button:has-text('Manage'), button:has-text('管理')")
                if manage_btn.is_visible(timeout=3000):
                    print("✅ Calendar API は���に有効です")
                else:
                    print("⚠️  有効化ボタンが見つかりません。手動で有効化してください。")
        except PwTimeout:
            print("⚠️  Calendar API ページの読み込みがタイムアウト。")

        # Step 4: OAuth同意画面
        print("\n" + "=" * 60)
        print("Step 4: OAuth同意画面の設定")
        print("=" * 60)

        page.goto(
            f"https://console.cloud.google.com/apis/credentials/consent?project={PROJECT_ID}",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        page.wait_for_timeout(5000)

        # External を選択
        try:
            external = page.locator("input[value='EXTERNAL'], mat-radio-button:has-text('External'), mat-radio-button:has-text('外部')")
            if external.is_visible(timeout=5000):
                external.click()
                page.wait_for_timeout(1000)
                create_btn = page.locator("button:has-text('Create'), button:has-text('作成')")
                if create_btn.is_visible(timeout=3000):
                    create_btn.click()
                    page.wait_for_timeout(5000)
            print("  → OAuth同意画面の設定ページに移動しました")
        except PwTimeout:
            print("  → OAuth同意画面は設定済みか、UIが異なります")

        # アプリ名設定
        try:
            app_name = page.locator("input[formcontrolname='displayName'], input[aria-label*='App name'], input[aria-label*='アプリ名']")
            if app_name.is_visible(timeout=3000):
                app_name.fill("OpenClaw Calendar")
                wait_and_log(page, "アプリ名: OpenClaw Calendar", 1)

                # ユーザーサポートメール
                email_input = page.locator("input[formcontrolname='email'], input[type='email']").first
                if email_input.is_visible(timeout=2000):
                    # メールアドレスが必要 — ��ーザーに聞く
                    print("\n⚠️  サポート用メールアドレスの入力が必要です。")
                    print("   ブラウザ画面で入力し、ページ下部の「保存して次へ」を押してください。")
                    print("   完了したらEnterキーを押してください...")
                    input()
        except PwTimeout:
            pass

        # Step 5: OAuth クライアントID作成
        print("\n" + "=" * 60)
        print("Step 5: OAuth クライアントID の作成")
        print("=" * 60)

        page.goto(
            f"https://console.cloud.google.com/apis/credentials/oauthclient?project={PROJECT_ID}",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        page.wait_for_timeout(5000)

        try:
            # アプリケーションタイプ: デスクトップアプリ
            type_select = page.locator("mat-select, [role='listbox']").first
            if type_select.is_visible(timeout=5000):
                type_select.click()
                page.wait_for_timeout(1000)
                desktop_opt = page.locator("mat-option:has-text('Desktop app'), mat-option:has-text('デスクトップ アプ��'), mat-option:has-text('Desktop')")
                if desktop_opt.is_visible(timeout=3000):
                    desktop_opt.click()
                    page.wait_for_timeout(1000)

                # 名前
                name_field = page.locator("input[formcontrolname='name'], input[aria-label*='Name'], input[aria-label*='名前']")
                if name_field.is_visible(timeout=2000):
                    name_field.fill("OpenClaw")
                    wait_and_log(page, "クライアント名: OpenClaw", 1)

                # 作成
                create_btn = page.locator("button:has-text('Create'), button:has-text('作成')")
                if create_btn.is_visible(timeout=3000):
                    create_btn.click()
                    page.wait_for_timeout(5000)
                    print("✅ OAuth クライアントID 作成リクエスト送信")

                    # JSON ダウンロードボタン
                    download_btn = page.locator("button:has-text('Download JSON'), button:has-text('JSON をダウンロード'), a:has-text('Download')")
                    if download_btn.is_visible(timeout=5000):
                        download_btn.click()
                        page.wait_for_timeout(3000)
                        print("✅ credentials.json ダウンロード開始")
                    else:
                        print("⚠️  JSONダウンロードボタンが見つかりません。")
                        print("   手動でダウンロードしてください。")
        except PwTimeout:
            print("⚠️  OAuth クライアントID 作成ページでタイムアウト。")

        print("\n" + "=" * 60)
        print("セットアップ完了！")
        print("=" * 60)
        print(f"\nブラウザは開いたままです。")
        print(f"必要に応じて手動で操作を完了してください。")
        print(f"\ncredentials.json をダウンロードしたら、以下に配置してください:")
        print(f"  {CREDS_OUTPUT}")
        print(f"\nCtrl+C で終了します。")

        try:
            page.wait_for_timeout(3600000)
        except KeyboardInterrupt:
            pass
        ctx.close()


if __name__ == "__main__":
    main()
