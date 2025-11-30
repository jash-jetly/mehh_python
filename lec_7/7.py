#####
class Person:
    def __init__(self,fname,lname):
        self.fname =fname
        self.lname = lname

    def print_full_name(self):
        return self.fname + " " + self.lname

##child class
class User(Person):
    def __init__(self, fname, lname):
        # self.fname = fname
        # self.lname = lname
        super().__init__(self,fname, lname)
    
## from parent - overrides parent function
    def print_full_name(self):
        return self.fname + " and " + self.lname

##its owns
    def set_username(self):
        return self.fname

# ##make object of person
# user_one= Person("Aashika","Pandey")
# print(user_one.fname)
# print(user_one.lname)

## make object of user class
user_one= User("Jash","Jetly")
# print(user_one.fname)# Aashika
# print(user_one.lname)# Pandey
print(user_one.print_full_name())

