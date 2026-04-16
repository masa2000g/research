---
name: daily-intelligence
description: デイリーインテリジェンス（毎朝のニュースブリーフィング）のパイプライン実行、品質管理、および配信。ニュースの収集(collect)、正規化(normalize)、編集要約(editorial)、HTML生成(assemble)の一連のワークフローを管理し、GitHub Pagesへの公開とTelegramへの通知を行う。ニュース品質（特に日本語要約の質）の低下や、生成時のタイムアウトが発生した際の対応も含む。
---

# Daily Intelligence Skill

このスキルは、マサさんのためのニュースブリーフィングシステム「Daily Intelligence」を安定運用し、高品質なレポートを提供するための手順をまとめたものです。

## ワークフロー概要

メインの操作は `/Users/takehara/Projects/masa-knowledge/` ディレクトリで行います。

### 1. パイプラインの実行
通常は `build_daily_intelligence.js` を使用して、状況に応じた最適なステージから開始します。

```bash
# 基本実行（今日の日付で、不足しているステージから開始）
node scripts/build_daily_intelligence.js

# フルリビルド（全ステージを強制実行）
node scripts/build_daily_intelligence.js --full

# 特定の日付を指定
node scripts/build_daily_intelligence.js --date YYYY-MM-DD
```

### 2. 品質の管理と修正
レポートの品質に問題がある場合（要約が英語のまま、内容が薄いなど）、以下の手順で修正します。

- **要約の再生成**: `staged/YYYY-MM-DD.json` を削除してから `editorial` ステージを再実行するか、`--full` オプションで回します。
- **プロンプトの調整**: 編集ロジックや語りかけのトーンを変更したい場合は、`scripts/editorial.js` または関連するプロンプト定義を修正します。

### 3. トラブルシューティング
- **ETIMEDOUT (Claude API)**: 大量のトピックを一度に処理しようとすると発生しやすいため、リトライを行うか、重要度の高いトピックに絞り込む設定を確認してください。
- **GitHub Pages 404**: 公開URLは `https://masa2000g.github.io/research/daily-intelligence/` です。`gitSyncToResearchPages` 関数が正しく実行され、`research-pages` リポジトリに push されているか確認してください。

## 参照ファイル
- **実装詳細**: `references/pipeline-specs.md` (パイプラインの各ステージの仕様)
- **ソース定義**: `/Users/takehara/Projects/masa-knowledge/sources/intelligence-sources.json`
