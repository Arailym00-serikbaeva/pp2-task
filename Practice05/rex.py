#1
import re
s = input()
x = re.findall("^a.*b", s)
if x:
    print("Match")
else:
    print("No match")
 
#2
import re
s = input()
x = re.findall("^ab{2,3}", s)
if x:
    print("Match")
else:
    print("No Match")
 
#3
import re
s = input()
x = re.findall("^[a-z]+[_][a-z]+", s)
print(x)
if x:
    print("Match")
else:
    print("No Match")
 
#4
import re
s = input()
x = re.findall("^[A-Z][a-z]+", s)
print(x)
if x:
    print("Match")
else:
    print("No Match")
 
#5
import re
s = input()
x = re.findall("a.+b$", s)
print(x)
if x:
    print("Match")
else:
    print("No Match")
 
#6
import re
s = input()
r = re.sub("[ ,.]", ":", s)
print(r)

#7
import re
s = input()
r = re.sub("[_]", "", s)
print(r)

#8
import re
s = input()
result = re.findall(r'[A-Z][a-z]*', s)
print(result)

#9
import re
s = input()
result = re.sub(r"(?<!^)([A-Z])", r" \1", s)
print(result)

#10
import re
s = input()
result = re.sub(r"(?<!^)([A-Z])", r"_\1", s).lower()
print(result)