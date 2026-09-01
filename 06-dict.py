"""
    dictionary
        store data in "key & value" pairs
        key and value separated by using ":"
        keys are "immutable"
        values are "mutable"
        we will represent with the help of {} / dict() constructor
""" 

# d1 = {}
# print(d1)
# print(type(d1))

# d1 = {
#     "name":"Emp1",
#     "dept":"R&D",
#     "salary":10000,
#     "id":101
# }
# print(d1)
# print(d1["name"])
# print(d1["Address"])
# print(d1.get("Address"))
# print(d1.get("Address","Hyderabad"))
# print(d1.keys())
# print(d1.values())
# print(d1.items())

# d1 = {}
# d1["key1"] = "GenAI"
# d1["key2"] = "AgenticAI"
# d1["key1"] = "Generative AI"
# del d1["key1"]
# print(d1)


# d1 = {
#     "key1" : "Hello",
#     "key2" : "FDE",
#     "key3" : "QC"
# }
# for key in d1.keys():
#     print(key,end=" ")

# print("\n")

# for value in d1.values():
#     print(value,end=" ")

# print("\n")

# for key,value in d1.items():
#     print(key,value,sep="--->")

# d1 = {
#     "key1" : "Hello",
#     "key2" : "FDE",
#     "key3" : "QC"
# }
# print("key1" in d1)
# print("key4" in d1)
# d1.pop("key3")
# d1.popitem()
# print(d1)

# d1 = {
#     "d2": {
#         "wish":"Hello"
#     }
# }

# print(d1["d2"]["wish"])
# for inner in d1.values():
#     for value in inner.values():
#         print(value)


# str = "Hello"
# count = {}
# for ch in str:
#     count[ch] = count.get(ch,0)+1       # {"H":1,"e":1,"l":2,"o":1}      

# print(count)

# str = "java python java ml java python"
# words = str.split(" ")
# print(words)

# d1 = {
#     "key1" : 100
# }
# d2 = {
#     "key2" : 200
# }
# d3 = {
#     "key3" : 300
# }
# d1.update(d2)
# d1.update(d3)
# print(d1)


# print( {x:x**x for x in range(1,6) } )


# d1 = {
#     "std1":80,
#     "std2":90,
#     "std3":75
# }
# x = max(d1,key=d1.get)
# print(x,d1.get(x))


# d1 = {
#     "John":80,
#     "Anil":90,
#     "Venkat":75
# }

# res = dict( sorted(d1.items()) )
# print(res)

# res = dict( sorted( d1.items(), key=lambda item:item[1] ) )
# print(res)

# expenses = {
#     "Rent":50000,
#     "Travel" : 10000,
#     "Food" : 20000
# }
# print( sum(expenses.values()) )

# d1 = {
#     "key1":100,
#     "key2":200
# }

# d2 = {value:key for key,value in d1.items()}
# print(d2)


# d1 = {
#     "key1" : 100,
#     "key1" : 1000
# }
# print(d1)

# d1 = {
#     "A":10,
#     "B":20,
#     "C":10,
#     "D":20,
#     "E":30
# }
# result = {}
# for key,value in d1.items():
#     if value not in result.values():
#         result[key] = value

# print(result)


# list1 = [{"num1":10},
#          {"num1":20},
#          {"num1":30}]
# print(list1[0]["num1"] + list1[1]["num1"] + list1[2]["num1"])
# res = 0
# for d1 in list1:
#     for x in d1.values():
#         res += x
# print(res)

# d1 = {"a":10, "b":20, "c":10}
# print( { value:key for key,value in d1.items() } )














