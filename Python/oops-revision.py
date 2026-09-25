# class Test:
#     def __init__(self):
#         self.num1 = 200
#         self.num2 = 100

# obj1 = Test()
# a = obj1.num1
# b = obj1.num2
# res = a+b
# print(res)

# obj2 = Test()
# obj2.num1 = 2000
# print(obj2.num1)        # 2000


# obj3 = Test()
# print(obj3.num1)#200




# class Test:
#     def __init__(self,x,y):
#         self.num1 = x
#         self.num2 = y

# obj1 = Test(200,100)
# print(obj1.num1 - obj1.num2)


# class Test:
#     def __init__(self,param1,param2):
#         self.x = 100
#         self.y = param1
#         self.z = param2

# obj1 = Test(200,300)
# print(obj1.x + obj1.y + obj1.z)


# class Test:
#     def __init__(vpro):
#         vpro.num1 = 200

# obj1 = Test()
# print(obj1.num1)

# class Test:
#     def __init__(num1,self):
#         pass

# obj1 = Test()



# class Calc:
#     def power1(self):
#         num1 = 2
#         res = num1 ** num1
#         print(res)
#     def power2(self):
#         num1 = 2
#         res = num1 ** num1
#         return res
#     def power3(self,num1):
#         res = num1 ** num1
#         print(res)
#     def power4(self,num1):
#         res = num1 ** num1
#         return res

# obj1 = Calc()
# obj1.power1()
# x = obj1.power2()
# print(x)
# obj1.power3(2)
# y = obj1.power4(2)
# print(y)

# Cube


# class Parent:
#     def __init__(self,empno):
#         self.empno = empno


# class Child(Parent):
#     def __init__(self, empno,ename,esal):
#         super().__init__(empno)
#         self.ename = ename
#         self.esal = esal


# obj = Child(101,"Emp1",10000)
# print(f"Employee Number : {obj.empno}")
# print(f"Employee Number : {obj.ename}")
# print(f"Employee Number : {obj.esal}")



# class Parent:
#     def test1(self):
#         print("Hello")
# class Child(Parent):
#     def test2(self):
#         super().test1()
# class Subchild(Child):
#     def test3(self):
#         super().test2()

# obj = Subchild()
# obj.test3()


# class Test:
#     pass

# obj1 = Test()
# obj1.num1 = 200
# print(obj1.num1)


# class Parent:
#     def test1(self):
#         print("test1")

# class Child(Parent):
#     def test2(self):
#         print("test2")
# obj = Child()
# obj.test1()
# obj.test2()


# class Parent:
#     def func1(self):
#         print("Parent !!!")

# class Child(Parent):
#     def func2(self):
#         print("Child !!!")

# class Subchild(Child):
#     def func3(self):
#         print("Subchild !!!")

# obj = Subchild()
# obj.func1()
# obj.func2()
# obj.func3()


# class Parent1:
#     def test1(self):
#         print("Parent1")

# class Parent2:
#     def test2(self):
#         print("Parent2")

# class Child(Parent1,Parent2):
#     def test3(self):
#         print("Child")

# obj = Child()
# obj.test1()
# obj.test2()
# obj.test3()


# class Parent1:
#     def test1(self):
#         print("100")

# class Parent2:
#     def test1(self):
#         print("10000")

# class Child(Parent1,Parent2):
#     def test2(self):
#         print("200")

# obj = Child()
# obj.test1()
# obj.test2()


# class Parent:
#     def test1(self):
#         print("1")

# class Child1(Parent):
#     def test2(self):
#         print("11")

# class Child2(Parent):
#     def test2(self):
#         print("111")

# obj1 = Child1()
# obj1.test1()
# obj1.test2()

# obj2 = Child2()
# obj2.test1()
# obj2.test2()


# class Parent:
#     num1 = 100

# class Child1(Parent):
#     num2 = 200

# class Child2(Parent):
#     num3 = 300

# class Subchild(Child1,Child2):
#     num4 = 400

# obj = Subchild()
# print(obj.num1, obj.num2, obj.num3, obj.num4)


# class Test:
#     # class member
#     college = "CBIT"

# print(Test.college)


# class Test:
#     college = "CBIT"

# obj = Test()
# print(obj.college)      # currently no instance member, so automatically class member will access



# class Test:
#     # class member
#     college = "CBIT"        # Test.college

#     def __init__(self):
#         # instance member
#         self.college = "Vasavi"     # obj.college


# obj = Test()
# print(obj.college)
# print(Test.college)


# class Test:
#     college = "CBIT"

# Test.college = "CBIT College"
# print(Test.college)


# class Test:
#     college = "CBIT"

#     @classmethod        # decorator
#     def test(cls):
#         cls.college = "CBIT College"


# Test.test()
# print(Test.college)


# class Test:
#     pass

# obj = Test()
# obj.msg = "Welcome"     # adding instance variable

# print(Test.msg)


# class Test:
#     msg = "Hello"
#     x = 100

#     def __init__(self):
#         self.msg = "Welcome"

# print(Test.__dict__)        # used to find the class members
# obj = Test()
# print(obj.__dict__)         # used to find instance members


# method overriding
# polymorphsim
# both Parent and Child, must contain same "method signature"

# class Parent:
#     def db_func(self):
#         return "Oracle !!!"

# class Child(Parent):
#     def db_func(self):
#         return "ChromaDB !!!"

# obj = Child()
# print( obj.db_func() )


# method overloading (same method name, and different signatures)
# polymorphsim
# not supported by python

# class Test:
#     def test1(self):
#         print("Hello")
#     def test1(self,param1):
#         print(param1)
#     def test1(self,param1,param2):
#         print(param1,param2)
# obj = Test()
# obj.test1(100,200)


# class Test:
#     def __init__(self):
#         pass
#     def __init__(self, param1):
#         print(param1)
#     def __init__(self, param1,param2):
#         print(param1,param2)
# obj = Test(1,2)


# we can achieve overloading with the help of variable-length parameter
# class Test:
#     def add(self,*param1):
#         print(sum(param1))

# obj = Test()
# obj.add(10,20)
# obj.add(10,20,30)

# unable to "return" with constructor
# class Test:
#     def __init__(self):
#         return "Hello"

# obj = Test()

# while creating the object, python will add default contructor
# class Test:
#     pass

# obj = Test()


# class Test:
#     pass

# Test.x = 100        # adding class variable
# print(Test.x)       # accessing class variable

# obj1 = Test()
# # obj1.x = 1000       # instance variable
# print(obj1.x)       # accessing instance variable

# abstract - dont know function implementation
# child classes knows the implementation
# @abstractmethod - used to declare the abstractmethod
# from abc import ABC,abstractmethod
# class Test(ABC):
#     @abstractmethod
#     def test(self):
#         pass

# class Child1(Test):
#     def test(self):
#         print("Child1 impl....")

# obj1 = Child1()
# obj1.test()


# static
# object data(self), class data (cls)
# independent operations
# @staticmethod

# class Test:
#     @staticmethod
#     def add():
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(res)

#     def is_even(num1):
#         return num1 % 2 == 0
# Test.add()
# print(Test.is_even(10))
# print(Test.is_even(9))


# class Test:
#     def __init__(self,salary):
#         self.salary = salary

#     @staticmethod
#     def get_salary(salary):
#         return salary

# obj = Test(100000)
# print(obj.salary)   # accessing instance

# print(Test.get_salary(2000))    # acceesing static


# class Test:
#     # class member
#     salary = 10000

#     # instance member
#     def __init__(self):
#         self.salary = 20000

#     @staticmethod
#     def get_salary(salary):     # static member
#         return salary


# print(Test.salary)
# obj = Test()
# print(obj.salary)
# print(Test.get_salary(30000))


# class Test:
#     def __init__(self):
#         self.name = "VPro"

#     @staticmethod
#     def access_name():
#         print(self.name)

# Test.access_name()


# class Test:
#     def __init__(self):
#         self.name = "VPro"

#     @staticmethod
#     def access_name(obj):
#         print(obj.name)

# obj = Test()
# Test.access_name( obj )


# class Test:
#     college = "CBIT"
#     @staticmethod
#     def test():
#         print(Test.college)
# Test.test()


# by default test() is the static method
# class Test:
#     def test():
#         print("Hello")

# Test.test()


# class Test:
#     def __init__(self):
#         self.__name = "VPro"

#     def set_name(self):
#         self.__name = "VPro Skills"

#     def get_name(self):
#         return self.__name


# obj = Test()
# obj.__name

class Salary:
    def __init__(self):
        self.__sal = 100000

    def reveal_sal(self,username,password):
        if username == "admin" and password == "admin@123":
            print(self.__sal)
        else:
            print("Unauthorized access")


obj = Salary()
obj.reveal_sal("admin","admin@123")



































 






























