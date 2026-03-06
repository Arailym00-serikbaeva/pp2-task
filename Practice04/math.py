import math
import random

#1
print(min(5, 10, 2))
print(max(5, 10, 2))
print(abs(-7))

<<<<<<< HEAD
import math
d=float(input("Input degree:"))
r=d*math.pi/180
print("Output radian:",round(r,6))
=======
d=float(input("Input degree:"))
r=d*math.pi/180
print("Output radian:",r)
>>>>>>> 1249109 (Add Practice5 - Python RegEx and receipt parsing examples)

#2
print(round(3.14159, 2))
print(pow(2, 3))

h=float(input("height: "))
a=float(input("Base, first value: "))
b=float(input("Base, second value: "))
t=((a+b)/2)*h
print("Expected Output: ",t)

#3
print(math.sqrt(16))
print(math.ceil(4.3))
print(math.floor(4.7))

n=int(input("Input number of sides: "))
s=float(input("Input the length of a side:  "))
c=(n*s*s)/(4*math.tan(math.pi/n))

#4
print(math.sin(math.pi / 2))
print(math.cos(0))
print(math.pi)
print(math.e)

<<<<<<< HEAD
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
area = base * height
print("Expected Output:", area)
=======

>>>>>>> 1249109 (Add Practice5 - Python RegEx and receipt parsing examples)

#5
print(random.random())        
print(random.randint(1, 10))  
items = ["apple", "banana", "cherry"]
print(random.choice(items))
random.shuffle(items)
print(items)
