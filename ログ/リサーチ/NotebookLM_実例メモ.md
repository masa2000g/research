# リサーチログ: NotebookLM + PDF/動画 学習の実例

## 目的
- NotebookLM を使って、PDFやYouTube講義をまとめて学習している人の事例を把握する。
- 将来的に Masaさんの「学習プロジェクト」の設計に活かす。

## 見つかった主なパターン

1. PDF + YouTube + オーディオを混ぜて「知識ベース」を作る使い方
   - 参考: GeeksforGeeks の "Advanced Use Cases of NotebookLM"
   - ポイント:
     - 複数のPDF、YouTube動画、音声を NotebookLM に突っ込んで、トピックごとにノートブックを作る。
     - 例: 講義動画 + スライドPDF + 補助資料を一つのノートブックにまとめて、質問・要約・比較を行う。

2. NotebookLM × Claude Code 連携による高度なワークフロー
   - 参考: Substack 記事 "How to use NotebookLM with Claude Code: 5 demos + 50 use cases with prompts"
   - ポイント:
     - NotebookLM を情報の「ストレージ」として使い、Claude Code からMCPスキル経由でアクセスする例。
     - PDFやCSV、SWOT分析資料、メール下書きなどをNotebookLMに入れ、外部エージェントがそこから情報を引き出してレポート生成などを行っている。

3. 個人の学習ノート／知識ベースとして使うケース
   - 参考: NotebookLMの一般的なガイドや Reddit のユーザー事例
   - ポイント:
     - テーマ別ノートブック（例: アルゴリズム、マーケティング、歴史など）を作り、関連PDFや講義動画のリンクをまとめて投入。
     - 自分のメモや要約も一緒に入れておき、NotebookLMにクイズ・要約・比較説明をさせる運用。

## Masaさんへの示唆
- すでに世の中でも「PDF＋YouTubeをNotebookLMにまとめる」使い方は一般的になりつつある。
- 特に、NotebookLMを"データベース"として使い、外部エージェント（Claude Codeなど）と連携するパターンは、MCP連携を考える上で良い参考になりそう。
- 今後、NotebookLMのMCP連携を検討するときは、この辺りの事例をもう少し深掘りして、Masaさん用のワークフロー案（学習プロジェクト用）をまとめる。
