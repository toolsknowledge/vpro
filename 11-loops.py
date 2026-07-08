# nums = [1,2,3,4,5]
# for num in nums:
#     print(num)

# for num in range(5):          # "0-included" and "5-excluded"
#     print(num)

# for num in range(2,7):
#     print(num)

# for num in range(0,10,2):
#     print(num)

# for num in range(10,0,-2):
#     print(num)

# for num in range(5,0,-1):
#     print(num)


# nums = [10,20,30,40,50]
# for index,element in enumerate(nums):
#     print(f"index is {index} and value is {element}")


# nums = [100,200,300,400,500]
# for index,element in enumerate(nums,start=1):
#     print(f"index is {index} and value is {element}")


# stds = ["Std1","Std2","Std3","Std4","Std5"]
# marks = [50,60,70,80,90]
# for std,mark in zip(stds,marks):
#     print(f"{std} got {mark} marks")


# nums = [10,8,6,25,32,15]
# largest = nums[0] # 32
# for num in nums:
#     if num > largest:
#         largest = num

# print(largest)

# find min number
# find 2nd largest
# find 2nd min number

# nums = [1,2,3,4,5]
# count = 0
# for num in nums:
#     if num%2 == 0:
#         count += 1

# print(count)

# find the number of odd numbers


# nums = [1,2,3,2,4,5,3]  # nums.count(1) 1 nums.count(2) 2 nums.count(3) 2
# duplicates = set()

# for num in nums:
#     if nums.count(num)>1:
#         duplicates.add(num)

# print(duplicates)

# str = "Python"
# for ch in str:
#     print(ch,end=" ")

# str = "Python"
# result=""   #nohtyP
# for ch in str:
#     result = ch + result
# print(result)

# a,b = 0,1
# for _ in range(10):
#     print(a,end=" ")
#     a,b = b,a+b


# str = "hello" # h-1 e-1 l-2 o-1

# for i in range(5):
#     print(i)
# else:
#     print("done !!!")

# for i in range(1,6):
#     if i == 3:
        #break Ex. 1 2
        #continue Ex. 1 2 4 5
    #     pass # Ex. 1 2 3 4 5
    # print(i)


# for i in range(3):
#     for j in range(3):
#         print(i,j,sep="➟")


# i=1
# while i<=5:
#     print(i)
#     i += 1
# else:
#     print("while loop done")


# while True:
#     name = input("Enter Name: ")

#     if name=="quit":
#         break

#     print(name)

