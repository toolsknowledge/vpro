# dictionary - key & value pairs, keys are immutable, values are mutable, {} / dict()

# Example-18 (find common keys)
# d1 = {
#     "A" : 10,
#     "B" : 20
# }
# d2 = {
#     "B" : 40,
#     "C" : 50
# }
# common = d1.keys() & d2.keys()
# print(common)

# Example-17 (Remove Duplicate Values)
# d1 = {
#     "A" : 10,
#     "B" : 20,
#     "C" : 10,
#     "D" : 30,
#     "E" : 20
# }
# result = {}

# for key,value in d1.items():
#     if value not in result.values():
#         result[key] = value

# print(result)


# Example-16 (Invert)
# d1 = {
#     "101" : "Hello",                
#     "102" : "Agentic AI"
# }
# d2 = {value:key for key,value in d1.items()}
# print(d2)



# Example-15 (sum of values)
# d1 = {
#     "key1" : 1,
#     "key2" : 2,
#     "key3" : 3    
# }
# res = sum(d1.values())
# print(res)



# Example-14 (Sorting) (1) key (2) value
# d1 = {
#     "Rahul" : 88,
#     "Samba" : 95,
#     "Anil" : 91
# }

# d2 = dict(sorted(d1.items()))
# print(d2)

# d3 = dict(sorted(d1.items(),key=lambda item:item[1]))
# print(d3)


# Example-13 (find highest value)
# d1 = {
#     "std1" : 50,
#     "std2" : 60,
#     "std3" : 70,
#     "std4" : 80
# }
# top_student = max(d1,key=d1.get)
# print(top_student)
# print(d1[top_student])



# Example-12 (check key present / not)
# d1 = {
#     "id" : 101,
#     "name" : "VPro",
#     "version" : 2.0
# }
# if "name" in d1:
#     print("Existed")
# else:
#     print("Not Existed")



# Example-11
# d1 = {
#     "id" : 101
# }
# d2 = {
#     "name" : "VPro"
# }
# d1.update(d2)
# print(d1)


# Example-10
# statement = "python java python java python"
# words = statement.split()
# count = {}
# for word in words:
#     count[word] = count.get(word,0) + 1

# print(count)

# Example-9
# msg = "hello"
# count = {} # {"h":1,"e":1,"l":2,"o":1}
# for ch in msg:
#     count[ch] = count.get(ch,0) + 1

# print(count)



# Example-8
# d1 = {x:x*x for x in range(1,6)}
# print(d1)



# Example-7
# d1 = {
#     101 : {
#         "key1" : 100
#     },
#     102 : {
#         "key1" : 200
#     }
# }
# print( d1.get(101).get("key1") )
# print( d1[102]["key1"] )
# for inner_d1 in d1.values():
#     print(inner_d1.get("key1"))




# Example-6
# d1 = {
#     "key1" : 100,
#     "key2" : 200,
#     "key3" : 300
# }
# for key in d1:
#     print(key)

# for value in d1.values():
#     print(value)

# for key,value in d1.items():
#     print(key,value)



# Example-5
# d1 = {}
# d1["key1"] = 100
# d1["key2"] = 200
# d1["key1"] = 1000
# d1["key3"] = 300

# print(d1["key1"],d1.get("key1"))
# print(d1["key4"])
# print(d1.get("key4"))
# print(d1.get("key4",0))
# del d1["key3"]
# del d1["key4"]
# d1.pop("key2")
# print(d1)



# Example-4
# d1 = {
#     "id":101,
#     "name":101,
# }
# print(d1)


# Example-3
# d1 = {
#     "name" : "Test1",
#     "name" : 123
# }
# print(d1)


# Example-2
# d1 = dict({"id":1,"name":"test"})
# print(d1)
# print(type(d1))


# Example-1
# d1 = {
#     "id":101,
#     "name":"AgenticAI",
#     "version":2.0
# }
# print(d1)
# print(d1.keys())
# print(d1.values())
# print(d1.items())