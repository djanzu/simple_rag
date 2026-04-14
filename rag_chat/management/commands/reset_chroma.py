import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Resets the ChromaDB by deleting the persist directory'

    def handle(self, *args, **options):
        persist_directory = os.path.join(settings.BASE_DIR, 'chroma_db')
        
        self.stdout.write(f'Resetting ChromaDB at {persist_directory}...')
        
        if os.path.exists(persist_directory):
            try:
                shutil.rmtree(persist_directory)
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted "{persist_directory}".'))
                self.stdout.write('ChromaDB has been reset. It will be recreated on the next embed or retrieval operation.')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error deleting directory: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'Directory "{persist_directory}" does not exist. Nothing to reset.'))
