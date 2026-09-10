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

 






























