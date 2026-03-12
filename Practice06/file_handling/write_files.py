#1
with open("test1.txt", "w") as f:
    f.write("Hello World")

#2
with open("test2.txt", "w") as f:
    f.write("Python programming")

#3
with open("test3.txt", "a") as f:
    f.write("Append text\n")

#4
lines = ["Line1\n", "Line2\n", "Line3\n"]
with open("test4.txt", "w") as f:
    f.writelines(lines)

#5
text = "Practice writing files"
with open("test5.txt", "w") as f:
    f.write(text)