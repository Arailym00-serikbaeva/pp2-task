
#1
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
p1 = Person("Ali", 25)
print(p1.name) 
print(p1.age) 

#2
class Car:
    def __init__(self, brand="Toyota", year=2020):
        self.brand = brand
        self.year = year
c1 = Car()
c2 = Car("BMW", 2023)
print(c1.brand, c1.year)  # Toyota 2020
print(c2.brand, c2.year)  # BMW 2023


#3
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area = width * height
r = Rectangle(5, 4)
print(r.area)  # 20


#4
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    def info(self):
        return f"Name: {self.name}, Grade: {self.grade}"
s = Student("Aruzhan", 90)
print(s.info())

#5
class ShoppingCart:
    def __init__(self):
        self.items = []
    def add_item(self, item):
        self.items.append(item)
cart = ShoppingCart()
cart.add_item("Apple")
cart.add_item("Banana")
print(cart.items)  # ['Apple', 'Banana']

