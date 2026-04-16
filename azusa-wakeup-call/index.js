require('dotenv').config();
const express = require('express');
const twilio = require('twilio');

const app = express();
app.use(express.json());

const {
  TWILIO_ACCOUNT_SID,
  TWILIO_AUTH_TOKEN,
  TWILIO_CALLER_NUMBER,
  MASA_PHONE_NUMBER,
  PORT
} = process.env;

if (!TWILIO_ACCOUNT_SID || !TWILIO_AUTH_TOKEN || !TWILIO_CALLER_NUMBER || !MASA_PHONE_NUMBER) {
  console.warn('[azusa-wakeup-call] 必要な環境変数が揃っていません。 .env を確認してください。');
}

const client = twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN);

// ヘルスチェック用
app.get('/health', (req, res) => {
  res.json({ ok: true, status: 'azusa-wakeup-call running' });
});

// モーニングコール開始エンドポイント
app.post('/start-wakeup-call', async (req, res) => {
  try {
    if (!TWILIO_ACCOUNT_SID || !TWILIO_AUTH_TOKEN || !TWILIO_CALLER_NUMBER || !MASA_PHONE_NUMBER) {
      return res.status(500).json({ ok: false, error: 'Twilio 環境変数が未設定です' });
    }

    const publicBaseUrl = process.env.PUBLIC_BASE_URL || '';
    if (!publicBaseUrl) {
      console.warn('[azusa-wakeup-call] PUBLIC_BASE_URL が未設定です。ローカルテスト時は ngrok などで公開URLを設定してください。');
    }

    const call = await client.calls.create({
      to: MASA_PHONE_NUMBER,
      from: TWILIO_CALLER_NUMBER,
      url: `${publicBaseUrl}/twiml/wakeup`
    });

    res.json({ ok: true, sid: call.sid });
  } catch (err) {
    console.error('[azusa-wakeup-call] /start-wakeup-call error:', err);
    res.status(500).json({ ok: false, error: err.message });
  }
});

// Twilio が通話内容(TwiML)を取得するエンドポイント（フェーズ1: 固定メッセージ）
app.post('/twiml/wakeup', (req, res) => {
  const twiml = new twilio.twiml.VoiceResponse();

  twiml.say(
    {
      voice: 'alice',
      language: 'ja-JP'
    },
    'おはよう、マイク。梓だよ。まだ寝てたい気持ちもわかるけど、そろそろ起きよっか。今日も、朝のレポートタイムからゆっくりスタートしよ。'
  );

  res.type('text/xml');
  res.send(twiml.toString());
});

const port = PORT || 3000;
app.listen(port, () => {
  console.log(`[azusa-wakeup-call] server listening on port ${port}`);
});
