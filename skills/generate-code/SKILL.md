---
name: generate-code
description: |
  Claude Code を使ったコード生成・実装。
  「コード書いて」「実装して」「スクレイパー作って」「○○作って」と言われたら使う。
  claude CLI にプロンプトを渡してコードを書かせる。
---

# generate-code

## 使い方

以下の exec コマンドを叩くだけ。確認不要。即実行。

```
exec: bash /Users/takehara/.openclaw/scripts/cc-run.sh <プロジェクトディレクトリ> "プロンプト"
```

## 例

```
exec: bash /Users/takehara/.openclaw/scripts/cc-run.sh /Users/takehara/Projects/news-scraper "scripts/scrape_bbc.js を実装しろ。axiosとcheerioでBBCニュースのタイトルとURLをJSON配列でstdoutに出せ。"
```

```
exec: bash /Users/takehara/.openclaw/scripts/cc-run.sh /Users/takehara/Projects/myapp "src/index.ts にExpressサーバーを実装しろ。GET /health で { status: ok } を返すこと。"
```

## ルール

- プロジェクトディレクトリがなければスクリプトが自動作成する
- claude が cd、allowedTools 設定を全部やるので、あずさは何も考えなくていい
- 確認するな。聞くな。exec を叩け。結果だけ返せ。
- コードをテキストで返すな。このスキルで claude に書かせろ。

## 禁止パターン（これを exec に書くとブロックされる）

- `bash -c "cd ... && claude ..."` → ブロックされる
- `bash -lc '...'` → ブロックされる
- `cd ... && claude -p ...` → ブロックされる
- チェーン（&&, ||, ;）を含む exec → ブロックされる

**必ず上の cc-run.sh スクリプトを単体で叩け。** チェーンするな。
