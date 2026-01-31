""" #204) 
n = int(input())
arr = list(map(int, input().split()))

count = 0
for x in arr:
    if x > 0:
        count += 1

print(count)
"""

""" #205)
n = int(input())
if n <= 0:
    print("NO")
else:
    while n % 2 == 0:
        n //= 2
    if n == 1:
        print("YES")
    else:
        print("NO")
"""

"""206)
a=int(input())
b=list(map(int,input().split()))
c=max(b)
print(c)"""

"""207)
a=int(input())
b=list(map(int,input().split()))
s=max(b)
n=0
for i in b:
  n+=1
  if i==s:
    print(n)
"""

"""208) 
a=int(input())
b=1
while b<=a:
  print(b, end=" ")
  b*=2
"""

"""209)
a=int(input())
b=list(map(int,input().split()))
c=min(b)
d=max(b)
for i in b:
  if i==d:
    i=c
    print(c, end=" ")
    continue
  else:
    print(i, end=" ")
"""

"""210)
a=int(input())
b=list(map(int,input().split()))
b.sort()
b.reverse()
for i in b:
  print(i, end=" ")
"""

"""212)
a=int(input())
b=list(map(int,input().split()))
for i in b:
  print(i**2, end=" ")
"""

"""211)
"""

"""215)
a=int(input())
s=set()
for i in range(a):
  b=input()
  s.add(b)
n=0
for i in s:
  n+=1
print(n)
"""

a=int(input())
if a%4==0 or a%100==0 or a%400==0:
  print("YES")
else:
  print("NO")




