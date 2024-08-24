import socket
import os
import time
from file_monitor import FileMonitor

class FileClient:
    def __init__(self, server_host='127.0.0.1', server_port=12345, watch_directory='./watch_directory'):
        self.server_host = server_host
        self.server_port = server_port
        self.watch_directory = watch_directory

    def start(self):
        """启动文件监控并发送新文件"""
        os.makedirs(self.watch_directory, exist_ok=True)
        monitor = FileMonitor(self.watch_directory, self.send_file)
        monitor.start()

        # 保持主线程运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down client...")
            monitor.stop()

    def send_file(self, file_path):
        """发送文件到服务端"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                print(f"Connecting to server at {self.server_host}:{self.server_port}...")
                client_socket.connect((self.server_host, self.server_port))
                print("Connected to server.")
                file_name = os.path.basename(file_path)

                # 发送文件名长度和文件名
                client_socket.send(len(file_name).to_bytes(4, 'big'))
                client_socket.send(file_name.encode())
                print(f"Sent file name: {file_name}")

                # 发送文件大小
                file_size = os.path.getsize(file_path)
                client_socket.send(file_size.to_bytes(8, 'big'))
                print(f"Sent file size: {file_size} bytes")

                # 发送文件内容
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        client_socket.sendall(data)
                print(f"File '{file_name}' sent to server.")
        except Exception as e:
            print(f"Error sending file {file_path}: {e}")

if __name__ == "__main__":
    client = FileClient(server_host='172.21.22.78', server_port=12345)
    client.start()