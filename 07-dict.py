# dictionary - key & value pairs
# {} / dict()
# keys are immutable and values are mutable

# Example-1
# student = {
#     "id" : 101,
#     "name" : "Std1",
#     "course" : "GenAI",
#     "marks" : 95
# }
# print(student)
# print(student["id"])
# print(student["branch"])
# print(student.get("branch"))
# print(student.get("branch","CSE"))
# print(type(student))


# Example-2
# student = {}
# student["id"] = 101
# student["name"] = "std1"
# student["marks"] = 90
# print(student)

# student["name"] = "student1"
# print(student)

# del student["marks"]
# print(student)

# print(student.get("marks",0))


# Example-3
# d1 = {
#     "key1" : 100,
#     "key1" : 1000
# }
# print(d1)

# Example-4
#int , float, bool, str, tuple, frozenset (immutables)
# s1 = frozenset()
# d1 = {
#     100 : 1,
#     10.1 : 2,
#     True : 3,
#     "Hello" : 4,
#     (10,20) : 5,
#     s1 : 6,
#     # [10,20] : 7
#     # {}: 8
#     # set() : 9,
#     # bytearray() : 10
# }
# print(d1)

# Example-5
# d1 = {
#     "key1" : "GenAI",
#     "key2" : "AgenticAI"
# }
# print(d1.keys())
# print(d1.values())
# print(d1.items())
# for key in d1:
#     print(key)
# for value in d1.values():
#     print(value)
# for key,value in d1.items():
#     print(key,value,sep="----->")


# Example-6
# d1 = {
#     101 : {
#         "name" : "Std1",
#         "marks" : 90
#     },
#     102 : {
#         "name" : "Std2",
#         "marks" : 95
#     }
# }
# print(d1[101]["name"])
# print(d1[102]["marks"])

# for inner in d1.values():
#     for key,value in inner.items():
#         print(key,value,sep="---->")

# Example-7
# print( {x:x*x for x in range(1,7)} )

# Example-8
# str = "Hello"
# count = {}  # {"H":1,"e":1,"l":2,"o":1}
# for ch in str:
#     count[ch] = count.get(ch,0) + 1

# print(count)

# Example-9
# str = "python java python java python"
# words = str.split()
# print(words)    #['python', 'java', 'python', 'java', 'python']

# Example-10
# d1 = {
#     "rollno":101
# }
# d2 = {
#     "name" : "Std1",
#     "marks" : 90
# }
# d1.update(d2)
# print(d1)

# Example-11
# d1 = {
#     "roll" : 101,
#     "name" : "Std1",
#     "marks" : 90
# }
# if "marks" in d1:
#     print("Available !!!")
# else:
#     print("Not Available !!!")



