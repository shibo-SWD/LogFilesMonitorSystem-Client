import socket

def start_client():
    # 输入服务器 IP 地址
    server_ip = input("Enter server IP address: ")

    # 创建一个 TCP/IP 套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 连接服务器
    server_address = (server_ip, 12345)
    print(f"Connecting to server at {server_ip} on port 12345...")
    client_socket.connect(server_address)
    print("Connected to server.")

    try:
        # 输入要发送的消息
        message = input("Enter message to send: ")
        client_socket.sendall(message.encode())
        print("Message sent to server.")
    finally:
        # 关闭连接
        client_socket.close()

if __name__ == "__main__":
    start_client()
