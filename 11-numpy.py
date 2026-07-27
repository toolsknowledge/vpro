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






