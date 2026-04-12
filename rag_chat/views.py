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
            
            prompt = ChatPromptTemplate.from_template("""You are a helpful assistant. Use the following context to answer the question.
If the answer is not in the context, just say you don't know. Don't try to make up an answer.
When generating responses, ensure that you check for any "provisos," "annotations," or "exception clauses" within the provided text. Especially when numerical calculations are required, please output the results after applying all conditional branches.
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
