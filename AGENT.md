# AGENT.md

## 🎯 Goal
このプロジェクトの目的は、Django + LangChain を用いたAIアプリケーションの開発です。
エージェントは「安全・再現性・可読性」を重視してコードを生成してください。

---

## 🧠 Tech Stack
- Python 3.11+
- Django (REST APIベース)
- LangChain
- OpenAI / Ollama / ローカルLLM
- PostgreSQL
- Redis（キャッシュ・Celery用）

---

## ⚙️ Coding Rules

### General
- 型ヒントを必ず付ける
- 可読性を優先（1関数は50行以内）
- コメントは「なぜ」を説明する
- マジックナンバー禁止

### Django
- ビジネスロジックは `services/` に書く
- `views.py` は薄く保つ（Fat Model / Service Layer）
- ORMクエリは最適化（select_related / prefetch_related）
- settingsは環境変数で管理

### LangChain
- Chains / Agents は責務ごとに分割
- プロンプトは必ず外部ファイル化（`prompts/`）
- LLM呼び出しはラップ関数を通す
- temperatureは用途別に固定（例: 0.0 or 0.7）

---

## 🧩 Architecture
```
project/
├── app/
│ ├── models/
│ ├── views/
│ ├── serializers/
│ ├── services/ # ビジネスロジック
│ ├── agents/ # LangChain Agent
│ ├── chains/ # LangChain Chains
│ └── prompts/ # プロンプトテンプレート
├── config/
├── tests/
└── manage.py
```


---

## 🤖 Agent Design Rules

- エージェントは「単一責務」にする
- ツールは明示的に定義する（暗黙禁止）
- Function Callingを優先する
- 無限ループ防止のため max_iterations を設定

例:
```python
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    max_iterations=5,
    verbose=True,
)
```
## 🔐 Security
外部入力は必ずバリデーション
プロンプトインジェクション対策を行う
秘密情報は .env に格納
ログに個人情報を出さない

## 🧪 Testing
pytest を使用
LLM部分はモック化
snapshotテストで出力を固定

## 🚀 Performance
非同期処理（Celery / asyncio）を活用
LLM呼び出しはキャッシュする
トークン使用量をログ出力する

## 🧭 Output Format

エージェントの出力は以下を守ること：

コードは必ず完全な形で出力
省略しない
実行可能な状態で提示

## ❌ 禁止事項
いきなり巨大なファイルを生成しない
未確認のライブラリを勝手に追加しない
ハードコードされたAPIキーを書く
不要な抽象化

## ✅ 推奨事項
小さく作って動かす
変更理由を説明する
エラーケースを先に考える


## 📚 RAG Rules

- chunkサイズは1000文字前後
- overlapは100〜200
- metadataを必ず保持

## 🧠 Vector DB

- ChromaDB を使用
- embeddingモデルは明示する（例: nomic-embed-text via Ollama）
- embedding関数は1箇所に集約する

- LLMはOllama経由で呼び出す
- モデル名は環境変数で管理
