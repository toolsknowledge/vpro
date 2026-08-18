# numpy - numerical python
# numpy performs "speed list operations"
# numpy "c based" implementation
# memory efficient
# broadcasting & vectorization
# 1) python -m venv venv           
# 2) source venv/bin/activate (mac book) venv\Scripts\activate(windows)
# 3) requirements.txt (numpy)
# 4) pip install -r requirements.txt
# import numpy as np

# Example-1
# import numpy as np
# arr1 = np.array([1,2,3,4,5])
# print(arr1)
# print(arr1.shape)
# print(arr1.ndim)

# arr2 = np.array([[1,2],[3,4],[5,6]])
# print(arr2)
# print(arr2.shape)
# print(arr2.ndim)

# Example-2
# import numpy as np
# print( np.zeros((3,3)) )
# print( np.ones((3,3)) )
# print( np.eye(3) * 3 )
# print( np.arange(0,10,2) )  # [0,2,4,6,8]
# print( np.linspace(0,1,5) ) # [0.   0.25 0.5  0.75 1.  ]
# print( np.full(5,5))
# print( np.ones(5) * 5 )

# Example-3 (Vectorization)
# import numpy as np
# arr1 = np.array([1,2,3])
# arr2 = np.array([10,11,12])
# print(arr1 + arr2)
# print(arr2 - arr1)

# Example-4 (Broadcasting)
# import numpy as np
# arr1 = np.array([1,2,3])
# print(arr1 + 10)

# Example-5
# import numpy as np
# arr1 = np.array([10,20,30,40,50,60])
# arr2 = arr1.reshape(2,3)
# print(arr2)
# arr3 = arr2.flatten()
# print(arr3)

# Example-6
# import numpy as np
# print( np.random.rand(3) )
# print( np.random.randint(1,10,6).reshape(2,3) )

# Example-7
# import numpy as np
# arr1 = np.array([1,4,9])
# print(np.sqrt(arr1))
# print(np.sum(arr1))
# print(np.mean(arr1))

# arr2 = np.array([[1,2],[3,4]])
# print(np.linalg.det(arr2))
# print(np.linalg.inv(arr2))
# print(np.linalg.matrix_transpose(arr2))


# Example - 8
# import numpy as np
# marks = np.array([78,85,90,66,72])
# print(f"Max Marks : {np.max(marks)}")
# print(f"Min Marks : {np.min(marks)}")
# print(f"Average Marks {np.mean(marks)}")

# Examples - 9
# import numpy as np
# sales = np.array([[200,300,400],
#                   [250,350,450]])
# print(np.sum(sales,axis=1))
# print(np.sum(sales,axis=0))

# Example-10
# print( [["VPro"] * 5 for _ in range(3)]  )

# Example-11
# import numpy as np
# arr1 = np.array([[1,2,3],
#                  [4,5,6]])
# print(arr1 + 10)
# print(arr1[0][0]) # 0th row and 0th col
# print(arr1[0,1])  # 0th row and 1st col
# print(arr1[1,2])  # 1st row and 2nd col
# print(arr1[:1])   # 0th index included and 1st index excluded
# print(arr1[:0+1])# 0th index included and 1st index excluded
# print(arr1[1:2])  # 1th index included and 2st index excluded

# print(arr1[:,1])
# print(arr1[:,2])
# print(arr1[:,0])
# print(arr1[:,0:2])
# print(arr1[0:2 :, 0:1])


# Example-13
# import numpy as np
# arr1 = np.array([10,20,30,40,50])
# arr2 = np.array([100,200,300,400,500])
# for element in arr1:
#     print(f"Elements are : {element}")

# for index,element in enumerate(arr1):
#     print(index,element)

# for ele1,ele2 in zip(arr1,arr2):
#     print(ele1,ele2)


# arr1 = np.array([[1,2,3],
#                  [4,5,6],
#                  [7,8,9]])
# for inner in arr1:
#     for index,element in enumerate(inner):
#         print(index,element,sep="--->",end="\n--------------")


# Example-14
# import numpy as np
# arr1 = np.array([1,2,3])
# arr2 = arr1
# arr2 = np.append(arr2,4)
# print(arr2)
# print(arr1)

# Example-15
import numpy as np
import sys
arr1 = [10,20,30,40,50]
arr2 = np.array([10,20,30,40,50])
print(sys.getsizeof(arr1))
print(sys.getsizeof(arr2))
