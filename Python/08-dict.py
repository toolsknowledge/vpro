# dictionary - represent data in the form of a key value pairs
# keys are immutable and values are mutable
# dictionary also supports hashtable (searching is fast)
# dynamic size
# {} / dict() constructor

# Example-1
# d1 = {
#     "key1" : "Hello",
#     "key2" : "welcome",
#     "key3" : "AgenticAI"
# }
# print(d1)
# d2 = dict(key1="Hello", key2="Welcome")
# print(d2)
# d3 = dict([("key1","Hello"),("key2","welcome")])
# print(d3)

# Example-2
# d1 = {
#     "key1" : "GenAI",
#     "key2" : "AgenticAI"
# }
# print(d1.keys())
# print(d1.values())
# print(d1.items())

# Example-3
# d1 = {
#     "key1" : "GenAI",
#     "key2" : "AgenticAI"
# }
# for key in d1.keys():
#     print(key)

# for values in d1.values():
#     print(values)

# for key,value in d1.items():
#     print(f"key is {key} and value is {value}")


# Example - 4
# outer = {
#     "name" : "VPro",
#     "address" : {
#         "location" : "SRNagar",
#         "city" : "Hyderabad",
#         "pin" : 500038
#     }
# }
# print(outer["address"]["location"],outer["address"]["city"],outer["address"]["pin"])

# Example - 5
# d1 = {}
# d1["key1"] = 100
# d1["key2"] = 200
# d1["key3"] = 300
# print(d1)

# d1["key1"] = 1000
# print(d1)

# print(d1["key1"])
# print(d1["key4"])   # Err
# print(d1.get("key4"))
# print(d1.get("key4",10000))

# d1.pop("key3")
# print(d1)

# d1.popitem()
# print(d1)

# d1.clear()
# print(d1)

# Example-6
# d1 = {
#     "key1" : 100,
#     "key1" : 200,
#     "key2" : 100
# }
# print(d1)


# Example-7 (Shallow Copy)
# d1 = {
#     "key1" : [10,20]
# }
# d2 = d1.copy()
# d2["key1"].append(30)
# print(d1)

# Example-8 (deep Copy)
# import copy
# d1 = {
#     "key1" : [10,20]
# }
# d2 = copy.deepcopy(d1)
# d2["key1"].append(30)
# print(d1)

# Example-9
# keys must be hashable
# d1 = {
#     (1,2) : [1,2]
# }

# Example-10
# d1 = {x:x*x for x in range(5)}
# print(d1)

# Example-11
d1 = {}
d1[True] = 100
d1[1] = 1000
print(d1)

d2 = {}
d2[1] = 100
d2[1.0] = 1000
print(d2)

d3 = {
    "key1" : 100,
    "key2" : 200
 }
print("key1" in d3)
print("key3" not in d3)
print("key2" not in d3)
