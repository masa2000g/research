#!/bin/zsh
set -u
cd /Users/takehara/Projects/masa-knowledge
mkdir -p /Users/takehara/.openclaw/workspace/logs
exec node scripts/build_daily_intelligence.js >> /Users/takehara/.openclaw/workspace/logs/daily-intelligence-2026-04-15.log 2>&1
