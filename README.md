# 簡易RAGチャットシステム

このシステムは、Djangoをベースにした簡易的なRAG（Retrieval-Augmented Generation）チャットシステムです。
ローカルで動作するLLM（Ollama）を使用し、PDFやMarkdownなどのドキュメントに基づいた回答を生成します。

## 技術スタック

- **Backend**: Django 5.2
- **Database**: SQLite3
- **Vector DB**: ChromaDB
- **LLM API**: Ollama
  - チャット: `gemma4:latest`
  - 埋め込み: `nomic-embed-text`
- **Library**: LangChain

## インストール方法

### 1. 仮想環境の作成と有効化

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. Ollamaのセットアップ

Ollamaをインストールし、必要なモデルをプルします。

```bash
ollama pull gemma4:latest
ollama pull nomic-embed-text
```

## 起動方法

### 1. データベースのマイグレーション

```bash
python manage.py migrate
```

### 2. 開発サーバーの起動

```bash
python manage.py runserver
```

サーバー起動後、ブラウザで `http://127.0.0.1:8000` にアクセスしてください。

## カスタムコマンド

### Django管理コマンド

#### ドキュメントの埋め込み (Embed)

指定したファイルをChromaDBに登録します。対応フォーマットは `.pdf`, `.md`, `.txt` です。

```bash
python manage.py embed <ファイルパス>
```

例:
```bash
python manage.py embed sample_rule.md
```

## 補足事項

- **ベクトルデータの保存**: `chroma_db/` ディレクトリに永続化されます。
- **インデックスのリセット**: 登録したデータを消去したい場合は `chroma_db/` ディレクトリを削除してください。
  - ``python manage.py reset_chroma``でも消去できます。

## memo
但し書きが読まれていないため、精度向上のために追加したプロンプト
```
回答を生成する際は、必ず提供されたテキスト内の**『ただし書き』『注釈』『例外規定』**が含まれていないかを確認してください。特に数値計算が必要な場合は、条件分岐をすべて適用した結果を出力してください。
```
