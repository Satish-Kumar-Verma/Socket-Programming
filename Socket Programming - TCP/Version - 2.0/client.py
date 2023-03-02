import socket
import datetime


def perform_survey(conn_id):
    try:
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
        transfer_flag = conn_id.recv(1024).decode('utf-8')
        if bool(int(transfer_flag)):
            print("[+] Your survey has been sent to the server.")

        else:
            print("[-] Server did not receive the data!")

    except KeyboardInterrupt:
        conn_id.send("NULL".encode('utf-8'))


def main():
    print()
    print("##################### Welcome to Survey App! ######################")
    print()
    print("###################################################################")
    print("[+] You are currently using the client application.")
    print("[+] You can only perform the survey using [client.exe].")
    print("###################################################################")
    print()

    try:
        server_ip, port = input("Enter the server ip and port number separated by a space : ").split()
        port = int(port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            current_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
            client_socket.connect((server_ip, port))
            connection_status = client_socket.recv(1024).decode('utf-8')
            current_time_2 = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
            print(f"[+] {connection_status}.")
            diff = (current_time_2 - current_time).total_seconds() * 1000.0
            print(f"RTT : {diff:.4f} ms")
            client_socket.send("IaMnOrMaL".encode('utf-8'))
            perform_survey(client_socket)

    except KeyboardInterrupt:
        print("[-] Caught Keyboard Interrupt!")
    except ConnectionRefusedError:
        print("[-] Connection Refused!")
    except ConnectionAbortedError:
        print("[-] Connection Aborted!")


if __name__ == '__main__':
    main()
