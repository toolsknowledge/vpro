# Loops - iterate the collections (Lists,Tuples)

# Example-1
# nums = [10,20,30,40,50]
# for num in nums:
#     print(num,end=" ")

# Example-2
# for num in range(5):
#     print(num)

# for num in range(2,7):
#     print(num)

# for num in range(2,10,2):   #2 4 6 8
#     print(num)

# for num in range(10,0,-2):  #10 8 6 4 2
#     print(num)


# Example-3
# nums = [100,200,300,400,500]
# for index,value in enumerate(nums):
#     print(index,value,sep="➜")

# for index,value in enumerate(nums,start=1):
#     print(index,value,sep="➜")

# Example-4
# stds = ["Std1","Std2","Std3","Std4","Std5"]
# marks = [60,70,80,90,100]
# for std,mark in zip(stds,marks):
#     print(std,"--->",mark)

# Example-5
# msg = "Hello"
# for ch in msg:
#     print(ch,end="")



# Example-6
# msg = "Hello"
# reverse = ""    # olleH       
# for ch in msg:
#     reverse = ch + reverse      

# print(reverse)

# Example-7 (find the largest number)
# nums = [25,78,45,100,32]
# largest = nums[0]   # 100
# for num in nums:
#     if num > largest:
#         largest = num
# print(largest)

# Example-8 (total even numbers)
# nums = [1,2,3,4,5,6]
# count = 0  
# for num in nums:
#     if num%2 == 0:
#         count = count+1  

# print(count)


# Example-9
# for i in range(5):
#     if i==3:
#         # break
#         # continue
#         pass
    
#     print(i,end=" ")

# break - 0 1 2
# continue - 0 1 2 4
# pass - 0 1 2 3 4


# Example-10 (display the duplicates)
# list1 = [1,1,2,3,2,2,3,1,4]     # list1.count(1) = 3
# duplicates = set()
# for element in list1:
#     if list1.count(element)>1:  # 3 > 1
#         duplicates.add(element)
# print(duplicates)

# Example-11 (Fibonacci Series)
# a,b = 0,1
# for _ in range(10):
#     print(a,end=" ")
#     a,b = b, a+b


# Example-13 (Nested Loop)
# for i in range(3):      # i=1
#     for j in range(3):  # j=0
#         print(i,"--->",j)

# Example-14
# for i in range(1,6):
#     for j in range(1,11):
#         print(i,"x",j,"=",i*j)
#     print("-------------")

# Example-15
# for i in range(5):
#     print(i)
# else:
#     print("Done !!!") 

# Example-16
# i=1 # Initilization
# while i<=5: # condition
#     print(i)
#     i = i+1 # increment

# Example-17
# i = 5
# while i > 0:
#     print(i)
#     i = i-1

# Example - 18 (Infinite Loop)
# name = ""
# while True:
#     name = input("enter your choice ?")
#     print(name)

#     if name == "q":
#         break
















    







