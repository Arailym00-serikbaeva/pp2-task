from functools import reduce

numbers = [1, 2, 3, 4, 5]

# 1
print(list(map(lambda x: x*2, numbers)))

#  2
print(list(map(lambda x: x**2, numbers)))

# 3
print(list(filter(lambda x: x % 2 == 0, numbers)))

# 4
print(list(filter(lambda x: x > 3, numbers)))

# 5
print(reduce(lambda x, y: x + y, numbers))