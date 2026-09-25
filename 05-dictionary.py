"""
    dictionaries
    ************
        key and value pairs
        {} / dict()
        keys - immutable
        values - mutable
"""
# d1 = {
#     "num1" : 200,
#     "num2" : 100
# }
# print(d1.keys())
# print(d1.values())
# print(d1.items())


# d1 = {
#     "num1" : 200,
#     "num2" : 100
# }
# print(d1["num1"])
# print(d1["num2"])
# # print(d1["num3"])
# print(d1.get("num3",0))

# d1 = {
#     "key1" : "ML",
#     "key2" : "DL",
#     "key3" : "NLP"
# }
# # for key in d1.keys():
# #     print(key)

# # for value in d1.values():
# #     print(value)

# for key,value in d1.items():
#     print(key,value,sep="--->")


d1 = {}
print(type(d1))

# adding data dynamically
d1["num1"] = 200
d1["num2"] = 100
d1["num3"] = 300
print(d1)

# updating the dictionary data
d1["num1"] = 2000
print(d1)

# deleting the data (by key)
d1.pop("num3")
print(d1)

d1.pop("num2")
print(d1)

# deleting last key
d1.popitem()
print(d1)


# basics(1hr)  llm(1hr)