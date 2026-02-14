#1
class A:
    def method_a(self):
        print("A")

#2
class B:
    def method_b(self):
        print("B")

#3
class C(A, B):
    pass

#4
class D(A, B):
    pass

#5
class E(A, B):
    pass

c = C()
c.method_a()
c.method_b()