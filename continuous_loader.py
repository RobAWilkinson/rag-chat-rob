from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from loader import (
    client, 
    vector_store, 
    embed_model, 
    ingestion_cache,
    pipeline,
    SimpleDirectoryReader
)

class NotesChangeHandler(FileSystemEventHandler):
    def __init__(self, watch_directory):
        self.watch_directory = watch_directory
        self.cooldown = {}
        self.cooldown_time = 2  # seconds

    def on_modified(self, event):
        if event.is_directory:
            return
            
        if not event.src_path.endswith(('.txt', '.md')):
            return

        current_time = time.time()
        last_modified = self.cooldown.get(event.src_path, 0)

        if current_time - last_modified > self.cooldown_time:
            print(f"Change detected in {event.src_path}")
            self.cooldown[event.src_path] = current_time
            self.process_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.txt', '.md')):
            print(f"New file created: {event.src_path}")
            self.process_file(event.src_path)

    def process_file(self, file_path):
        try:
            # Load single file
            loader = SimpleDirectoryReader(
                input_files=[file_path],
            )
            documents = loader.load_data()
            
            # Process and update vector store
            nodes = pipeline.run(
                documents=documents,
                show_progress=True
            )
            print(f"Successfully processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

def start_watching(directory_path):
    event_handler = NotesChangeHandler(directory_path)
    observer = Observer()
    observer.schedule(event_handler, directory_path, recursive=True)
    observer.start()

    try:
        print(f"Started watching directory: {directory_path}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching directory")
    
    observer.join()

if __name__ == "__main__":
    WATCH_DIR = "/Users/rob/Documents/obsidian-notes"  # Update this path
    start_watching(WATCH_DIR) 