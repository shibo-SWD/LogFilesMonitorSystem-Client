# file_monitor.py

import os
import time
from threading import Thread

class FileMonitor:
    def __init__(self, directory, callback):
        self.directory = directory
        self.callback = callback
        self.running = False

    def start(self):
        """启动文件监控线程"""
        self.running = True
        self.thread = Thread(target=self._monitor_directory, daemon=True)
        self.thread.start()
        print("File monitor started, watching directory:", self.directory)

    def stop(self):
        """停止文件监控"""
        self.running = False
        self.thread.join()
        print("File monitor stopped.")

    def _monitor_directory(self):
        """监控目录中的新文件"""
        files_set = set(os.listdir(self.directory))

        while self.running:
            current_files = set(os.listdir(self.directory))
            new_files = current_files - files_set

            for new_file in new_files:
                file_path = os.path.join(self.directory, new_file)
                print(f"New file detected: {file_path}")
                self.callback(file_path)

            files_set = current_files
            time.sleep(1)
