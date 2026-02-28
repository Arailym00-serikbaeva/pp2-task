#1
numbers = [1, 2, 3, 4]
iterator = iter(numbers)
print(next(iterator)) 
print(next(iterator)) 

n=int(input())
for i in range(1,n+1):
    print(i**2)
    
#2
numbers = [10, 20, 30]
iterator = iter(numbers)
for num in iterator:
    print(num)


def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i
n = int(input().strip())
first = True
for num in even_numbers(n):
    if not first:
        print(",", end="")
    print(num, end="")
    first = False



#3
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self
  def __next__(self):
    x = self.a
    self.a += 1
    return x
myclass = MyNumbers()
myiter = iter(myclass)
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

def divisible_numbers(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = int(input().strip())
first = True
for num in divisible_numbers(n):
    if not first:
        print(" ", end="")
    print(num, end="")
    first = False
    

#4
def count_up_to(max_value):
    current = 1
    while current <= max_value:
        yield current
        current += 1
for number in count_up_to(4):
    print(number)

a,b=map(int,input().split())
for i in range(a,b+1):
    print(i**2)

#5
squares = (x * x for x in range(5))
for square in squares:
    print(square)

n=int(input())
for i in range(-n,1):
    print(-i)
