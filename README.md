# kawai-soundproof-watcher

中古の防音室の新着出品を自動チェックし、新着があった場合のみ hiroshige.ichino@gmail.com
にメール通知するウォッチャーです。用途の異なる2系統のウォッチャーを運用しています。

## ウォッチャー1: 防音室本体（DR-50 / DR-40 4.3畳）

1日2回（日本時間 8:00 / 20:00）実行。詳細は [`data/criteria.json`](data/criteria.json) を参照。

1. **第一希望**: カワイ ナサール（Nasall）Dr-50 の防音室（サイズ不問）
2. **次点**: Dr-40・4.3畳タイプの防音室のみ
   - カワイ ナサール（例: LKSX22-31, MKSX22-31）
   - ヤマハ セフィーネNS（例: AMDC43H, AMDC43C）

状態管理: [`data/seen_items.json`](data/seen_items.json)

## ウォッチャー2: Dr-40・0.8畳（メーカー問わず）

1日1回（日本時間 8:00）実行。詳細は [`data/criteria_dr40_08.json`](data/criteria_dr40_08.json) を参照。

- Dr-40等級・0.8畳タイプの中古防音室（カワイ・ヤマハ等メーカー問わず）

状態管理: [`data/seen_items_dr40_08.json`](data/seen_items_dr40_08.json)

いずれも「中古」のみが対象です。

## 情報源

- 優先: 中古楽器店・防音室専門店・買取/リサイクル業者、メーカー特約店の中古/展示品ページ
- 通常: メルカリ、ヤフオク!、PayPayフリマ、ジモティー

## 仕組み

Claude Code Remote の Routine（スケジュール実行）がこのセッションを再開し、以下を行います
（ウォッチャー1・2共通の流れ、参照する `criteria`/`seen_items` ファイルが異なるのみ）。

1. `data/seen_items*.json`（これまでに検知済みの出品一覧）を読み込む
2. Web検索で情報源を横断的にチェックし、条件に合う出品を探す
3. 既知の出品と照合し、新着のみを抽出
4. 新着があれば `scripts/send_email.py` で hiroshige.ichino@gmail.com にメール送信
   （新着が無ければメールは送らない）
5. `data/seen_items*.json` を更新して commit / push

状態（何を既に通知済みか）は `data/seen_items*.json` に git 管理されているため、
実行環境がリセットされても GitHub 上の最新状態から再開できます。

## メール送信のセットアップ（Resend）

メール送信には [Resend](https://resend.com) の API を使用します。以下はユーザー側の作業です。

1. https://resend.com でアカウント作成（hiroshige.ichino@gmail.com で登録推奨）
2. ダッシュボードで API キーを発行
3. このリポジトリを動かしている Claude Code Remote の **環境変数** に
   `RESEND_API_KEY` を登録
4. 独自ドメインを検証しない場合、送信元はデフォルトで `onboarding@resend.dev`
   （Resend のサンドボックス送信元）になります。この場合、**Resend アカウント登録に
   使ったメールアドレス宛にしか送信できない**制限があるため、
   hiroshige.ichino@gmail.com で登録してください
5. 独自ドメインを検証済みの場合は環境変数 `RESEND_FROM_EMAIL` で送信元を上書き可能

`RESEND_API_KEY` が未設定の場合、実行セッションはメールを送信できません。代わりに
プッシュ通知（Claude Code Remote の Remote Control 経由）で新着件数のみ通知します。
**Routine（スケジュール実行）で起動されるセッションには Gmail 等のコネクタツールが
引き継がれないため、Gmail下書き作成へのフォールバックは使えません。** 実際にメール
を受け取るには `RESEND_API_KEY` の設定が必須です。

## 手動テスト

```bash
export RESEND_API_KEY=...   # Resend の API キー
echo "<p>テスト送信</p>" > /tmp/test_body.html
python3 scripts/send_email.py "防音室ウォッチャー: テスト" /tmp/test_body.html
```
