#1
file = open("example.txt", "r")
print(file.read())
file.close()

#2
with open("example.txt", "r") as f:
    print(f.readline())

#3
with open("example.txt", "r") as f:
    for line in f:
        print(line)

#4
with open("example.txt", "r") as f:
    lines = f.readlines()
    print(lines)

#5
with open("example.txt", "r") as f:
    print(len(f.read()))