#1
class Person:
    def __init__(self, name):
        self.name = name

#2
class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

#3
class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

#4
class Worker(Person):
    def __init__(self, name, job):
        super().__init__(name)
        self.job = job

#5
class Manager(Person):
    def __init__(self, name, department):
        super().__init__(name)
        self.department = department