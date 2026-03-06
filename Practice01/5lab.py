#501
#import re
#txt = input()
#x = re.findall("^Hello", txt)
#if x:
#  print("Yes")
#else:
#  print("No")

#502
import re
txt = input()
a=input()
x = re.search(a, txt)
b=0
if x!=None:
    print("Yes")
else:
    print("No")

#503
import re
s = input().strip()
p = input().strip()
m = re.findall(p, s)
print(len(m))

#503
import re
txt = input()
a=input()
x = re.search(a, txt)
b=0
for i in range(0,len(txt)):
    if x!=None:
        b+=1
print(b)

#504
a=input()
n=0
for i in a:
    if i=='1' or i=='2' or i=='3' or i=='4' or i=='5' or i=='6' or i=='7' or i=='8' or i=='9' or i=='0':
        print(i,end=" ")

#505
import re
s = input().strip()
if re.match(r'^[A-Za-z].*[0-9]$', s):
    print("Yes")
else:
    print("No")

#506
import re
text = input().strip()
match = re.search(r'\S+@\S+\.\S+', text)
if match:
    print(match.group())
else:
    print("No email")


#507
import re
s = input().strip()
p = input().strip()
r = input().strip()
result = re.sub(p, r, s)
print(result)

#508
import re
s = input().strip()
pattern = input().strip()
parts = re.split(pattern, s)
print(",".join(parts))

#509
import re
s = input().strip()
words = re.findall(r'\b\w{3}\b', s)
print(len(words))

#510
import re
s = input().strip()
if re.search(r'cat|dog', s):
    print("Yes")
else:
    print("No")

#511
import re
s = input().strip()
letters = re.findall(r'[A-Z]', s)
print(len(letters))

#512
import re
s = input().strip()
nums = re.findall(r'\d{2,}', s)
print(" ".join(nums))

#513
import re
s = input().strip()
words = re.findall(r'\w+', s)
print(len(words))

#514
import re
s = input().strip()
pattern = re.compile(r'\d+')
if pattern.fullmatch(s):
    print("Match")
else:
    print("No match")

#515
import re
s = input().strip()
result = re.sub(r'\d', lambda m: m.group()*2, s)
print(result)

#516
import re
s = input().strip()
match = re.search(r'Name:\s*(.+?),\s*Age:\s*(\d+)', s)
if match:
    name, age = match.groups()
    print(f"{name} {age}")

#517
import re
s = input().strip()
dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', s)
print(len(dates))

#518
import re
user_input = input()
pattern = r'\w+'
pattern = re.compile(pattern=pattern)
s = re.findall(pattern, user_input)
print(len(s))

#519
import re
user_input = input()
pattern = r'\w+'
pattern = re.compile(pattern=pattern)
s = re.findall(pattern, user_input)
print(len(s))




