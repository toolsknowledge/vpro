"""
    dictionaries
    ************
        store the data in the form of a key and value pairs
        we will represent dictionaries with the help of either {} / dict()
        keys are immutable
        values are mutable
"""
# Example-1
# d1 = {
#     "num1" : 200,
#     "num2" : 100
# }
# print(d1.keys())        # tuple(list)
# print(d1.values())      # tuple
# print(d1.items())       # tuple


# Example-2
# d1 = {
#     "num1" : 200,
#     "num2" : 100
# }
# print(d1["num1"])
# print(d1["num2"])
# # print(d1["num3"])
# print(d1.get("num3",0))

# Example-3
# d1 = {}
# print(d1)

# d1["num1"] = 200
# d1["num2"] = 100
# d1["num3"] = 300
# print(d1)

# d1["num1"] = 2000
# d1["num2"] = 1000
# print(d1)


# d1.pop("num3")
# print(d1)

# d1.popitem()
# print(d1)

# del d1["num1"]
# print(d1)



# Example-4
# d1 = {
#     "key1" : 200,
#     "key1" : 100,
#     "key2" : 300
# }
# print(d1)

# Example-5
# d1 = {
#     "num1" : 200,
#     "num2" : 200
# }
# print(d1)


# Example-6
# d1 = {
#     "num1" : 200,
#     "num2" : 100,
#     "num3" : 50
# }
# for key in d1.keys():
#     print(key)
# for value in d1.values():
#     print(value)
# for key,value in d1.items():
#     print(key,value)


# Example-7
# d1 = {
#     "101" : {"name":"std1","marks":90},
#     "102" : {"name":"std2","marks":80}
# }
# print(d1["101"]["marks"])
# print(d1["102"]["name"])

# for inner in d1.values():
#     for value in inner.values():
#         print(value)


# Example-8 (dict compression)
# res = {x:x*x for x in range(1,6)}              # 1,2,3,4,5
# print(res)                                     # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}


# Example-8
# d1 = {"num1":0,"num2":1}        # {"0":"num1","1":"num2"}
# d1 = {value:key for key,value in d1.items()}
# print(d1)


# Example-9
# text = "hello"
# count = {}
# for ch in text:
#     count[ch] = count.get(ch,0) + 1
# print(count)


# Example-10
# d1 = {
#     "name" : "std1"
# }
# d2 = {
#     "marks" : 90
# }
# d1.update(d2)
# print(d1)


# Example-11
# d1 = {
#     "num1" : 300,
#     "num2" : 200,
#     "num3" : 100
# }
# print("num2" in d1)
# print("num4" in d1)


# Example-12
# d1 = {
#     "Anil" : 90,
#     "Venkat": 80,
#     "Charan" : 85
# }
# d1 = dict( sorted(d1.items()) )
# print(d1)

# d1 = dict( sorted(d1.items(),key=lambda item:item[1]) )
# print(d1)


# Example-13
# d1 = {
#     "key1" : 10,
#     "key2" : 20
# }
# d2 = {
#     "key1" : 100,
#     "key3" : 300
# }
# res = d1.keys() & d2.keys()
# print(res)