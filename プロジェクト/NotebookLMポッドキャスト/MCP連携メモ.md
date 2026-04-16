# NotebookLM × MCP 連携メモ

## 使う予定のコンポーネント

- NotebookLM（Google製）
  - 機能: ノートブック作成、ソース追加（PDF, URL, YouTube, 音声など）、Audio Overview（Podcast風オーディオ）生成
- notebooklm-mcp-cli（外部MCPサーバ）
  - 役割: NotebookLMに対する MCP インターフェースを提供
  - 対応クライアント: OpenClaw, Claude Code, Codex 等（README記載）
- OpenClaw（梓）
  - 役割: Masaさんとの対話・プロジェクト管理・MCP経由でのNotebookLM操作のオーケストレーション

## 想定するセットアップ手順（高レベル）

1. notebooklm-mcp-cli のインストール
   - 例: `uvx --from notebooklm-mcp-cli nlm ...` 形式のコマンド（正確な手順はGitHub README参照）。

2. Googleアカウントで NotebookLM にログイン
   - `nlm login` のようなコマンドでブラウザが開き、NotebookLM/Google認証を完了させる。

3. OpenClaw 用 skill 定義のインストール
   - 例: `nlm skill install openclaw`
   - これにより、OpenClawから `notebooklm` MCPツールを呼び出せるようになる想定。

4. OpenClaw 側で MCPツールの認識確認
   - `openclaw status` や関連ログで、`notebooklm` ツールが有効になっているか確認。

## ワークフロー中でのMCPの使い方（理想）

1. **ノートブックの作成 / 選択**
   - メソッド例: `create_notebook(title, description)` / `list_notebooks()`

2. **ソースの追加**
   - メソッド例: `add_source(notebook_id, url, kind)`
   - kind: `web`, `youtube`, `pdf`, など

3. **Podcast（Audio Overview）の生成トリガー**
   - メソッド例: `create_podcast(notebook_id, style, audience, length)`
   - style/audience/length は NotebookLM のUIで指定できるオプションに対応させる。

4. **生成結果の取得**
   - メソッド例: `get_podcast(notebook_id, podcast_id)`
   - 戻り値として、再生用リンク or NotebookLM内のリソースIDを受け取り、Masaさんに伝える。

※ 具体的なメソッド名・パラメータは notebooklm-mcp-cli の README / スキーマ定義を要確認。

## セキュリティ・運用上の注意

- Googleアカウント認証情報は notebooklm-mcp-cli 側で安全に保持し、OpenClaw側には生のトークンを渡さない。
- MCPサーバ（notebooklm-mcp-cli）は、Mac mini 上でのみlistenする（ローカルホスト）構成にする。
- NotebookLMに投入するソースは、公開情報 or 個人利用の範囲に収まるものを基本とし、機密情報は扱わない前提で設計する。

---

今後、実際に notebooklm-mcp-cli のREADMEやスキーマを確認したら、
- 利用可能メソッド一覧
- サンプル呼び出しペイロード
- OpenClawからの呼び出し例

をこのファイルに追記していく。