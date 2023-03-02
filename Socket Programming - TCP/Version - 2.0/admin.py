import socket
from prettytable import PrettyTable
import csv
import sys


def help_command(data):
    for key, val in data.items():
        print(f"{key}{val}")


def display_records():
    print("[+] Displaying the survey...\n")
    with open('survey_data_client.csv', 'r') as file:
        data = csv.reader(file)
        table = PrettyTable()
        table.field_names = next(data)

        for row in data:
            table.add_row(row)
    print(table)


def get_records(conn_id):
    try:
        with open("survey_data_client.csv", "wb") as file:
            line = conn_id.recv(1024).decode('utf-8')
            if line == "No Records":
                return False
            while True:
                if "AEIOUYRUG" in line:
                    temp = line.replace("AEIOUYRUG", "").encode('utf-8')
                    file.write(temp)
                    break
                file.write(line.encode('utf-8'))
                line = conn_id.recv(1024).decode('utf-8')

        print("[+] Survey data is received!")
        return True
    except Exception as e:
        print(e)
        print("Exiting...")
        sys.exit(-1)


def read_survey(connection_id):
    if get_records(connection_id):
        display_records()

    else:
        print("[-] Does not receive the data from the server.")


def main():
    print()
    print("##################### Welcome to Survey App! ######################")
    print()
    print("###################################################################")
    print("[+] You are currently using the admin application.")
    print("[+] You can monitor the activities of the users using [admin.exe].")
    print("###################################################################")
    print()

    server_ip, port = input("Enter the server ip and port number separated by a space : ").split()
    port = int(port)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, port))
            connection_status = client_socket.recv(1024).decode('utf-8')
            print(f"[+] {connection_status}!")

            print("\n[+] Type :[LOGIN] and press Enter to enter the admin panel.\n")
            cmd = input("User@Server$").lower()
            if cmd == "login":
                username = input("Enter the root username : ")
                password = input("Enter the root password : ")
                credentials = f"{username} {password} IaMnOtAnAdMiN"
                client_socket.send(credentials.encode('utf-8'))
                auth_status = client_socket.recv(1024).decode('utf-8')
                auth_status = bool(int(auth_status))
                if auth_status:
                    print("[+] Root user authentication successful!")

                else:
                    print("[-] Authentication failed!")
                    client_socket.close()
                    print('[-] Exiting...')
                    sys.exit(-1)

            else:
                print(f"[-] Command {cmd} does not exist.")

            print("\n[+] Type [HELP] to print the list of commands.")
            while True:
                command = input("Admin@Server#").lower()
                if command == 'logout':
                    client_socket.send(command.encode('utf-8'))
                    response = client_socket.recv(1024).decode('utf-8')
                    client_socket.close()
                    print(response)
                    break

                elif command == 'read survey':
                    client_socket.send(command.encode('utf-8'))
                    if get_records(client_socket):
                        display_records()

                    else:
                        print("[+] No survey has been recorded yet!")

                else:
                    client_socket.send(command.encode('utf-8'))
                    response = client_socket.recv(1024).decode('utf-8')
                    print(response)
    except KeyboardInterrupt:
        print("[-] Caught Keyboard Interrupt!")

    except ConnectionRefusedError:
        print("[-] Connection Refused!")

    except ConnectionAbortedError:
        print("[-] Connection Aborted!")

    except UnboundLocalError:
        print("[-] Unbound local error!")

    except ValueError:
        print("[-] Someone might not perform the survey correctly!")


if __name__ == '__main__':
    main()
