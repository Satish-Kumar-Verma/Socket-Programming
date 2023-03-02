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

    def update_session(self):
        self.time_of_creation = datetime.datetime.now().strftime("%H:%M:%S")

    def get_cookie(self):
        return self

    @staticmethod
    def valid(cookie):
        current_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
        ckt = datetime.datetime.strptime(cookie.time_of_creation, "%H:%M:%S")
        if round((current_time - ckt).total_seconds() / 60) > cookie.session_life:
            print("Session Expired!")
            return False
        return True

    def __str__(self):
        return f"""Token :{self.token},\nCreated time :{self.time_of_creation},
        \rSession life :{self.session_life} minutes"""
