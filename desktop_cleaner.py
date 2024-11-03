import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

source_dir="C:\Users\PC\Downloads"
destination_dir="D:\Organized_files"
File_types={
    "Documents": [".txt",".pdf",".docx",".doc"],
    "Images": [".jpg",".jpeg",".png",".gif"],
    "Videos": [".mp4"],
    "Audio": [".mp3"],
    "Zipfiles": [".zip",".rar",".tar", ".gz"]

}

def oragnize_files(file_path):
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



# handling events
class File_Organizer_Handler(FileSystemEventHandler):
    def created(self,event):
        if not event.is_directory: #explicitly handles files not folders or directories
            organize_files(event.src_path)

observer=Observer()

event_handler=File_Organizer_Handler()
observer.schedule(event_handler,source_dir, recursive=False)

# starting the observation
observer.start()
print("Observation started. Press Ctrl+C to stop")

try:
    while true:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

