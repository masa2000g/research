#!/bin/bash
# =============================================================
# work-timer.sh — 作業中定時報告タイマー
# 1分ごとにステータスファイルを読み取り Telegram に送信する
# =============================================================
# Usage:
#   bash work-timer.sh start "タスク名"   — タイマー開始
#   bash work-timer.sh stop               — タイマー停止＋終了通知
#   bash work-timer.sh status             — 現在の状態確認
#   bash work-timer.sh update "doing" "done" "next"  — ステータス更新
# =============================================================

STATUS_DIR="/Users/takehara/.openclaw/workspace/.work-status"
STATUS_FILE="$STATUS_DIR/current.md"
PID_FILE="$STATUS_DIR/timer.pid"
LOG_FILE="$STATUS_DIR/timer.log"
NOTIFY="bash /Users/takehara/.openclaw/scripts/telegram-notify.sh"
INTERVAL=60

ensure_dir() {
  [ -d "$STATUS_DIR" ] || mkdir -p "$STATUS_DIR"
}

cmd_start() {
  ensure_dir
  local TASK_NAME="${1:-作業中}"

  # Kill existing timer if running
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    kill "$(cat "$PID_FILE")" 2>/dev/null
    wait "$(cat "$PID_FILE")" 2>/dev/null
  fi

  # Initialize status file
  cat > "$STATUS_FILE" <<EOF
task: $TASK_NAME
started: $(date '+%Y-%m-%d %H:%M:%S')
---
🔄 やっていること: $TASK_NAME の準備中
✅ 完了したこと: なし
⏭️ 次にやること: $TASK_NAME に着手
EOF

  # Start background timer loop
  (
    COUNT=0
    while true; do
      sleep "$INTERVAL"
      COUNT=$((COUNT + 1))
      if [ ! -f "$STATUS_FILE" ]; then
        break
      fi
      # Read the body (everything after ---)
      BODY=$(sed -n '/^---$/,$ p' "$STATUS_FILE" | tail -n +2)
      TASK=$(head -1 "$STATUS_FILE" | sed 's/^task: //')
      ELAPSED="${COUNT}分経過"
      MSG="⏱️ 定時報告 [$ELAPSED] $TASK"$'\n'"$BODY"
      $NOTIFY "$MSG" >> "$LOG_FILE" 2>&1
    done
  ) &
  echo $! > "$PID_FILE"

  # Send start notification
  $NOTIFY "🔄 作業タイマー開始: $TASK_NAME（1分ごとに進捗報告します）"

  echo "✅ タイマー開始: $TASK_NAME (PID: $(cat "$PID_FILE"), interval: ${INTERVAL}s)"
}

cmd_stop() {
  if [ -f "$PID_FILE" ]; then
    local PID
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
      kill "$PID" 2>/dev/null
      wait "$PID" 2>/dev/null
    fi
    rm -f "$PID_FILE"

    # Send final report
    if [ -f "$STATUS_FILE" ]; then
      BODY=$(sed -n '/^---$/,$ p' "$STATUS_FILE" | tail -n +2)
      TASK=$(head -1 "$STATUS_FILE" | sed 's/^task: //')
      STARTED=$(sed -n '2p' "$STATUS_FILE" | sed 's/^started: //')
      $NOTIFY "🏁 作業終了: $TASK（開始: $STARTED）"$'\n'"$BODY"
      rm -f "$STATUS_FILE"
    fi
    echo "⏹️ タイマー停止。終了通知を送信しました。"
  else
    echo "⚠️ 稼働中のタイマーはありません。"
  fi
}

cmd_status() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "🟢 タイマー稼働中 (PID: $(cat "$PID_FILE"))"
    echo "---"
    cat "$STATUS_FILE" 2>/dev/null
  else
    echo "⚪ タイマー停止中"
    [ -f "$PID_FILE" ] && rm -f "$PID_FILE"
  fi
}

cmd_update() {
  if [ ! -f "$STATUS_FILE" ]; then
    echo "⚠️ アクティブな作業セッションがありません。先に start してください。"
    exit 1
  fi

  local DOING="${1}"
  local DONE="${2}"
  local NEXT="${3}"

  # Preserve header, replace body
  HEADER=$(sed -n '1,/^---$/ p' "$STATUS_FILE")

  cat > "$STATUS_FILE" <<EOF
$HEADER
🔄 やっていること: $DOING
✅ 完了したこと: $DONE
⏭️ 次にやること: $NEXT
EOF

  echo "📝 ステータス更新完了"
}

# --- Main ---
case "${1:-}" in
  start)   shift; cmd_start "$@" ;;
  stop)    cmd_stop ;;
  status)  cmd_status ;;
  update)  shift; cmd_update "$@" ;;
  *)
    echo "Usage: bash work-timer.sh {start|stop|status|update}"
    echo "  start  \"タスク名\"                     — タイマー開始"
    echo "  stop                                   — タイマー停止"
    echo "  status                                 — 現在の状態確認"
    echo "  update \"doing\" \"done\" \"next\"           — ステータス更新"
    exit 1
    ;;
esac
