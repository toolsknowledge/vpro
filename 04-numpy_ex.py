import numpy as np

# Faq15
# arr1 = np.arange(1,10)
# arr2 = arr1.reshape(3,3)
# arr1[0] = 100
# arr2[2][2] = 900
# print(arr1)


# Faq14
# count even numbers
# arr1 = np.array([10,15,20,25,30,35])
# x = np.count_nonzero(arr1 % 2 == 0)
# print(x)


# Faq13
# Normalization
# marks = np.array([50,60,70,80,90])
# normalization = (marks - marks.min()) / (marks.max()-marks.min())
# print(normalization)


# Faq12
# dot product
# arr1 = np.array([1,2,3])
# arr2 = np.array([4,5,6])
# res = np.dot(arr1,arr2)
# print(res) # (1*4) + (2*5) + (3*6)


# Faq11
# display diagnoal values
# arr1 = np.array([[1,2,3],
#                  [4,5,6],
#                  [7,8,9]])
# arr2 = np.diag(arr1)
# print(arr2)


# Faq10
# Identity Matrix
# arr1 = np.identity(4)
# print(arr1)


# Faq9
# Stack Arrays Horizontally
# arr1 = np.array([[1],[2],[3]])
# arr2 = np.array([[4],[5],[6]])
# arr3 = np.hstack((arr1,arr2))
# print(arr3)




# Faq8
# Stack Arrays Vertically
# arr1 = np.array([1,2,3])
# arr2 = np.array([4,5,6])
# arr3 = np.vstack((arr1,arr2))
# print(arr3)



# Faq7
# Split an array
# arr1 = np.arange(12)
# parts = np.split(arr1,3)
# print(parts)


# Faq6
# Concat Arrays
# arr1 = np.array([1,2,3])
# arr2 = np.array([4,5,6])
# new_arr = np.concatenate((arr1,arr2))
# print(new_arr)



# Faq5
# find top 3 elements
# arr1 = np.array([10,50,20,40,30])
# top = np.sort(arr1)[-3:]    #[10,20,30,40,50]
# print(top)



# Faq4
# Reverse an array
# arr1 = np.array([10,20,30,40,50])
# new_arr = arr1[::-1]
# print(new_arr)




# Faq3
# Find the duplicates
# arr1 = np.array([10,20,30,10,20,30,40])
# uniques,counts = np.unique(arr1,return_counts=True)
# print(uniques)
# print(counts)


# Faq2
# replace negative values with 0
# profits = np.array([100,-50,30,-10,1000,-90])
# new_arr = np.where(profits < 0,0,profits)
# print(new_arr)


# Faq1
# Find Salaries >50000
# salaries = np.array([10000,30000,20000,50000,90000,15000])
# high_salaries = salaries[salaries > 50000]
# print(high_salaries)


# Example-17
# arr1 = np.array([10,50,20,40,30])
# print(arr1.argmax())
# print(arr1.argmin())


# Example-16
# arr1 = np.array([1,2,3])
# # arr2 = arr1
# arr2 = arr1.copy()
# arr1[0] = 100
# print(arr2)


# Example-15
# np.random.seed(10)
# arr1 = np.random.randint(1,100,10)
# print(arr1)


# Example - 14
# arr1 = np.array([10,50,20,40,30])
# arr2 = np.sort(arr1)
# print(arr2)

# Example - 13
# marks = np.array([55,65,75,85,95])
# result = np.where(marks>60,"pass","fail")
# print(result)

# Exampl-12
# marks = np.array([55,65,75,85,95])
# print(marks.sum())
# print(marks.max())
# print(marks.min())
# print(marks.mean())
# arr1 = np.array([[1,2],
#                  [3,4]])
# print(arr1.sum(axis=0)) # col-sum
# print(arr1.sum(axis=1)) # row-sum

# Example-11 (Multiplication)
# arr1 = np.array([[1,2],
#                  [3,4]])
# arr2 = np.array([[5,6],
#                  [7,8]])

# arr3 = np.matmul(arr1,arr2)
# print(arr3)


# Example-10 (Matrix Addition)
# arr1 = np.array([1,2,3])
# arr2 = np.array([4,5,6])
# arr3 = arr1 + arr2
# print(arr3)

# arr4 = np.array([[1,2],
#                  [3,4]])
# arr5 = np.array([[5,6],
#                  [7,8]])
# arr6 = arr4 + arr5
# print(arr6)


# Example-9 (Broadcasting)
# salary = np.array([10000,20000,30000,40000,50000])
# new_salaries = salary + 5000
# print(new_salaries)




# Example-8 (Fancy Indexing)
# marks = np.array([55,65,75,85,95])
# print(marks[0])
# print(marks[[0,2,4]])


# Example-7
# arr1 = np.array([25000,50000,75000,100000])
# arr2 = arr1[arr1>50000]
# print(arr2)

# Example-6 (2D - 1D)
# arr1 = np.array([[1,2],[3,4]])
# arr2 = arr1.flatten()
# print(arr2)


# Example-5
# arr1 = np.arange(1,13)
# arr2 = arr1.reshape(3,4)
# print(arr2)

# Example-4
# arr1 = np.linspace(0,1,4)
# print(arr1)

# Example-3
# arr1 = np.arange(10,21)
# print(arr1)

# arr2 = np.arange(10,21,2)
# print(arr2)


# Example-2
# arr1 = np.zeros((3,4))
# print(arr1)
# arr2 = np.ones((2,5))
# print(arr2)


# Example-1
# arr1 = np.array([10,20,30,40,50])
# print(arr1)
# print(arr1.ndim)
# print(arr1.shape)
# print(arr1.size)
# print(arr1.dtype)

# arr2 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])
# print(arr2)
