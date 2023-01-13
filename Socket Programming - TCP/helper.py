
# import pickle
import datetime


class Credentials:
    def __init__(self):
        self.username = ""
        self.password = ""

    def set_username(self, uname):
        self.username = uname

    def set_password(self, pwd):
        self.password = pwd

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password


class Cookie:
    def __init__(self):
        self.token = ""
        self.session_life = 2
        self.time_of_creation = ""
        self.set_time_of_creation()

    def set_token(self, tk):
        self.token = tk

    def set_session_life(self, s_life):
        self.session_life = s_life

    def set_time_of_creation(self):
        self.time_of_creation = datetime.datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def valid(cookie):

        print(f"Cookie created time : {cookie.time_of_creation}")
        print(f"Current time : {datetime.datetime.now()}")
        _ = input("wait 2 min")

        current_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
        ckt = datetime.datetime.strptime(cookie.time_of_creation, "%H:%M:%S")
        if round((current_time - ckt).total_seconds() / 60) > cookie.session_life:
            print("Session Expired!")
            return False
        return True

    def __str__(self):
        return f"""Token :{self.token},\nCreated time :{self.time_of_creation},
        \rSession life :{self.session_life} minutes"""


# c = Cookie()
# c1 = Cookie()
# c1.set_token("TK_1234")
# c1.set_session_life(2)
# Cookie.valid(c1)
# print(c1)




#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# import pickle
# cred = Credentials()
#
# username = 'Baking_Bad'
# password = 'CN_Group_1'
# cred.set_username(username)
# cred.set_password(password)
#
# print(cred.username)
# print(cred.password)
#
# with open('root_credentials.dat', 'wb') as file:
#     pickle.dump(cred, file)
#
# with open('root_credentials.dat', 'rb') as file:
#     obj = pickle.load(file)
#     print(obj.username)
#     print(obj.password)
#
#
# def get_credentials():
#     with open('root_credentials.dat', 'rb') as file:
#         obj = pickle.load(file)
#         uname = obj.get_username()
#         pwd = obj.get_password()
#         return uname, pwd
#
#
# data = get_credentials()
# print(data[0], data[1])


# import csv
#
# with open("survey_data.csv", 'w', newline='') as file:
#     w = csv.writer(file)
#
#     w.writerow(['SNo.', 'Full Name', 'Project Rating', 'Recorded Time'])

# import csv
# from prettytable import PrettyTable
#
# with open('survey_data_client.csv', 'r') as file:
#     data = csv.reader(file)
#     print("Displaying.......")
#     table = PrettyTable()
#     table.field_names = next(data)
#
#     for row in data:
#         table.add_row(row)
#
#     print(table)
