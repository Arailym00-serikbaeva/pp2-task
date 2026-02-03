#1
i=1
while i<10:
    if i==3:
        break
    print(i)
    i+=1

#2
s="Programming"
i=0
while i<len(s):
    if s[i]=='g':
        print("'g' found,stopping.")
        break
    i+=1

#3
i=1
while i<10:
    if i%2==0:
        print(f"First even number: {i}")
        break
    i+=1

#4
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

#5
t=0
n=1
while n<100:
    t+=n
    if t>50:
        print("Limit exceeded")
        break
    n+=1