import os

# 1
os.mkdir("folder1")

# 2
os.mkdir("folder2")

# 3
print(os.listdir())

# 4
print(os.getcwd())

# 5
if os.path.exists("folder1"):
    print("Folder exists")