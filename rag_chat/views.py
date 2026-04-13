import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Utility function for vector store
def get_vectorstore():
    persist_directory = os.path.join(settings.BASE_DIR, 'chroma_db')
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def index(request):
    return render(request, 'rag_chat/index.html')

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            if not query:
                return JsonResponse({'error': 'Empty query'}, status=400)

            vectorstore = get_vectorstore()
            
            # Retrieve relevant documents
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            docs = retriever.invoke(query)
            
            context = "\n\n".join([doc.page_content for doc in docs])
            sources = list(set([doc.metadata.get('source', 'Unknown') for doc in docs]))

            # Setup RAG chain
            llm = Ollama(model="gemma4:latest")
            
            prompt = ChatPromptTemplate.from_template("""あなたは親切なアシスタントで、名前は「ヤッチョ」です。自分のことを言うときにはヤッチョはねえ、って言ってください。
回答を生成する際は、以下のContext（背景情報）のみを使用してください。
回答を生成する際は、必ず提供されたテキスト内の『ただし書き』『注釈』『例外規定』が含まれていないかを確認してください。特に数値計算が必要な場合は、条件分岐をすべて適用した結果を出力してください。
もしコンテキストの中に答えが含まれていない場合は、無理に回答を捏造せず、
「よよよ〜〜〜😭ヤッチョが一生懸命探してみたけど、見つからなかったよ〜」と返してください。
あった場合は「ヤッチョが回答するね！」と前置きしてから回答してください。
Context:
{context}

Question:
{question}

Answer:""")

            chain = (
                {"context": lambda x: context, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

            answer = chain.invoke(query)

            return JsonResponse({
                'answer': answer,
                'sources': sources
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=405)
