#1
numbers = [1, 2, 3, 4]
iterator = iter(numbers)
print(next(iterator)) 
print(next(iterator)) 

#2
numbers = [10, 20, 30]
iterator = iter(numbers)
for num in iterator:
    print(num)

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

#4
def count_up_to(max_value):
    current = 1
    while current <= max_value:
        yield current
        current += 1
for number in count_up_to(4):
    print(number)

#5
squares = (x * x for x in range(5))
for square in squares:
    print(square)
