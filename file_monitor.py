import os
import time
from threading import Thread

class FileMonitor:
    def __init__(self, directory, callback, initial_files_to_send=None):
        self.directory = directory
        self.callback = callback
        self.running = False
        # 使用服务器返回的需要发送的文件列表初始化
        self.files_to_send = set(initial_files_to_send) if initial_files_to_send else set()
        self._sync_initial_files()  # 立即同步初始文件

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

    def _sync_initial_files(self):
        """同步初始文件，将客户端有但服务端没有的文件发送给服务端"""
        current_files = set(os.listdir(self.directory))
        files_to_send_now = self.files_to_send
        print(files_to_send_now)

        for new_file in files_to_send_now:
            file_path = os.path.join(self.directory, new_file)
            print(f"Syncing file to server: {file_path}")
            self.callback(file_path)  # 使用回调函数发送文件

        # self.files_to_send -= current_files
        # 更新已发送的文件列表
        self.files_to_send.update(files_to_send_now)

    def _monitor_directory(self):
        """监控目录中的新文件"""
        files_set = set(os.listdir(self.directory))

        while self.running:
            current_files = set(os.listdir(self.directory))
            # 仅检测新文件
            new_files = current_files - files_set

            # 过滤掉已经在self.files_to_send中的文件，只发送新的和没有在初始列表中的文件
            files_to_send_now = new_files - self.files_to_send

            for new_file in files_to_send_now:
                file_path = os.path.join(self.directory, new_file)
                print(f"New file detected: {file_path}")
                self.callback(file_path)  # 调用回调函数发送文件

            # 更新已存在文件列表
            files_set = current_files
            # 添加刚检测到的新文件到self.files_to_send中，防止重复发送
            self.files_to_send.update(new_files)
            time.sleep(1)
