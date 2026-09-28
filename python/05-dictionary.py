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


# d1 = {}
# print(type(d1))

# # adding data dynamically
# d1["num1"] = 200
# d1["num2"] = 100
# d1["num3"] = 300
# print(d1)

# # updating the dictionary data
# d1["num1"] = 2000
# print(d1)

# # deleting the data (by key)
# d1.pop("num3")
# print(d1)

# d1.pop("num2")
# print(d1)

# # deleting last key
# d1.popitem()
# print(d1)




# d1 = {
#     "key1" : 100,
#     "key1" : 1000
# }
# print(d1)
# {'key1': 1000}
# Note : python wont allows duplicate keys
# overriding will happen

# d1 = {
#     "key1" : 100,
#     "key2" : 100
# }
# print(d1)


# d1 = {
#     101 : {
#         "name" : "Std1",
#         "marks" : 90
#     },
#     102 : {
#         "name" : "Std2",
#         "marks" : 80
#     }
# }
# print(d1[101]["marks"])
# print(d1[102]["name"])


# d1 = {
#     "num1" : 100
# }
# d2 = {
#     "num2" : 200
# }
# d1.update(d2)
# print(d1)

# str = "Hello"       # H - 1.  e - 1.  l - 2. o - 1
# count = {}
# for ch in str:
#     count[ch] = count.get(ch,0) + 1
# print(count)


# d1 = {
#     "key1" : 100,
#     "key2" : 100
# }
# if "key1" in d1:
#     print("Exist !!!")
# else:
#     print("Not Exist !!!")

# if "key3" not in d1:
#     print("Not Exist !!!")
# else:
#     print("Exist !!!")



# d1 = {
#     "Charan" : 90,
#     "Anil" : 95,
#     "Balu" : 70
# }
# # res = dict(sorted(d1.items()))
# # print(res)
# res = dict(sorted(d1.items(),key=lambda item:item[1]))
# print(res)


# d1 = {
#     "key1" : 1,
#     "key2" : 2,
#     "key3" : 3
# }
# res = {key:value**value for key,value in d1.items()}
# print(res)


# d1 = {
#     "101":"Charan",
#     "102":"Anil",
#     "103":"Balu"
# }
# res = {value:key for key,value in d1.items()}
# print(res)

# remove duplicate values 
# data = {
#     "A":10,
#     "B":20,
#     "C":10,
#     "D":30,
#     "E":20
# }

# result = {}
# for key,value in data.items():
#     if value not in result.values():
#         result[key] = value

# print(result)


# d1 = {
#     "A":10,
#     "B":20,
#     "C":30
# }

# d2 = {
#     "A":40,
#     "D":30
# }

# common = d1.keys() & d2.keys()
# print(common)















