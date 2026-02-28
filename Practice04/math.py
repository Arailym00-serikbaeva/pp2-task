import math
import random

#1
print(min(5, 10, 2))
print(max(5, 10, 2))
print(abs(-7))

import math
d=float(input("Input degree:"))
r=d*math.pi/180
print("Output radian:",round(r,6))

#2
print(round(3.14159, 2))
print(pow(2, 3))

#3
print(math.sqrt(16))
print(math.ceil(4.3))
print(math.floor(4.7))

#4
print(math.sin(math.pi / 2))
print(math.cos(0))
print(math.pi)
print(math.e)

#5
print(random.random())        
print(random.randint(1, 10))  
items = ["apple", "banana", "cherry"]
print(random.choice(items))
random.shuffle(items)
print(items)
