import time
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    """自定义的事件处理程序，用于监控文件更改"""

    def __init__(self, send_file_callback):
        self.send_file_callback = send_file_callback
        self.last_modified = {}  # 记录每个文件的最后修改时间

    def on_modified(self, event):
        """文件被修改时触发"""
        if not event.is_directory:
            now = time.time()
            filepath = event.src_path

            # 检查文件的最后修改时间是否在1秒内
            if filepath in self.last_modified and (now - self.last_modified[filepath]) < 1:
                return  # 如果在1秒内，则忽略此次修改事件

            self.last_modified[filepath] = now
            print(f"File modified: {filepath}")
            self.send_file_callback(filepath)

    def on_created(self, event):
        """文件被创建时触发"""
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            self.send_file_callback(event.src_path)