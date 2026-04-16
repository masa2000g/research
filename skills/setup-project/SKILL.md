---
name: setup-project
description: |
  Node.jsプロジェクトの初期化とパッケージインストール。
  「プロジェクト作って」「○○インストールして」「セットアップして」と言われたら使う。
  npm init、npm install を実行する。
---

# setup-project

## 使い方

以下の exec コマンドを叩くだけ。確認不要。即実行。

```
exec: bash /Users/takehara/.openclaw/scripts/npm-setup.sh <プロジェクトディレクトリ> [パッケージ名...]
```

## 例

```
exec: bash /Users/takehara/.openclaw/scripts/npm-setup.sh /Users/takehara/Projects/news-scraper axios cheerio
```

```
exec: bash /Users/takehara/.openclaw/scripts/npm-setup.sh /Users/takehara/Projects/myapp express dotenv cors
```

## ルール

- プロジェクトディレクトリがなければスクリプトが自動作成する
- package.json がなければ npm init -y を自動実行する
- 確認するな。聞くな。exec を叩け。結果だけ返せ。

## 禁止パターン（これを exec に書くとブロックされる）

- `bash -c "cd ... && npm ..."` → ブロックされる
- `bash -lc '...'` → ブロックされる
- `cd ... && npm install` → ブロックされる
- チェーン（&&, ||, ;）を含む exec → ブロックされる

**必ず上の npm-setup.sh スクリプトを単体で叩け。** チェーンするな。
