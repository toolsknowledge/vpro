"""
    tuples
    ******
        collection of hetrogeneous elements
        () / tuple()
        duplicates allowed
        index starts from 0 (supports negative indexes also)
        immutable
"""

# Example-1
# import sys
# list1 = [10,20,30,40,50]
# t1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(t1))

# Example-2
# t1 = (10,20,30,40,50)
# e1,e2,e3,e4,e5 = t1
# print(e1,e2,e3,e4,e5)

# t2 = (100,200,300,400,500)
# e1,*list1,e5 = t2

# e2,*list2 = list1

# e3,e4 = list2

# print(e1,e2,e3,e4,e5)


# Example-3
# t1 = (10,20,30,40,50)
# print(type(t1))

# t2 = (100)
# print(type(t2))

# t3 = (100,)
# print(type(t3))

# t4 = 1000,2000,3000,4000,5000
# print(type(t4))

# t5 = 10000,
# print(type(t5))


# Example-4
# a = 100
# b = 200
# b,a = a,b
# print(b)
# print(a)

# Example-5
# t1 = 10,20,10,20,20,30
# print(t1.count(10))
# print(t1.count(20))
# print(t1.count(40))
# print(t1.index(20))
# print(t1.index(10))


# Example-6
# t1 = 10,20,30,40,50
# t1[0] = 1000

# Example-7
# t1 = (10,20,30,40,50)
# list1 = list(t1)
# list1[0] = 1000
# t1 = tuple(list1)
# print(t1)

# Example-8
# def test_func():
#     num1 = 200
#     num2 = 100
#     return num1+num2, num1-num2, num1*num2, num1/num2

# add,sub,mul,div = test_func()
# print(add,sub,mul,div)


# Example-9
d1 = {
    (10,20) : "Hello"
}
print(d1[(10,20)])
