#!/usr/bin/env python3
"""
Google Calendar 操作スクリプト for OpenClaw.

Usage:
  python3 gcal.py auth            # 初回OAuth認証（ブラウザが開く）
  python3 gcal.py list            # 今日〜7日後の予定一覧
  python3 gcal.py today           # 今日の予定
  python3 gcal.py add "タイトル" "2026-04-07T09:00:00" "2026-04-07T10:00:00" ["説明"]
  python3 gcal.py quick "明日の10時にミーティング"   # クイック追加
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDS_DIR = Path.home() / ".openclaw" / "credentials"
CLIENT_SECRET = CREDS_DIR / "google-calendar-oauth.json"
TOKEN_FILE = CREDS_DIR / "google-calendar-token.json"

JST = timezone(timedelta(hours=9))


def get_service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                print(f"❌ {CLIENT_SECRET} が見つかりません。", file=sys.stderr)
                print("   Google Cloud Console から OAuth クライアントIDのJSONをダウンロードし、", file=sys.stderr)
                print(f"   {CLIENT_SECRET} に配置してください。", file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())
        print(f"✅ トークン保存: {TOKEN_FILE}")

    return build("calendar", "v3", credentials=creds)


def cmd_auth(_args):
    service = get_service()
    result = service.calendarList().list().execute()
    calendars = result.get("items", [])
    print(f"✅ 認証成功！ {len(calendars)} 個のカレンダーにアクセス可能:")
    for cal in calendars:
        primary = " ⭐" if cal.get("primary") else ""
        print(f"  - {cal['summary']}{primary}")


def cmd_list(args):
    service = get_service()
    now = datetime.now(JST)
    end = now + timedelta(days=args.days)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])
    if not events:
        print(f"📅 {args.days}日間の予定はありません。")
        return

    results = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end_time = event["end"].get("dateTime", event["end"].get("date"))
        results.append({
            "id": event["id"],
            "title": event.get("summary", "(無題)"),
            "start": start,
            "end": end_time,
            "description": event.get("description", ""),
            "location": event.get("location", ""),
        })

    print(json.dumps(results, ensure_ascii=False, indent=2))


def cmd_today(_args):
    class FakeArgs:
        days = 1
    cmd_list(FakeArgs())


def cmd_add(args):
    service = get_service()

    event = {
        "summary": args.title,
        "start": {
            "dateTime": args.start,
            "timeZone": "Asia/Tokyo",
        },
        "end": {
            "dateTime": args.end,
            "timeZone": "Asia/Tokyo",
        },
    }
    if args.description:
        event["description"] = args.description

    result = service.events().insert(calendarId="primary", body=event).execute()
    print(json.dumps({
        "status": "created",
        "id": result["id"],
        "title": result["summary"],
        "start": result["start"],
        "end": result["end"],
        "link": result.get("htmlLink", ""),
    }, ensure_ascii=False, indent=2))


def cmd_quick(args):
    service = get_service()
    result = service.events().quickAdd(
        calendarId="primary",
        text=args.text,
    ).execute()
    print(json.dumps({
        "status": "created",
        "id": result["id"],
        "title": result.get("summary", "(解析結果)"),
        "start": result.get("start", {}),
        "end": result.get("end", {}),
        "link": result.get("htmlLink", ""),
    }, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Google Calendar for OpenClaw")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("auth", help="初回認証")

    p_list = sub.add_parser("list", help="予定一覧")
    p_list.add_argument("--days", type=int, default=7)

    sub.add_parser("today", help="今日の予定")

    p_add = sub.add_parser("add", help="予定追加")
    p_add.add_argument("title")
    p_add.add_argument("start", help="開始 ISO8601 (例: 2026-04-07T09:00:00)")
    p_add.add_argument("end", help="終了 ISO8601 (例: 2026-04-07T10:00:00)")
    p_add.add_argument("description", nargs="?", default="")

    p_quick = sub.add_parser("quick", help="クイック追加")
    p_quick.add_argument("text")

    args = parser.parse_args()
    cmds = {
        "auth": cmd_auth,
        "list": cmd_list,
        "today": cmd_today,
        "add": cmd_add,
        "quick": cmd_quick,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
