user_input=input("Enetr name: ")
user_password=input("password: ")

class User:
    def  __init__(self, username, password):
        self.username = username
        self.__password=password

    def get_password(self):
        return self.__password


class Auth(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def login(self, username, password):
        if self.username==username and self.get_password() == password:
            return True
        else:
            return False

    def reg():
        pass

obj = Auth('prasad', '123')
print(obj.login(user_input, user_password))




