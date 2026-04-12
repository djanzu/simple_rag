import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

class Command(BaseCommand):
    help = 'Embeds a file into ChromaDB'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Path to the file to embed')

    def handle(self, *args, **options):
        filename = options['filename']
        if not os.path.exists(filename):
            raise CommandError(f'File "{filename}" does not exist')

        self.stdout.write(f'Processing file: {filename}...')

        # Load document
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.pdf':
            loader = PyPDFLoader(filename)
        elif ext == '.md':
            loader = UnstructuredMarkdownLoader(filename)
        else:
            loader = TextLoader(filename)

        documents = loader.load()

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
        chunks = text_splitter.split_documents(documents)

        self.stdout.write(f'Split into {len(chunks)} chunks.')

        # Embed and store
        persist_directory = os.path.join(settings.BASE_DIR, 'chroma_db')
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        vectorstore.persist()

        self.stdout.write(self.style.SUCCESS(f'Successfully embedded "{filename}" into ChromaDB.'))
