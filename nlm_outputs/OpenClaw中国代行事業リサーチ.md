# OpenClaw中国代行事業リサーチ NotebookLM 出力メモ

- Notebook ID: `e11e4e9c-7b8d-45d9-86a7-f083eab57f8e`
- Audio artifact ID (podcast): `063e14fb-cd1f-49d5-94a9-f6cab7d21a11`
- 生成元ソース:
  - MIT Technology Review: https://www.technologyreview.com/2026/03/11/1134179/china-openclaw-gold-rush/
  - Business Insider: https://www.businessinsider.com/china-openclaw-lobster-craze-uninstall-ai-agent-paid-side-hustle-2026-3
  - WIRED: https://www.wired.com/story/china-is-going-all-in-on-openclaw/
  - SCMP (uninstall 代行): https://www.scmp.com/tech/big-tech/article/3346397/chinas-openclaw-users-paid-install-viral-ai-agent-now-they-spend-remove-it
  - SCMP (一人会社／副業): https://www.scmp.com/tech/article/3347416/openclaw-government-support-fuels-rise-one-person-companies-china

現状の nlm CLI (version 0.1.12) には `nlm download` サブコマンドが存在しないため、この時点では CLI から mp3 を直接ダウンロードできない。

音声を取得する方法候補:

1. NotebookLM の Web UI から、上記 Notebook を開き、Audio/Podcast アーティファクト `063e14fb-...` を探して再生 or ダウンロード。
2. 将来の `notebooklm-mcp-cli` のバージョンで `nlm download audio <notebook> <artifact-id> --output podcast.mp3` が利用可能になったら、同じ Notebook/Artifact ID を使って mp3 を取得する。
