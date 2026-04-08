# このシステムについて

簡易的なRAGシステムを提供する

## 技術スタック
- python
- django
- sqlite
- venv
- langchain
- chromadb
- ollama（API呼び出し）

djangoベースで作成されて、以下のカスタムコマンドが使用可能。
- python manage.py embed ファイル名
  - 指定されたファイルをnomic-embed-textを使用してchromadbに投入する
  

## web画面
- メイン画面
  - chatgptのようなチャットインターフェースを備える
  - chat欄に入力された自然言語を認識し、chromadbよりデータを探す
  - 参照したソースとともに回答する

## 使用するLLM
- ollama
  - gemma4:latest
  - nomic-embed-text
