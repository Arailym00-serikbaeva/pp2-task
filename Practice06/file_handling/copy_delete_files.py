import shutil
import os

#1
shutil.copy("example.txt", "copy_example.txt")

#2
shutil.copy("test1.txt", "backup_test1.txt")

#3
if os.path.exists("copy_example.txt"):
    os.remove("copy_example.txt")

#4
if os.path.exists("backup_test1.txt"):
    os.remove("backup_test1.txt")

#5
shutil.copy("test2.txt", "copy_test2.txt")