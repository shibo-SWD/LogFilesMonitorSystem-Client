import socket
import os
import time
import argparse
from file_monitor import FileMonitor

class FileClient:
    def __init__(self, server_host='127.0.0.1', server_port=12345, watch_directory='./watch_directory'):
        self.server_host = server_host
        self.server_port = server_port
        self.watch_directory = watch_directory

    def start(self):
        """启动文件监控并发送新文件"""
        os.makedirs(self.watch_directory, exist_ok=True)

        # 连接服务器并获取需要发送的文件列表
        files_to_send = self.list_files()

        # 监控文件夹并发送新文件
        monitor = FileMonitor(self.watch_directory, self.send_file, files_to_send)
        monitor.start()

        # 保持主线程运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down client...")
            monitor.stop()

    def list_files(self):
        """列出监控目录中的所有文件，并检查哪些需要发送"""
        files = os.listdir(self.watch_directory)
        files_to_send = []

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                print(f"Connecting to server at {self.server_host}:{self.server_port} to list files...")
                client_socket.connect((self.server_host, self.server_port))
                print("Connected to server.")

                # 发送指令标识 (例如 'LIST')
                client_socket.send(b'LIST')

                # 发送文件名列表的长度
                files_data = '\n'.join(files).encode()
                client_socket.send(len(files_data).to_bytes(4, 'big'))
                client_socket.send(files_data)

                # 接收需要发送的文件列表长度
                response_length_data = client_socket.recv(4)
                response_length = int.from_bytes(response_length_data, 'big')

                # 接收需要发送的文件列表
                response_data = client_socket.recv(response_length).decode()
                files_to_send = response_data.split('\n')

        except Exception as e:
            print(f"Error listing files: {e}")

        print(files_to_send)
        return files_to_send

    def send_file(self, file_path):
        """发送文件到服务端"""
        if not os.path.isfile(file_path):
            print(f"Skipping {file_path} because it is not a file.")
            return

        with open(file_path, 'rb') as file:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.server_host, self.server_port))
                print(f"Connected to server at {self.server_host}:{self.server_port}")

                # 发送命令
                sock.sendall(b'SEND')

                # 发送文件名长度和文件名
                file_name_encoded = file_name.encode()
                sock.sendall(len(file_name_encoded).to_bytes(4, 'big'))
                sock.sendall(file_name_encoded)

                # 发送文件大小
                sock.sendall(file_size.to_bytes(8, 'big'))

                # 发送文件内容
                chunk = file.read(1024)
                while chunk:
                    sock.sendall(chunk)
                    chunk = file.read(1024)

                print(f"File '{file_name}' sent to server.")

if __name__ == "__main__":
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="Start the FileClient to watch a directory and send files to a server.")

    # 添加 `--serviceip` 参数
    parser.add_argument('-sip', '--serviceip', 
                        type=str, default='127.0.0.1', 
                        help='The IP address of the server to connect to.')
    parser.add_argument('-wd', '--watchDir', type=str, default='./watch_directory', 
                        help='The directory of monitored folder.')

    # 解析参数
    args = parser.parse_args()
    client = FileClient(server_host=args.serviceip,
                        server_port=12345, 
                        watch_directory=args.watchDir)
    client.start()
