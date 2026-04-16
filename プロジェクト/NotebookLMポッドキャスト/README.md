# NotebookLMポッドキャスト プロジェクト

## 目的
- Masaさんが興味あるトピックを話すだけで、
  - 梓がトピックを具体化
  - 質の高いソースをリサーチ
  - NotebookLMにソースを登録
  - NotebookLMのPodcast機能（Audio Overview）を呼び出し
- という一連の流れを **MCP連携込み** で半自動化し、
  - 「自分専用の学習Podcast」を量産できるようにする。

## 理想のワークフロー
1. Masa: 「◯◯についてのPodcastが欲しい」と梓に伝える。
2. 梓: 3〜5個の質問でトピックを具体化（対象・レベル・視点など）。
3. 梓: Web検索などでソース候補（記事・PDF・YouTube等）をリサーチし、ログにまとめる。
4. 梓 or Claude Code: MCP経由で NotebookLM にアクセスし、
   - ノートブックを作成 or 既存ノートブックを選択
   - ソースURLやテキストを追加
   - Podcast（Audio Overview）の生成をトリガー
5. NotebookLM: Podcastを生成（長め／初心者向けなど設定）。
6. Masa: NotebookLM上でPodcastを再生して聞く（公開は目的としない）。

## 現状の前提
- NotebookLM は Masaさんの Google アカウントで利用可能。
- OpenClaw（梓）はローカルMac mini上で稼働中。
- NotebookLM への直接操作は、MCPサーバとskill定義を通じて行う方針。

---

## 当面のタスク

1. MCPサーバ / CLI のセットアップ方針整理
   - `notebooklm-mcp-cli` の GitHub README を読み、
     - 対応している操作（list notebooks, add source, create podcast など）
     - OpenClaw向け skill ファイルのインストール手順
     を把握する。

2. 環境設計
   - NotebookLM MCPサーバをどこで動かすか決める（Mac mini上で常駐）。
   - 認証方法（GoogleアカウントOAuth）の扱いを確認する。

3. 最小ユースケースの実装
   - 1トピック分について：
     - ノートブック作成
     - ソースの1〜2件登録
     - Podcast生成トリガー
     までを MCP 経由で通す。

4. 通常運用フローのテンプレ化
   - 梓が Masaさんに聞く質問テンプレート
   - ソースリサーチログのフォーマット
   - NotebookLM MCPへの呼び出しパターン（CLI or skill）のテンプレ

詳しいMCP連携のメモは `MCP連携メモ.md` に分けて記録していく。