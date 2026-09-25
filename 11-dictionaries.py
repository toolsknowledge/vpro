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
