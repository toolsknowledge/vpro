# dictionary : key & value pairs
# keys are "immutable" (dont modify)
# values are "mutable" (allows to modify)
# {} / "dict()" constructor
# key and value separated by using ":"

# Example-1
# d1 = {
#     "num1" : 200,
#     "num2" : 100
# }
# print(d1.keys())            # dict_keys(['num1', 'num2'])
# print(d1.values())
# print(d1.items())



# Example-2
# d1 = {
#     "num1" : 200,
#     "num2" : 100
# }
# x = d1["num1"]
# y = d1["num2"]
# add = x + y
# print(f"Addition : {add}")
# sub = x - y


# Example-3
# d1 = {
#     "num1" : 200
# }
# print( d1["num1"] )
# print( d1["num2"] )       # Err
# x = d1.get("num2",0)
# print(x)


# Example-4
# d1 = {}
# print(d1)

# # add the keys
# d1["num1"] = 1
# d1["num2"] = 200
# d1["num3"] = 300
# print(d1)

# # update the data
# d1["num1"] = 100
# print(d1)

# # delete num3 (>=3.x version)
# d1.pop("num3")
# print(d1)

# # delete last key
# d1.popitem()
# print(d1)

# # delete num1 by using del (old key)
# del d1["num1"]
# print(d1)

# # delete entire obj
# del d1
# print(d1)


# Example-5
# d1 = {
#     "num1" : 1,
#     "num1" : 100
# }
# print(d1)



# Example-6
# d1 = {
#     "num1":100,
#     "num2":100
# }
# print(d1)


# Example-7
# d1 = {
#     "num1" : 200,
#     "num2" : 100,
#     "num3" : 50
# }
# iterate the keys
# for key in d1.keys():
#     print(key)


# iterate the value
# for value in d1.values():
#     print(value)


# iterate both key & values
# for key,value in d1.items():
#     print(key,value)


# Example-8 (nested dictionary)
# d1 = {
#     "key1" : {
#         "msg" : "welcome"
#     }
# }
# print(d1["key1"]["msg"])



# Example-9 (Assignment)
# d1 = {
#     "d2":{
#         "d3":{
#             "nums" : {
#                 "x" : 200,
#                 "y" : 100
#             }
#         }
#     }
# }


# Example-10
# outer = {
#     "101" : {
#         "name" : "std1",
#         "marks" : 90
#     },
#     "102":{
#         "name" : "std2",
#         "marks" : 80
#     }
# }

# for x in outer.values():
#     for key,value in x.items():
#         print(key,value,sep=" | ")


# Example-11 (dictionary comprehension)
# print( {x:x*x for x in range(1,6)} )                       # x = 1,2,3,4,5


# Example-12
# hello - h:1, e:1, l:2, o:1
# str = "hello"
# count = {}
# for ch in str:
#     count[ch] = count.get(ch,0) + 1

# print(count)


# Example-13
# d1 = {
#     "name" : "std1"
# }
# d2 = {
#     "marks" : 90
# }
# d1.update(d2)
# print(d1)

# Example-14
# d1 = {
#     "key1":200,
#     "key2":100
# }
# print("key1" in d1)
# print("key3" not in d1)

# Example-15
# d1 = {
#     "key1" : 10,
#     "key2" :20
# }
# d2 = {
#     "key1" : 100,
#     "key3" :300
# }
# res = d1.keys() & d2.keys()
# print(res)


# Print Non Common Keys (Assignment)

# Example-16
# d1 = {
#     "Anil" :90,
#     "Venkat" : 80,
#     "Charan" : 85
# }
# d1 = dict( sorted(d1.items()) )
# print(d1)

# d1 = dict(sorted(d1.items(), key=lambda item:item[1]))
# print(d1)

