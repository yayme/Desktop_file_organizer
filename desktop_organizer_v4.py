import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import tkinter as tk
from tkinter import messagebox
import threading
import os
import shutil
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
source_dir=r"C:\Users\PC\Downloads"
destination_dir=r"D:\Organized_files"
File_types={
    "Documents-pdf": [".txt",".pdf"],
    "Documents-doc":[".docx",".doc"],
    "Images": [".jpg",".jpeg",".png",".gif"],
    "Videos": [".mp4"],
    "Audio": [".mp3"],
    "Zipfiles": [".zip",".rar",".tar", ".gz"]

}
observer=None
observer_thread=None
# separate thread for the start observer loop so that it doesnt stop commands from gui

def wait(file_path):
    while True:
        try:
            with open(file_path,'r'):
                break
        except PermissionError:
            if file_path.endswith('.tmp'):
                time.sleep(5)
            else:
                time.sleep(10)

# immediately trying to move the file results in error because the browser
# is still using it, so we wait for a bit before moving it


def organize_files_in_destination():
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    for file in files:
        file_path=os.path.join(source_dir,file)
        organize_files(file_path)




# Predefined labels
labels = ['math', 'computer science', 'machine learning', 'artificial intelligence','statistics','presentation','modeling']

# Load spaCy model for word embeddings
nlp = spacy.load("en_core_web_md")


def calculate_similarity(file_text, labels):
    # Vectorize the file text and labels
    vectorizer = TfidfVectorizer(stop_words="english")

    # Combine file text and labels into a list of texts
    texts = [file_text] + labels
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Calculate similarity between the file text and each label
    similarities = tfidf_matrix[0, 1:].toarray()[0]

    # Find the label with the highest similarity
    max_similarity_index = similarities.argmax()

    return labels[max_similarity_index], similarities[max_similarity_index]


def organize_files(file_path):
    try:
        # Read the file content (title and first few lines)
        name, ext = os.path.splitext(file_path)
        ext = ext.lower()

        with open(file_path, 'r', errors='ignore') as file:
            file_content = file.read()
            file_text = file_content[:500]  # Get title + first few lines (adjust as needed)

        # Calculate the similarity of the file text with predefined labels
        label, similarity = calculate_similarity(file_text, labels)

        # Folder for the label
        destination_folder = os.path.join(destination_dir, label)

        # Make sure the destination folder exists
        os.makedirs(destination_folder, exist_ok=True)

        # Move the file to the appropriate folder
        shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
        print(
            f"Moved '{os.path.basename(file_path)}' to '{destination_folder}' based on similarity of {similarity:.2f}")

    except Exception as e:
        print(f"Exception occurred: {e}")


# handling events
class File_Organizer_Handler(FileSystemEventHandler):
    def on_created(self,event):
        if not event.is_directory: #explicitly handles files not folders or directories
            time.sleep(10)
            organize_files_in_destination()



def start_observer():
    global observer, observer_thread
    if observer is None:
        observer=Observer()
        event_handler=File_Organizer_Handler()
        observer.schedule(event_handler,source_dir, recursive=False)

    # run the observer in a separate thread
    def run_observer():
        observer.start()


    observer_thread=threading.Thread(target=run_observer, daemon=True)
    observer_thread.start()
    # print("Observation started. Press Ctrl+C to stop")
    messagebox.showinfo("File Organizer","Observation started.Press Stop button to stop")


def stop_observer():
    global observer,observer_thread
    if observer:
        observer.stop()
        observer.join()
        observer=None
        observer_thread=None
        messagebox.showinfo("file organizer", "observation stopped")

def launch_app():
    global root
    root=tk.Tk()
    root.title("File Organizer")
    start_button=tk.Button(root,text="start file organizer",command=start_observer,padx=20,pady=10)
    start_button.pack(pady=20)
    stop_button=tk.Button(root,text="stop file organizer", command=stop_observer, padx=20,pady=10)
    stop_button.pack(pady=20)
    root.mainloop()

launch_app()
# if __name__ == '__main__':
#     launch_app()
