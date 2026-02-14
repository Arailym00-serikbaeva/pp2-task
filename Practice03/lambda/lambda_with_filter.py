numbers = [1,2,3,4,5,6,7,8,9]

#1
print(list(filter(lambda x: x%2==0, numbers)))

#2
print(list(filter(lambda x: x>5, numbers)))

#3
print(list(filter(lambda x: x<4, numbers)))

#4
print(list(filter(lambda x: x!=3, numbers)))

#5
print(list(filter(lambda x: x%3==0, numbers)))