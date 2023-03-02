import socket
import threading
import pickle
import csv
import os
from helper import Credentials


ADMIN_FLAG = 'IaMnOtAnAdMiN'
lock = threading.Lock()


def get_credentials():
    """Read stored credentials from the server."""

    try:
        if not os.path.exists('root_credentials.dat'):
            cred = Credentials()

            # username = input("Enter the root username : ")
            # password = input("Enter the root password : ")
            username, password = "Baking_Bad", "CN_Group_1"
            cred.set_username(username)
            cred.set_password(password)

            with open('root_credentials.dat', 'wb') as file:
                pickle.dump(cred, file)

        with open('root_credentials.dat', 'rb') as file:
            obj = pickle.load(file)
            uname = obj.get_username()
            pwd = obj.get_password()
            return uname, pwd

    except Exception as e:
        print(e)


def authorize(input_credentials):
    stored_cred = get_credentials()
    if input_credentials[0] == stored_cred[0] and input_credentials[1] == stored_cred[1]:
        return True
    return False


def send_records(conn_id, client_address):
    try:
        lock.acquire()
        with open('survey_data.csv', 'rb') as file:
            line = file.read(1024)
            while line:
                conn_id.send(line)
                line = file.read(1024)
            conn_id.send("AEIOUYRUG".encode())
        lock.release()
        print(f'[+] Survey Data has been sent to the user with IP : {client_address}')
    except FileNotFoundError:
        lock.release()
        conn_id.send("No Records".encode('utf-8'))
        print(f"[+] No survey has been recorded yet! (Host : {client_address})")


def log_survey_data(data, client_address):
    try:
        lock.acquire()
        if not os.path.exists('survey_data.csv'):
            with open('survey_data.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(['SNo.', 'Full Name', 'Project Rating', 'Recorded Time'])
        with open('survey_data.csv', 'r') as file:
            temp = csv.reader(file)
            temp_list = list(temp)
            sno = temp_list[-1][0]

        if sno != 'SNo.':
            sno = int(sno) + 1
            data = f"{sno},{data}".split(",")
        else:
            data = f"1,{data}".split(",")

        with open('survey_data.csv', 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)
        lock.release()
        print(f"[+] Client : [{client_address[0]}] has performed the survey and the data is logged into the server!")
        return True

    except Exception as e:
        print(e)
        return False


def connection_msg(connection_id, client_address):
    print(f"[+] TCP connection is established with the host : {client_address}")
    connection_id.send("TCP Connection is established with the server".encode('utf-8'))


def help_cmd(connection_id, address):
    x = ["SHOW ACTIVE", "READ SURVEY", "SHOW VISITED", "LOGOUT", "HELP"]
    y = ["     - Show the number of active users.", "     - Read the survey data.",
         "    - Show the number of total server visitors.", "          - Logout from the server.",
         "            - Show all the available commands."]

    result_str = "\n\tList of available commands :"

    list_of_commands = dict(map(lambda i, j: (i, j), x, y))
    for key, val in list_of_commands.items():
        result_str += f"\n\t{key}{val}"

    connection_id.send(result_str.encode('utf-8'))
    print(f"[+] Query has been sent to [{address}].")


def read_survey(connection_id, address):
    send_records(connection_id, address)


def show_visited(connection_id, address):
    lock.acquire()
    with open('number_of_clients.txt', 'rt') as f:
        total_clients = f.read()
    lock.release()
    connection_id.send(f"[+] Total Visitors : {total_clients}".encode('utf-8'))
    print(f"[+] Query has been sent to [{address}].")


def show_active(connection_id, address):
    live_count = threading.active_count() - 1
    connection_id.send(f"[+] Live clients : {live_count}".encode('utf-8'))
    print(f"[+] Query has been sent to [{address}].")


def logout_cmd(connection_id, address):
    print(f"[+] Logging out...[{address}]")
    connection_id.send(f"[+] Logged out!".encode('utf-8'))
    connection_id.close()


def admin_panel(connection_id, address):
    while True:
        command = connection_id.recv(1024).decode('utf-8')

        if command == 'logout':
            logout_cmd(connection_id, address)
            break

        elif command == 'help':
            help_cmd(connection_id, address[0])

        elif command == 'show active':
            show_active(connection_id, address[0])

        elif command == 'show visited':
            show_visited(connection_id, address[0])

        elif command == 'read survey':
            read_survey(connection_id, address[0])

        else:
            print(f"[-] Wrong query from [{address[0]}].")
            connection_id.send("[-] Command does not exist...".encode('utf-8'))


def handle_clients(connection_id, address):
    connection_msg(connection_id, address)
    user_type = connection_id.recv(1024).decode('utf-8').split()
    if user_type[-1] == ADMIN_FLAG:
        if authorize(user_type):
            print(f"[+] Host with IP : [{address[0]}] is a root user!")
            connection_id.send("1".encode('utf-8'))
            admin_panel(connection_id, address)

        else:
            print("[-] Root user authentication failed!")
            print(f"[!] Host with IP : [{address[0]}] is trying to get the root access with incorrect credentials!")
            connection_id.send("0".encode('utf-8'))

        connection_id.close()

    else:
        survey_data = connection_id.recv(1024).decode('utf-8')
        if 'NULL' != survey_data:
            status = log_survey_data(survey_data, address)
            if status:
                connection_id.send('1'.encode())
                connection_id.close()

            else:
                connection_id.send('0'.encode())
                connection_id.close()
        else:
            print(f"[-] Client : [{address[0]}] has not performed the survey correctly!")
            connection_id.close()


def main():
    ip = 'localhost'
    # ip = "192.168.10.189"
    port = 9191

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((ip, port))
            server_socket.listen(1)
            print(f"[+] Server is listening on port [{port}]...")
            number_of_clients = 0
            while True:
                conn_id, address = server_socket.accept()
                lock.acquire()
                number_of_clients += 1
                with open('number_of_clients.txt', 'w') as f:
                    f.write(str(number_of_clients))
                lock.release()
                client = threading.Thread(target=handle_clients, args=(conn_id, address))
                client.start()
    except KeyboardInterrupt:
        print("[-] Caught Keyboard Interrupt!")

    except BrokenPipeError:
        print("[-] Broken Pipe Error! Connection is terminated!")

    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
