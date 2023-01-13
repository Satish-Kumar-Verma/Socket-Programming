import socket
import pickle
import csv
import datetime
from helper import Credentials


def get_credentials():
    with open('root_credentials.dat', 'rb') as file:
        obj = pickle.load(file)
        uname = obj.get_username()
        pwd = obj.get_password()
        return uname, pwd


def authorize(input_credentials):
    stored_cred = get_credentials()
    if input_credentials[0] == stored_cred[0] and input_credentials[1] == stored_cred[1]:
        return True
    return False


def log_survey_data(data, client):
    with open('survey_data.csv', 'a', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)
    print(f"[+] Client : [{client[0]}] has performed the survey and the data is logged into the server!")


def send_records(conn_id, client_address):
    with open('survey_data.csv', 'rb') as file:
        line = file.read(1024)
        while line:
            conn_id.send(line)
            line = file.read(1024)
        conn_id.send("DONE".encode())
        print(f'[+] Survey Data has been sent to the user with IP : {client_address[0]}')


def admin_panel(conn_id, client):
    credentials = conn_id.recv(1024).decode().split(",")
    if authorize(credentials):
        conn_id.send("1".encode('utf-8'))
        print(f"[+] Authorization successful!")
        print(f"[+] {credentials[0]} is the root user with IP : {client[0]}")

        view_data = conn_id.recv(1024).decode()
        if view_data == 'v':
            send_records(conn_id, client)

    else:
        print("[-] Authorization failed!\n[-] Connection is terminated.")
        conn_id.send("0".encode('utf-8'))
        return

    choice = conn_id.recv(1024).decode('utf-8')
    if choice == 'v':
        send_records(conn_id)


def client_panel(conn_id, client_address, n_conn):
    try:
        data = conn_id.recv(1024).decode('utf-8')
        data = str(n_conn) + "," + data
        log_survey_data(data.split(","), client_address)
        conn_id.send('1'.encode())

    except Exception as e:
        print(e)
        conn_id.send('0'.encode())


def choose_panel(conn_id, client_address, n_conn):
    user_type = conn_id.recv(1024).decode('utf-8')
    if user_type == 'r':
        admin_panel(conn_id, client_address)

    elif user_type == 'n':
        client_panel(conn_id, client_address, n_conn)


def main():
    # host = '192.168.87.198'
    host = 'localhost'  # 127.0.0.1
    port = 9090

    # Address family : IPv4, Transport : TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        server_socket.bind((host, port))

        # maximum number of queued connections : 10
        server_socket.listen(10)

        print(f"[+] Server is listening on port {port}...")
        no_of_connection = 0
        while True:
            connection_id, client_address = server_socket.accept()
            no_of_connection += 1
            print(f"[+] TCP connection is established with the host : {client_address}")

            message = "Connection established".encode('utf-8')
            connection_id.send(message)

            choose_panel(connection_id, client_address, no_of_connection)

            connection_id.close()


if __name__ == '__main__':
    main()



