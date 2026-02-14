#1
def add(a, b):
    return a + b

#2
def square(x):
    return x * x

#3
def is_even(x):
    return x % 2 == 0

#4
def get_full_name(first, last):
    return first + " " + last

#5
def max_number(a, b):
    return a if a > b else b

print(add(2, 3))
print(square(4))
print(is_even(6))
print(get_full_name("Ali", "Khan"))
print(max_number(10, 5))