import os
from watchdog.observers import Observer
from file_event_handler import FileEventHandler

class FileMonitor:
    def __init__(self, directory, callback, initial_files_to_send=None):
        self.directory = directory
        self.callback = callback
        self.running = False
        self.observer = None
        # 使用服务器返回的需要发送的文件列表初始化
        self.files_to_send = set(initial_files_to_send) if initial_files_to_send else set()
        self._sync_initial_files()  # 立即同步初始文件

    def start(self):
        """启动文件监控"""
        self.running = True
        self.observer = Observer()
        event_handler = FileEventHandler(self.callback)
        self.observer.schedule(event_handler, self.directory, recursive=False)
        self.observer.start()
        print("File monitor started, watching directory:", self.directory)

    def stop(self):
        """停止文件监控"""
        self.running = False
        self.observer.stop()
        self.observer.join()
        print("File monitor stopped.")

    def _sync_initial_files(self):
        """同步初始文件，将客户端有但服务端没有的文件发送给服务端"""
        for new_file in self.files_to_send:
            file_path = os.path.join(self.directory, new_file)
            print(f"Syncing initial file to server: {file_path}")
            self.callback(file_path)  # 使用回调函数发送文件

        # 清除已发送的文件列表
        self.files_to_send.clear()