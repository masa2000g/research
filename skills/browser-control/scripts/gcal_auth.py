#!/usr/bin/env python3
"""
Google Calendar OAuth認証（SSH越し対応版）。
URLが表示されるので、手元のブラウザで開いてログイン→許可→コードを貼り付ける。
"""
import sys
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDS_DIR = Path.home() / ".openclaw" / "credentials"
CLIENT_SECRET = CREDS_DIR / "google-calendar-oauth.json"
TOKEN_FILE = CREDS_DIR / "google-calendar-token.json"


def main():
    if not CLIENT_SECRET.exists():
        print(f"❌ {CLIENT_SECRET} が見つかりません。")
        print()
        print("Google Cloud Console で以下を実施してください:")
        print("  1. https://console.cloud.google.com/ にアクセス")
        print("  2. プロジェクト作成 (名前: openclaw-calendar)")
        print("  3. 「APIとサービス」→「ライブラリ」→ Google Calendar API を有効化")
        print("  4. 「APIとサービス」→「認証情報」→「認証情報を作成」→「OAuthクライアントID」")
        print("     - アプリの種類: デスクトップアプリ")
        print("     - 名前: OpenClaw")
        print("  5. 作成後「JSONをダウンロード」→ 以下に配置:")
        print(f"     {CLIENT_SECRET}")
        print()
        print("  ※ 初回は「OAuth同意画面」の設定も必要です（外部 → テストユーザーに自分を追加）")
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    creds = flow.run_local_server(port=18791, open_browser=False)

    TOKEN_FILE.write_text(creds.to_json())
    print(f"\n✅ 認証成功！トークン保存: {TOKEN_FILE}")

    # 動作確認
    from googleapiclient.discovery import build
    service = build("calendar", "v3", credentials=creds)
    result = service.calendarList().list().execute()
    calendars = result.get("items", [])
    print(f"📅 {len(calendars)} 個のカレンダーにアクセス可能:")
    for cal in calendars:
        primary = " ⭐" if cal.get("primary") else ""
        print(f"  - {cal['summary']}{primary}")


if __name__ == "__main__":
    main()
