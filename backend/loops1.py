# Example-1
# nums = [1,2,3,4,5]
# for x in nums:
#     print(x)



# Example-2
# for num1 in range(5):        # 0 - included and 5 - excluded
#     print(num1)

# for num2 in range(2,5):       # 2 included and 5 excluded
#     print(num2)

# for num3 in range(0,10,2):      # 0, 2, 4, 6, 8
#     print(num3)

# for num4 in range(10,0,-2):     # 10. 8. 6.  4.  2  
#     print(num4)


# Example-3
# nums = [10,20,30,40,50]
# for a,b in enumerate(nums):
#     print(f"Index {a} | element : {b}")


# Example-4
# t1 = 10,20,30
# t2 = 100,200,300
# for element1,element2 in zip(t1,t2):
#     print(element1,element2)



# Example-5
# nums = [10,8,6,25,32,15]
# largest = nums[0]           # 32
# for num in nums:
#     if num > largest:
#         largest = num       # largest = 32      

# print(largest)

# Assignments
# find the 1st max
# find the 2nd max
# find the 2nd min
# find the 1st min


# Example-6 (even numbers count)
# nums = [1,2,3,4,5]
# count = 0
# for num in nums:
#     if num % 2 == 0:
#         count += 1

# print(count)

# find the count of odd numbers


# list the duplicates
# nums = [1,2,3,2,4,5,3]
# duplicates = set()

# for num in nums:
#     if nums.count(num) > 1:
#         duplicates.add(num)

# print(duplicates)


# str = "Python"
# result = ""
# for ch in str:
#     result = ch + result

# print(result)


for i in range(1,6):        # 1 - included and 6 - excluded
    if i == 3:
        # break
        continue
    print(i)                # 1 2
                            # 1 2 4 5




