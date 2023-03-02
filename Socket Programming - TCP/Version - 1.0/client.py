import socket
import datetime
from prettytable import PrettyTable
import csv


def display_records():
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
            line = conn_id.recv(1024)
            while True:
                if "DONE" in line.decode():
                    temp = line.decode().replace("DONE", "").encode()
                    file.write(temp)
                    break
                file.write(line)
                line = conn_id.recv(1024)

        print("[+] Survey data is received!")
        return True
    except Exception as e:
        print(e)
        print("Exiting...")
        return False


# def admin_panel(connection_id):
#


def admin_auth(connection):
    username = input("Enter your username : ")
    password = input("Enter your password : ")

    cred = f"{username},{password}"

    connection.send(cred.encode('utf-8'))

    auth_result = connection.recv(1024).decode('utf-8')
    return bool(int(auth_result))


def perform_survey(conn_id):
    while True:
        name = input("Enter your name : ")
        rating = input("How much would you rate out of 10 : ")
        rating_time = datetime.datetime.now().strftime('%d-%m-%y %I:%M:%S')

        print("[+] Your survey has been recorded!")
        send_flag = input("Send the survey data -> [S] or Edit the survey -> [E] : ").lower()
        if send_flag == 's':
            break

    survey_data = f"{name},{rating},{rating_time}"

    print("[+] Sending survey data to the server...")
    conn_id.send(survey_data.encode('utf-8'))
    flag = conn_id.recv(1024).decode('utf-8')
    if bool(int(flag)):
        print("[+] Your survey has been sent to the server.")

    else:
        print("[-] Server did not receive the data!")


def main():
    print()
    print("##################### Welcome to Survey App! ######################")
    print("[+] Root User   : Can view the survey results.")
    print("[+] Normal User : Only allowed to perform the survey!")
    print()
    print("###################################################################")
    print("[+] You can choose your role after getting connected to the server.")
    print("###################################################################")
    print()
    host, port = input("[+] Enter the host\'s IP and port number separated by a space : ").split()
    port = int(port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect_ex((host, port))
            msg = client_socket.recv(1024).decode('utf-8')  # default -> utf-8, you may not specify it

            print(f"[+] {msg} with the host : {host}\n")

            choice = input("Choose your role --> Root user or Normal user [R/n] : ").lower()
            client_socket.send(choice.encode('utf-8'))

            if choice == 'r':
                if admin_auth(client_socket):
                    print("[+] Root user authentication successful!")

                    view_data = input("View Data? [V] :").lower()
                    if view_data == 'v':
                        client_socket.send(view_data.encode('utf-8'))
                        if get_records(client_socket):
                            display_records()
                        else:
                            exit(1)

                else:
                    print("[-] Authentication failed!")
                    print("[-] Connection terminated!")
                    exit(1)

            elif choice == 'n':
                perform_survey(client_socket)

        except Exception as e:
            print(f'{e}')

        finally:
            client_socket.close()


if __name__ == '__main__':
    main()


