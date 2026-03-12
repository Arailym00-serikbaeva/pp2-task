#1
n = ["Aisha", "Alua", "Arman"]
for i, j in enumerate(n):
    print(f"{i}: {j}")

#2
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")


names = ["Ali", "Aruzhan", "Dana"]
scores = [85, 90, 78]

#3
for i, name in enumerate(names):
    print(i, name)

#4
for name, score in zip(names, scores):
    print(name, score)

#5
for i, (name, score) in enumerate(zip(names, scores)):
    print(i, name, score)

#6
print(list(enumerate(names)))
print(list(zip(names, scores)))