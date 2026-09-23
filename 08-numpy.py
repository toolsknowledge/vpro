"""
    numpy - numerical python
    used to perform lists operations 1D,2D,....ND
    better memory management
    numpy operaions are speed compared to "normal lists"
    supports "vectorization"
    supports "broadcasting"
"""
# Example-1
# import numpy as np
# print(np.__version__)

# Example-2
# import numpy as np
# arr1 = np.array([10,20,30,40,50])
# print(arr1.shape)
# print(arr1.dtype)
# print(arr1.ndim)      # 1D 2D 3D 

# arr2 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])


# Example-3
# import numpy as np
# arr1 = np.zeros((3,3),dtype=int)
# print(arr1)

# arr2 = np.ones((2,2),dtype=float)
# print(arr2)

# arr3 = np.eye(2)
# print(arr3)

# arr4 = np.full((2,2),10)
# print(arr4)

# arr5 = np.arange(0,10,2)        #[0, 2, 4, 6, 8]
# print(arr5) 

# arr6 = np.linspace(0,1,5)       #1-0 = 1    [0.   0.25 0.5  0.75 1.  ]
# print(arr6)


# Example-4
# import numpy as np
# arr1 = np.array([10,20,30,40,50])
# print(arr1[0])
# print(arr1[-4])
# print(arr1[-1])
# print(arr1[0:2])
# print(arr1[:1+1+1]) # 0:3
# print(arr1[2:])
# print(arr1[-2:])
# print(arr1[-4:-2])
# print(arr1[::2])
# print(arr1[::3])
# print(arr1[::-1])
# print(arr1[::-2])
# print(arr1[::-3])


# Example-5
# import numpy as np
# arr1 = np.array([[10,20],
#                  [30,40]])
# print(arr1[0][0], arr1[0,0])
# print(arr1[1,1])
# print(arr1[1,0])

# Example-6
# import numpy as np
# arr1 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])
# print(arr1[:,0])    # all-rows and col-1
# print(arr1[:,2])    # all-rows and col-3
# print(arr1[:,0:2])  # all-rows and (0th & 1st col)
# print(arr1[:,1:])   # all-rows, 2nd & 3rd cols
# print(arr1[0:1:,0])
# print(arr1[0:1:,2])
# print(arr1[2::,2])



# Example-7
# import numpy as np
# arr1 = np.array([10,20,30])
# arr2 = np.append(arr1,40)
# print(arr2)
# print(arr1)


# Example-8
# import numpy as np
# arr1 = np.array([1,2,3,4,5])
# arr1[0] = 100
# arr1[1:4] = 1000        # [100,1000,1000,1000,5]
# arr1[arr1<6] = 2000     # [ 100 1000 1000 1000 2000]
# print(arr1)


# Example-9
# import numpy as np
# arr1 = np.array([1,2,3,4,5])
# arr2 = np.delete(arr1,1)
# print(arr2)     #[1,3,4,5]

# import numpy as np
# arr1 = np.array([1,2,3,4,5])
# arr2 = np.delete(arr1,[1,3])
# print(arr2)     #[1 3 5]


# Example-10
# import numpy as np
# arr1 = np.array([[10,20,30],
#                  [40,50,60]])
# new_row = [70,80,90]
# arr2 = np.vstack((arr1,new_row))
# print(arr2)

# Exammple-11
# import numpy as np
# arr1 = np.array([[10,20],
#                  [40,50],
#                  [70,80]])
# new_col = np.array([[30],[60],[90]])
# arr2 = np.hstack((arr1,new_col))
# print(arr2)


# Example-12
# import numpy as np
# arr1 = np.array([[10,20],
#                  [40,50],
#                  [70,80]])
# arr2 = np.delete(arr1,0,axis=0)
# print(arr2)       # delete 0th row

# arr2 = np.delete(arr1,2,axis=0)
# print(arr2)       # delete 2nd row

# arr2 = np.delete(arr1,0,axis=1)
# print(arr2)


# Example-13 (vectorization)
# import numpy as np
# arr1 = np.array([1,2,3])
# arr2 = np.array([10,11,12])
# arr3 = arr1 + arr2
# print(arr3)

# Example-14 (broadcasting)
# import numpy as np
# arr1 = np.array([1,2,3])
# x = 10
# arr2 = arr1 + x
# print(arr2)


# Example-15
# import numpy as np
# arr1 = np.array([10,20,30,40,50,60])
# arr2 = arr1.reshape(2,3)
# print(arr2)

# Example-16
# import numpy as np
# arr1 = np.array([10,20,30])     # [[10],[20],[30]]
# arr2 = arr1.reshape(-1,1)
# print(arr2)

# Example-17
# import numpy as np
# arr1 = np.array([[10,20,30],
#                  [40,50,60]])
# arr2 = arr1.flatten()
# print(arr2)


# Example-18
# import numpy as np
# arr1 = np.array([10,50,20,40,30])
# print(np.max(arr1))
# print(np.min(arr1))
# print(np.sum(arr1))
# print(np.mean(arr1))

# res1 = np.sort(arr1)
# print(res1)

# res2 = np.sort(arr1)[::-1]
# print(res2)

# print(arr1)     # sort() immutable


# Example-19
# import numpy as np
# arr1 = np.array([[1,2],
#                  [3,4]])
# print(np.sum(arr1))
# print(np.sum(arr1,axis=0))  # cols
# print(np.sum(arr1,axis=1))  # rows
# print(np.transpose(arr1))   # rows --> cols and cols --> rows
# print(np.linalg.det(arr1))  # det | |


# Example-20
# import numpy as np
# arr1 = np.array([[1,2],
#                  [3,4]])
# arr2 = np.array([[5,6],
#                  [7,8]])
# # print(arr1 * arr2)
# print(arr1 @ arr2)


# Example-21
# import numpy as np
# arr1 = np.array([10,20,30])

# arr2 = arr1         # shallow copy
# arr1[2] = 300
# print(arr2)

# arr2 = arr1.copy()      # deep copy
# arr1[0] = 100
# print(arr2)

# Example-22
# import numpy as np
# arr1 = np.array([50,10,30,20,40])
# print(np.argsort(arr1))

# Example-23
# import numpy as np
# arr1 = np.array([10,20,30,40,50,60,70])
# arr2 = np.where(arr1>=40,"Pass","Fail")
# print(arr2)



# Example-24
# import numpy as np
# arr1 = np.random.rand(3)
# print(arr1)

# arr2 = np.random.randint(1,10,5)
# print(arr2)

# Example-25
# import numpy as np
# arr1 = np.array([4,2])
# arr2 = np.array([3,5])
# print(np.greater(arr1,arr2))
# print(np.less(arr1,arr2))
# print(np.equal(arr1,arr2))





















