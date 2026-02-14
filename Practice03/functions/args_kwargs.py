#1
def print_args(*args):
    print(args)

#2
def sum_args(*args):
    print(sum(args))

#3
def print_kwargs(**kwargs):
    print(kwargs)

#4
def show_info(**kwargs):
    for k, v in kwargs.items():
        print(k, v)

#5
def mix(a, *args, **kwargs):
    print(a, args, kwargs)

print_args(1, 2, 3)
sum_args(5, 10, 15)
print_kwargs(name="Ali", age=20)
show_info(city="Almaty", country="KZ")
mix(1, 2, 3, x=10, y=20)