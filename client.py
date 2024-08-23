import socket
import os
import time

def watch_directory(directory, host='172.21.22.78', port=12345):
    # 追踪已有的文件
    files_set = set(os.listdir(directory))

    while True:
        # 检查新文件
        current_files = set(os.listdir(directory))
        new_files = current_files - files_set

        for new_file in new_files:
            file_path = os.path.join(directory, new_file)
            send_file(file_path, host, port)
        
        # 更新追踪的文件集合
        files_set = current_files
        time.sleep(1)  # 等待一段时间后再次检查文件夹

def send_file(file_path, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        file_name = os.path.basename(file_path)
        
        # 发送文件名长度和文件名
        client_socket.send(len(file_name).to_bytes(4, 'big'))
        client_socket.send(file_name.encode())

        # 发送文件大小
        file_size = os.path.getsize(file_path)
        client_socket.send(file_size.to_bytes(8, 'big'))

        # 发送文件内容
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)

        print(f"File '{file_name}' sent to server.")

if __name__ == "__main__":
    # 设置监控的目录
    watch_directory('./watch_directory')