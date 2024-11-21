import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import tkinter as tk
from tkinter import messagebox
import threading
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
    for file_name in os.listdir(source_dir):
        file_path=os.path.join(source_dir,file_name)
        if os.path.isfile(file_path):
            organize_files(file_path)

def organize_files(file_path):
    try:
        wait(file_path)
        name,ext=os.path.splitext(file_path)
        ext=ext.lower()


        for folder_name,extensions in File_types.items():
            if ext in extensions:
                destination_folder=os.path.join(destination_dir,folder_name)
                os.makedirs(destination_folder,exist_ok=True)
                shutil.move(file_path, os.path.join(destination_folder,os.path.basename(file_path)))
                print(f"moved '{os.path.basename(file_path)}' from '{file_path}' to '{destination_folder}'")
                return

        others=os.path.join(destination_dir,"others")
        os.makedirs(others, exist_ok= True)
        shutil.move(file_path,os.path.join(others,os.path.basename(file_path)))
        print(f"moved '{os.path.basename(file_path)}' from '{file_path}' to '{others}'")
    except Exception as e:
        print(f"found exception but moving on'{e}'")



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
    root=tk.Tk()
    root.title("File Organizer")
    start_button=tk.Button(root,text="start file organizer",command=start_observer,padx=20,pady=10)
    start_button.pack(pady=20)
    stop_button=tk.Button(root,text="stop file organizer", command=stop_observer, padx=20,pady=10)
    stop_button.pack(pady=20)
    root.mainloop()


if __name__ == '__main__':
    launch_app()
