---
name: browser-control
description: |
  Playwrightを使ったブラウザ操作スキル。ページを開く、検索する、スクリーンショットを撮る、
  フォームに入力する、ボタンをクリックするなど、汎用的なブラウザ操作を提供する。
  X投稿やWebアプリ操作など、GUI操作が必要なタスクに使う。
---

# browser-control Skill

## 概要

Playwright (Python) を使って、ブラウザを自動操作するスキル。
エージェントが「ブラウザを開いて○○してほしい」と頼まれたとき、このスキルを使う。

## 前提

- Python 3.10+ がインストール済み
- Playwright がインストール済み (`pip install playwright && playwright install chromium`)
- 永続プロファイル: `~/.playwright-profiles/<profile-name>/` にログイン状態を保持

## 使い方

### インストール確認

```bash
which python3 && python3 -c "from playwright.sync_api import sync_playwright; print('OK')"
```

もし入っていなければ:
```bash
pip install playwright && playwright install chromium
```

### 提供するスクリプト

すべてのスクリプトは `scripts/` に配置。

#### 1. `browse.py` — 汎用ブラウザ操作

```bash
# ページを開いてスクリーンショット
python3 scripts/browse.py open "https://example.com" --screenshot /tmp/shot.png

# ページを開いてテキスト内容を取得（エージェントが読める形式で）
python3 scripts/browse.py read "https://example.com"

# ページ内でクリック
python3 scripts/browse.py click "https://example.com" --selector "button.submit"

# テキスト入力
python3 scripts/browse.py type "https://example.com" --selector "input[name=q]" --text "検索ワード"

# Google検索してトップ結果を返す
python3 scripts/browse.py search "検索クエリ"
```

#### 2. `x_post.py` — X (Twitter) 投稿

既存の `X-auto-post/playwright_x_post.py` を改良したもの。

```bash
# 投稿テキストをセットして確認待ち（手動Post前提）
python3 scripts/x_post.py --text "投稿内容" --confirm

# 完全自動投稿（ユーザー承認済みの場合のみ）
python3 scripts/x_post.py --text "投稿内容" --auto
```

## プロファイル管理

サイトごとにログイン状態を分離:

| プロファイル名 | 用途 |
|---|---|
| `default` | 一般的なブラウジング |
| `x-twitter` | X/Twitter用（既存の `~/.playwright-x-profile` から移行） |
| `google` | Google系サービス用 |

プロファイルパス: `~/.playwright-profiles/<name>/`

## エージェントへの指示

このスキルが使えるとき:
- 「このページ開いて」「このサイトの内容教えて」→ `browse.py read`
- 「スクショ撮って」→ `browse.py open --screenshot`
- 「Xに投稿して」→ `x_post.py`（外部発信なので必ずユーザー承認を取る）
- 「ログインして」→ `browse.py open` でheadlessをオフにして手動ログインを案内
- Web検索で情報確認したい → `browse.py search` または Brave Search API

**重要:** スクリプトが存在するか `ls` で確認してから使うこと。
なければこのSKILL.mdを読んで必要なスクリプトを作成する。

## セキュリティ

- 外部への発信（投稿、メール送信、購入等）は**必ずユーザー承認を取る**
- 読み取り専用の操作（ページ閲覧、スクショ、テキスト抽出）は自律的に実行してOK
- パスワードやクレデンシャルをログやメモリに保存しない
