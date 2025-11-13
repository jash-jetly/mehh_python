class student:
    roll_number=8
    def __init__ (self, roll_number):
        self.roll_number=roll_number

    def learn(self):
        return "learning"

jash = student(123)
print(jash.learn())


class Faculty:
    pass

prasad=Faculty()
prasad.skills = ['python', 'js']
print(prasad.skills)

gatik = Faculty()

Faculty.skills = ['skills toh nahi hai', 'read', 'write']
print(gatik.skills)
