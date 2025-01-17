# File Organizer

A Python script to organize files from a specified source directory into categorized folders in a destination directory. The application monitors the source directory in real-time and moves files based on their types, simplifying file management.

## Features
- **Real-Time Monitoring**: Tracks file changes using `watchdog`.
- **Customizable File Organization**: Define categories and file extensions in a dictionary.
- **Automatic Folder Creation**: Dynamically creates required folders.
- **GUI Integration**: Simple interface built with `Tkinter`.
- **Standalone Application**: Package as a `.exe` using `PyInstaller`.

---

## Python Libraries Used
- `os`: File and directory operations.
- `shutil`: Moving files between directories.
- `time`: Introduce delays for smoother operation.
- `watchdog`: Real-time monitoring of directory changes.
- `tkinter`: Graphical User Interface (GUI).
- `threading`: Non-blocking observer for smooth GUI operation.

---

## Version Updates

### **v0: Basic Skeleton**
- Core functionality to organize files based on file types.
- Limitation: Permission errors when handling files in use by browsers.

### **v1: Permission Error Fix**
- Added delay (`time.sleep`) to handle files still in use.
- Switched to processing files directly from the source directory.

### **v2: GUI Integration**
- Added a `Tkinter` GUI for starting and stopping the organizer.
- Packaged as a standalone `.exe` using `PyInstaller`.

### **v3: Observer Stop Fix**
- Introduced `threading` to run the observer in a separate thread.
- Added a functional "Stop" button to cleanly terminate the process.

---









