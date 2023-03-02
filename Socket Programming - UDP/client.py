import socket


def main():
    server_ip = 'localhost'
    # server_ip = "192.168.165.198"
    port = 9090

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto("hello".encode('utf-8'), (server_ip, port))

        data = client_socket.recvfrom(1024)

        print(f"Message received :{data[0].decode()}")


if __name__ == '__main__':
    main()
