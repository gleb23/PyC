__author__ = 'gleb23'

class A(object):
    def foo(self):
        return self.__class__

class B(A):
    pass

print A().foo()
print B().foo()

class Metaclass(type):
    def __new__(cls):
        type("A", (), {})

if Metaclass() != Metaclass():
    print 'yes'