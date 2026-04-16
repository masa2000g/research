# Pipeline Specifications

Daily Intelligence パイプライン（v4）の各ステージの技術仕様です。

## Stage 1: Collect (収集)
- **スクリプト**: `scripts/collect.js`
- **内容**: `sources/intelligence-sources.json` に定義された各軸のRSS/Webソースから記事を収集。
- **出力**: `data/queue/YYYY-MM-DD.jsonl` (1記事1行のJSONL形式)
- **特徴**: 重複チェックを行い、新規記事のみを追記する。

## Stage 2: Normalize (正規化)
- **スクリプト**: `scripts/normalize.js`
- **内容**: キューから記事を読み込み、重複除去、メタデータの正規化、10軸への再分類を行う。
- **出力**: `data/normalized/YYYY-MM-DD.json`
- **オプション**: `--scraper` を指定すると外部スクレイパーの結果を統合。

## Stage 3: Editorial (編集)
- **スクリプト**: `scripts/editorial.js`
- **内容**: 
  1. 正規化済み記事をクラスタリングして「トピック」を生成。
  2. claude CLI を呼び出し、各軸のオーバービュー（語りかけ形式の要約・背景・展望）を生成。
  3. 各トピックの詳細（何が起きたか・なぜ重要か）を日本語で生成。
- **出力**: `data/staged/YYYY-MM-DD.json`
- **課題**: 英語ソースが多い場合に要約が英語に引きずられることがある。

## Stage 4: Assemble (組み立て)
- **スクリプト**: `scripts/render.js`
- **内容**: `staged` データから HTML レポートを生成。インデックスページ (`index.html`) も更新。
- **出力**: `docs/daily-intelligence/YYYY-MM-DD.html`

## Publish & Verify
- **GitHub Sync**: `docs/` の成果物を `research-pages` リポジトリへコピーして push。
- **HTTP Verify**: 公開された URL が HTTP 200 を返すか検証。
