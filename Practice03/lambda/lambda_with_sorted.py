students = [("Ali",20),("Dana",18),("Arman",22)]

#1
print(sorted(students, key=lambda x: x[1]))

#2
print(sorted(students, key=lambda x: x[0]))

#3
print(sorted(students, key=lambda x: x[1], reverse=True))

#4
print(sorted(students, key=lambda x: len(x[0])))

#5
print(sorted(students, key=lambda x: x[0][-1]))