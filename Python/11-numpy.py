# Example - 1
# import numpy as np
# print(np.__version__)


# Example - 2
# import numpy as np
# arr1 = np.array([100,200,300])      # 1D
# arr2 = np.array([[100,200],         # 2D
#                  [300,400],
#                  [500,600]])
# arr3 = np.array([[[1,2,3]]])        # 3D
# print(arr2.shape)
# print(arr2.dtype)
# print(arr2.ndim)

# Example - 3
# import numpy as np
# arr1 = np.zeros((2,3))
# print(arr1)

# arr2 = np.ones((3,3))
# print(arr2)

# arr3 = np.eye(3)
# print(arr3)

# arr4 = np.arange(0,10,1)
# print(arr4)

# arr5 = np.arange(0,10,2)
# print(arr5)

# arr6 = np.linspace(0,1,4)
# print(arr6)

# arr7 = np.array([1,2,3,4,5],dtype=int)
# print(arr7)

# arr8 = np.full(5,3)
# print(arr8)

# arr9 = np.full((2,2),5)
# print(arr9)


# Example - 4
# import numpy as np
# arr1 = np.array([10,20,30,40,50])
# print(arr1[0],arr1[-5])
# print(arr1[0:3])
# print(arr1[:2])
# print(arr1[2:])
# print(arr1[:0+1])
# print(arr1[-3:-1])
# print(arr1[::-1])
# print(arr1[::-2])
# print(arr1[::-3])

# arr2 = np.array([[10,20],
#                  [30,40]])
# print(arr2[0][0],arr2[0][1], arr2[1][3])


# Example - 5
# import numpy as np
# arr1 = np.array([10,20,30,40,50])

# for element in arr1:
#     print(element,end=" | ")

# for index,element in enumerate(arr1):
#     print(index,element,sep="--->")


# arr2 = np.array([[10,20,30],
#                  [40,50,60]])
# for inner_list in arr2:
#     for index,element in enumerate(inner_list):
#         print(index,element,sep="---->")
#     print("----------------------------------")


# Example - 6
# import numpy as np
# arr1 = np.array([1,2])
# arr2 = np.array([3,4])
# arr3 = arr1 + arr2
# print(arr3)

# arr4 = arr2 - arr1
# print(arr4)

# arr5 = arr1 * arr2
# print(arr5)


# Example - 7
# import numpy as np
# arr1 = np.array([10,20,30])
# num = 2
# print(arr1 + num)

# arr2 = np.array([[10,20,30],
#                  [40,50,60]])
# x = 10
# print(arr2 + x)


# Example - 8
# import numpy as np
# arr1 = np.array([1,2,3,4,5,6])
# arr2 = arr1.reshape(2,3)
# arr3 = arr2.flatten()
# print(arr3)

# Example - 9
# import numpy as np
# arr1 = np.array([[1,2],
#                  [3,4]])

# print( np.linalg.inv(arr1) )                
# print( np.linalg.det(arr1) )                # ad - bc
# print( np.linalg.matrix_transpose(arr1) )


# Example - 10
# import numpy as np
# print( np.random.rand(3) )
# print( np.random.randint(1,10,6).reshape(2,3) )

# Example - 11
# import numpy as np
# marks = np.array([60,65,70,75,80,85,90])
# print(f"Average Marks : {np.mean(marks)}")
# print(f"Max Marks : {np.max(marks)}")
# print(f"Min Marks : {np.min(marks)}")


# Example - 12
# import numpy as np
# sales = np.array([[200,300,250],
#                   [400,500,450]])
# print(np.sum(sales,axis=1)) # row wise sum
# print(np.sum(sales,axis=0)) # column wise sum


# Example - 13
# import numpy as np
# arr1 = np.array([100,200,300])
# arr2 = arr1  # (Shallow Copy)
# arr2[0] = 1000
# print(arr1)

# Example - 14
# import numpy as np
# arr1 = np.array([1,2,3])
# arr2 = np.array([4,5,6])
# print(np.add(arr1,arr2))
# print(np.subtract(arr1,arr2))
# print(np.multiply(arr1,arr2))
# print(np.divide(arr2,arr1))

# print(np.power(arr1,2))
# print(np.mod([10,20,30],3))
# print(np.remainder([10,20,30],3))

# Example - 15
# import numpy as np
# arr1 = np.array([1,2])
# arr2 = np.array([1,2])
# print(np.equal(arr1,arr2))

# x = np.array([4,2])
# y = np.array([3,5])
# print(np.greater(x,y))
# print(np.less(x,y))

# Example - 16
import numpy as np
# arr1 = np.array([10,50,20,40,30])
# arr2 = np.sort(arr1)
# print(arr2)
# print(arr2[::-1])

# arr1 = np.array([10,50,20,40,30])   # [0, 1, 2 , 3 , 4]
# print(np.argsort(arr1)) # [0 2 4 3 1]

# arr1 = np.array([10,50,20,40,30])
# i = np.where(arr1>20)
# print(type(i))
# for element in i:
#     print(arr1[element])

# arr1 = np.array([1,2,2,3,3])
# print(np.unique(arr1))




