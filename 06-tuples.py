"""
    tuple - collection of elements
    immutable
    hetrogeneous elements
    ordered
    ()
    ocupies "less memory" compated to "lists"
    tuple operations are "speed" because of "immutablity"
"""

# Example-1
# t1 = (10,20,30,40,50)
# print(type(t1))

# e1,e2,e3,e4,e5 = t1
# print(e1,e2,e3,e4,e5)

# e1,e2,*list1 = t1
# e3,*list2 = list1
# e4,e5 = list2
# print(e1,e2,e3,e4,e5)

# Example-2
# t1 = (10,20,30,40,50,10,20)
# print(t1.count(10))
# print(t1.count(50))
# print(t1.count(60))
# print(len(t1))
# print(max(t1))
# print(min(t1))
# print(sum(t1))
# print(t1.index(10))
# print(t1.index(50))

# Example-3
# t1 = (10,20)
# t2 = (30,40,50)
# t3 = t1 + t2
# print(t3)
# print(30 in t3)
# print(300 not in t3)
# print(300 in t3)
# t4 = t3 * 2
# print(t4)

# Example-4
# t1 = 10,20,30,40,50
# for element in t1:
#     print(element)

# for index,element in enumerate(t1):
#     print(index,element,sep="→")

# t2 = 100,200,300,400,500
# for element1,element2 in zip(t1,t2):
#     print(element1,element1,sep="→")

# t3 = "Python","ML","DL","NLP","GenAI","AgenticAI"
# i = 0
# while(i<len(t3)):
#     print(t3[i])
#     i+=1

# Example-5
# t1 = (10,20),(100,200),(1000,2000)
# for outer in t1:
#     for index,element in enumerate(outer):
#         print(index,element,sep="→")
#     print("----------------------")


# Example-6
# d1 = {
#     (10,20) : "Hello"
# }
# print(d1[(10,20)])

# Example-7
# from collections import namedtuple
# emps = namedtuple("Employees",["name","age","salary"])
# t1 = emps("Samba",40,500000)
# print(t1)
# print(t1.name, t1.age, t1.salary)

# Example-8
# def test(num1,num2):
#     return num1+num2, num1-num2, num1*num2, num1/num2

# t1 = test(200,100)
# add,sub,mul,div = t1
# print(add)
# print(sub)
# print(mul)
# print(div)

# Example-9
# t1 = ( [10,20],[30,40] )
# t1[0][0] = 1000
# t1[1][1] = 4000
# print(t1)


# Example-10
# map()

#t1 = (100,200,300,400,500)      #(1,2,3,4,5) (map())


#t2 = (1,2,3,4,5)            # even elements (filter())


#t3 = 1000,2000,3000,4000,5000   # 15000 (reduce())

# Example-11
t1 = 10,
print(type(t1))

t2 = 100
print(type(t2))