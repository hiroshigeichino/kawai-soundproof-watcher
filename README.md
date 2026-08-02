# gibson-1959-les-paul-watcher

2000年製 Gibson Les Paul **カスタムショップ** 1959 Reissue（通称 R9）の中古出品を
1日2回自動チェックし、新着があった場合のみ hiroshige.ichino@gmail.com にメール通知する
ウォッチャーです。

## 検索条件

詳細は [`data/criteria.json`](data/criteria.json) を参照。

- **対象**: Gibson Les Paul 1959 Reissue、2000年製、**カスタムショップ製のみ**
  （レギュラーライン／Historic Collection等のカスタムショップ以外は対象外）
- **状態**: 中古のみ
- **表記揺れ**: 「レスポール」「Les Paul」「1959」「'59」「59」「カスタムショップ」
  「Custom Shop」「CS」など、商品名の書き方が揺れる前提で検索する
- **シリアルによる判定**: 商品名だけで判別できない場合、シリアル番号（先頭が
  「9」＝1959モデル、続けて「0」から始まる番号。999本目までは0始まりの4桁、
  1000本目以降は0始まりの5桁）から候補を絞り込む。写真にしかシリアルが
  写っておらず本文からは読み取れない出品は除外せず「要確認」として報告する

## 情報源

検索対象はネット上の全サイト。以下は代表例で、これに限らず検索でヒットしたものは
種別を問わずすべて確認する。

- デジマート (digimart.net)、Jギター (jguitar.com)
- 各ギターショップ・中古/ヴィンテージ楽器店のECサイト全般
- 個人売買: メルカリ、ヤフオク!、PayPayフリマ、ラクマ、ジモティー、その他フリマ系サイト

## 仕組み

1日2回（日本時間 8:00 / 20:00）、Claude Code Remote の Routine（スケジュール実行）が
新しいセッションを起動し、以下を行います。

1. `data/seen_items.json`（これまでに検知済みの出品一覧）を読み込む
2. `data/criteria.json` の検索条件・シリアル判定ロジック・情報源を確認する
3. Web検索で情報源を横断的にチェックし、条件に合う（または「要確認」の）出品を探す
4. 既知の出品と照合し、未通知の新着（要確認含む）のみを抽出する
5. 新着が1件以上あれば `scripts/send_email.py` で hiroshige.ichino@gmail.com にメール送信する
   （新着が無ければメールは送らない）
6. `data/seen_items.json` を更新して commit / push（新着の有無にかかわらず毎回行う）

状態（何を既に通知済みか）は `data/seen_items.json` に git 管理されているため、
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
プッシュ通知（Claude Code Remote の Remote Control 経由）でチェック結果の概要のみ通知します。
**Routine（スケジュール実行）で起動されるセッションには Gmail 等のコネクタツールが
引き継がれないため、Gmail下書き作成へのフォールバックは使えません。** 実際にメール
を受け取るには `RESEND_API_KEY` の設定が必須です。

## 手動テスト

```bash
export RESEND_API_KEY=...   # Resend の API キー
echo "<p>テスト送信</p>" > /tmp/test_body.html
python3 scripts/send_email.py "Gibson 1959 Les Paulウォッチャー: テスト" /tmp/test_body.html
```
