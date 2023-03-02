import socket


def main():
    ip = 'localhost'
    # ip = "192.168.165.198"
    port = 9090
    buffer_size = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((ip, port))

        while True:
            byte_address_pair = server_socket.recvfrom(buffer_size)
            message = byte_address_pair[0].decode('utf-8')
            address = byte_address_pair[1]

            print(f"Message : {message} \n{address}")
            server_socket.sendto("Hello".encode('utf-8'), address)


if __name__ == '__main__':
    main()
