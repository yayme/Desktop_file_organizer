import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import json  # for reading/writing configuration and labels

# Default paths
config_file_path = "config.json"
labels_file_path = "labels.json"

# Load spaCy model for word embeddings
nlp = spacy.load("en_core_web_md")

# Default configuration
config = {
    "source_dir": "",
    "destination_dir": ""
}

observer = None
observer_thread = None

def load_config():
    """Load configuration from a JSON file."""
    global config
    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as file:
            config = json.load(file)
    else:
        save_config()

def save_config():
    """Save configuration to a JSON file."""
    with open(config_file_path, "w") as file:
        json.dump(config, file)


def load_labels():
    """Load user-defined labels from a JSON file."""
    if os.path.exists(labels_file_path):
        with open(labels_file_path, "r") as file:
            labels = json.load(file)
    else:
        labels = ["math", "computer science", "machine learning", "artificial intelligence", "statistics", "presentation", "modeling"]
    return labels


def save_labels(labels):
    """Save user-defined labels to a JSON file."""
    with open(labels_file_path, "w") as file:
        json.dump(labels, file)

labels = load_labels()

def calculate_similarity(file_text, labels):
    """Calculate similarity of the file text with predefined labels."""
    vectorizer = TfidfVectorizer(stop_words="english")
    texts = [file_text] + labels
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarities = tfidf_matrix[0, 1:].toarray()[0]
    max_similarity_index = similarities.argmax()
    return labels[max_similarity_index], similarities[max_similarity_index]


def wait_for_file(file_path):
    """Wait until the file is finished downloading."""
    while True:
        try:
            with open(file_path, 'r'):
                break
        except (PermissionError, FileNotFoundError):
            time.sleep(10)
        except Exception as e:
            print(f"Error while waiting for file: {e}")
            break


def organize_files(file_path):
    """Organize files into categories based on similarity."""
    try:
        if file_path.endswith(".tmp"):
            print(f"Skipping temporary file: {file_path}")
            return

        wait_for_file(file_path)
        name, ext = os.path.splitext(file_path)
        ext = ext.lower()

        with open(file_path, 'r', errors='ignore') as file:
            file_content = file.read()
            file_text = file_content[:500]  # Get title + first few lines (adjust as needed)

        label, similarity = calculate_similarity(file_text, labels)
        destination_folder = os.path.join(config["destination_dir"], label)
        os.makedirs(destination_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
        print(f"Moved '{os.path.basename(file_path)}' to '{destination_folder}' based on similarity of {similarity:.2f}")

    except Exception as e:
        print(f"Exception occurred: {e}")


class File_Organizer_Handler(FileSystemEventHandler):
    """Handle file system events."""
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(10)  # Delay to ensure the file is not in use
            file_path = os.path.join(config["source_dir"], os.path.basename(event.src_path))
            organize_files(file_path)


def start_observer():
    """Start the file observer to monitor downloads folder."""
    global observer, observer_thread
    if observer is None:
        observer = Observer()
        event_handler = File_Organizer_Handler()
        observer.schedule(event_handler, config["source_dir"], recursive=False)

    def run_observer():
        observer.start()

    observer_thread = threading.Thread(target=run_observer, daemon=True)
    observer_thread.start()
    messagebox.showinfo("File Organizer", "Observation started. Press Stop button to stop.")


def stop_observer():
    """Stop the file observer."""
    global observer, observer_thread
    if observer:
        observer.stop()
        observer.join()
        observer = None
        observer_thread = None
        messagebox.showinfo("File Organizer", "Observation stopped.")


def select_directory(label, config_key):
    """Allow the user to select a directory."""
    directory = filedialog.askdirectory()
    if directory:
        config[config_key] = directory
        save_config()
        label.config(text=f"{config_key.replace('_', ' ').capitalize()}: {directory}")


def launch_app():
    """Launch the GUI for the File Organizer."""
    global root
    root = tk.Tk()
    root.title("File Organizer")

    load_config()

    # Source Directory
    source_label = tk.Label(root, text=f"Source directory: {config['source_dir']}")
    source_label.pack(pady=5)
    source_button = tk.Button(root, text="Select Source Directory", command=lambda: select_directory(source_label, "source_dir"))
    source_button.pack(pady=5)

    # Destination Directory
    dest_label = tk.Label(root, text=f"Destination directory: {config['destination_dir']}")
    dest_label.pack(pady=5)
    dest_button = tk.Button(root, text="Select Destination Directory", command=lambda: select_directory(dest_label, "destination_dir"))
    dest_button.pack(pady=5)

    # Start button to begin file organizing
    start_button = tk.Button(root, text="Start File Organizer", command=start_observer, padx=20, pady=10)
    start_button.pack(pady=20)

    # Stop button to halt the file organizing
    stop_button = tk.Button(root, text="Stop File Organizer", command=stop_observer, padx=20, pady=10)
    stop_button.pack(pady=20)

    # Label management section
    label_frame = tk.LabelFrame(root, text="Manage Labels", padx=10, pady=10)
    label_frame.pack(pady=20)

    label_listbox = tk.Listbox(label_frame, height=5, width=30)
    label_listbox.pack(side=tk.LEFT)

    # Add current labels to the listbox
    for label in labels:
        label_listbox.insert(tk.END, label)

    def add_label():
        new_label = label_entry.get()
        if new_label and new_label not in labels:
            labels.append(new_label)
            label_listbox.insert(tk.END, new_label)
            save_labels(labels)
            label_entry.delete(0, tk.END)

    def remove_label():
        selected_label = label_listbox.curselection()
        if selected_label:
            label = label_listbox.get(selected_label)
            labels.remove(label)
            label_listbox.delete(selected_label)
            save_labels(labels)

    label_entry = tk.Entry(label_frame)
    label_entry.pack(side=tk.LEFT, padx=5)
    add_button = tk.Button(label_frame, text="Add Label", command=add_label, padx=10, pady=5)
    add_button.pack(side=tk.LEFT)
    remove_button = tk.Button(label_frame, text="Remove Label", command=remove_label, padx=10, pady=5)
    remove_button.pack(side=tk.LEFT)

    root.mainloop()

#
# if __name__ == "__main__":
#     launch_app()
launch_app()

