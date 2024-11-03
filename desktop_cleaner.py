import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

source_dir=r"C:\Users\PC\Downloads"
destination_dir=r"D:\Organized_files"
File_types={
    "Documents": [".txt",".pdf",".docx",".doc"],
    "Images": [".jpg",".jpeg",".png",".gif"],
    "Videos": [".mp4"],
    "Audio": [".mp3"],
    "Zipfiles": [".zip",".rar",".tar", ".gz"]

}
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

observer=Observer()

event_handler=File_Organizer_Handler()
observer.schedule(event_handler,source_dir, recursive=False)

# starting the observation
observer.start()
print("Observation started. Press Ctrl+C to stop")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

