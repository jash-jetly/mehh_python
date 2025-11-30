from abc import ABC, abstractmethod

class Human(ABC):
    @abstractmethod
    def talk(self):
        print('talkinggg.......')

class Man(Human):
    def talk(self):
        print('hmm...')

     def walk(self):
         print('walking')

person = Man()
person.walk()

