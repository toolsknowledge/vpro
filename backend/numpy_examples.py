# numpy - numerical python
# lists operations (1D-[], 2D-[[]], 3D-[[[]]], ..... ND)
# numpy operations are "speed" compared to "lists"
# numpy supports "braodcasting"
# numpy supports "vectorization"
# better memory management

# Step 1. requirements.txt -- numpy
# Step 2. python -m venv venv
# Step 3. source venv/bin/activate (mac), venv\Scripts\activate(windows)
# Step 4. python -m pip install -r requirements.txt 

# Example-1
# import numpy as np
# print(np.__version__)


# Example-2
# import numpy as np
# arr1 = np.array([10,20,30,40,50])
# print(arr1.shape)
# print(arr1.dtype)
# print(arr1.ndim)

# arr2 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])
# shape
# dtype
# ndim


# Example-3
# import numpy as np
# arr1 = np.zeros((3,3))
# print(arr1)

# arr2 = np.zeros((2,2),dtype="int")
# print(arr2)

# arr3 = np.eye(2)            # > 3.1
# print(arr3)

# arr4 = np.identity(3)
# print(arr4)

# arr5 = np.full((2,2),2)
# print(arr5)

# arr6 = np.arange(1,10)
# print(arr6)

# arr7 = np.arange(0,10,2)        #[0,2,4,6,8]
# print(arr7)

# arr8 = np.linspace(0,1,5)       # 1-0 = 1/5 [0, 0.25, 0.5, 0.75, 1]
# print(arr8[3])


# Example - 4
# import numpy as np
# arr1 = np.array([10,20,30,40,50])
# print(arr1[0])
# print(arr1[-1])
# print(arr1[2])
# print(arr1[-3])
# print(arr1[0:3])            # 0 onwards included and 3 onwards excluded
# print(arr1[0:4])            
# print(arr1[2:])             # index 2 to last
# print(arr1[:2]) # 0:2
# print(arr1[:1+1+1]) # 0 : 3
# print(arr1[::2])
# print(arr1[::3])
# print(arr1[::-1])
# print(arr1[::-2])
# print(arr1[::-3])

# print(arr1[-2:])
# print(arr1[-4:])
# print(arr1[-5:-2])      # -2 onwards excluded


# Example-5
# import numpy as np
# arr1 = np.array([[10,20],
#                  [30,40]])
# print(arr1[0,0])
# print(arr1[0][0])
# 20
# 30
# 40


# Example-6
# import numpy as np
# arr1 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])
# print(arr1[:,0])    # all rows and col-0

# all rows and col-1
# all rows and col-2

# print(arr1[:,0:2])  # 0 col & 1st-"included" and 2nd col "excluded"
# print(arr1[:,1:])

# print(arr1[0:1:,1]) # [20]
# [10]
# [30]
# [90]

# print(arr1[2::, 2])

# Example-7
# import numpy as np
# arr1 = np.array([[10,20],
#                  [40,50]])
# new_row = [70,80]
# arr2 = np.vstack((arr1,new_row))

# new_col = np.array([[30],[60],[90]])
# arr3 = np.hstack( (arr2,new_col) )
# print(arr3)


# Example-8
# import numpy as np
# arr1 = np.array([[10,20],
#                  [40,50],
#                  [70,80]])
# arr2 = np.delete(arr1,0,axis=0)
# print(arr2)

# arr3 = np.delete(arr1,0,axis=1)
# print(arr3)


# Example - 9 (vectorization)
# import numpy as np
# arr1 = np.array([10,20,30])
# arr2 = np.array([1,2,3])
# arr3 = arr1 + arr2
# print(arr3)


# Example-10 (broadcasting)
# import numpy as np
# arr1 = np.array([10,20,30])
# x = 1
# arr2 = arr1 + x
# print(arr2)


# Example-11
# import numpy as np
# arr1 = np.array([10,20,30,40,50,60])
# arr2 = arr1.reshape(2,3)
# arr3 = arr2.flatten()
# print(arr3)


# Example-12
# import numpy as np
# arr1 = np.array([10,20,30])     # [[10],[20],[30]]
# arr2 = arr1.reshape(-1,1)
# print(arr2)


# Example-13
# import numpy as np
# arr1 = np.array([10,50,20,40,30])
# print(np.max(arr1))
# min
# sum
# mean()
# sort()
# decending


# Example-14
# import numpy as np
# arr1 = np.array([[1,2],
#                  [3,4]])
# print(np.sum(arr1))
# print(np.sum(arr1,axis=0))
# print(np.sum(arr1,axis=1))
# print(np.transpose(arr1))
# print(np.linalg.det(arr1))


# Example-15
# import numpy as np
# arr1 = np.array([4,2])
# arr2 = np.array([3,5])
# print(np.greater(arr1,arr2))
# print(np.less(arr1,arr2))
# print(np.equal(arr1,arr2))

# Example-16
# import numpy as np
# arr1 = np.random.rand(3)
# print(arr1)

# arr2 = np.random.randint(1,10,5)
# print(arr2)


# Example-17
# import numpy as np
# arr1 = np.array([10,20,30,40,50,60,70,80,90,100])
# arr2 = np.where(arr1>=40,"Pass","Fail")
# print(arr2)


# Example-18
# import numpy as np
# arr1 = np.array([50,10,30,20,40])
# print(np.argsort(arr1))         # [1 3 2 4 0]


# Example-19
# import numpy as np
# arr1 = np.array([10,20,30])

# shallow copy arr1 = arr2


# arr2 = arr1.copy()      # deep copy


# Example - 20
# import numpy as np
# arr1 = np.array([[1,2],
#                  [3,4]])
# arr2 = np.array([[5,6],
#                  [7,8]])
# arr3 = arr1 * arr2
# print(arr3)

# arr4 = arr1 @ arr2
# print(arr4)


# Example - 21
# import numpy as np
# arr1 = np.array([1,2,3,4,5])
# arr1[0] = 100
# print(arr1)               # [100   2   3   4   5]

# arr1[1:4] = 1000
# print(arr1)              # [ 100 1000 1000 1000    5]

# arr1[arr1<6] = 2000
# print(arr1)             # [ 100 1000 1000 1000 2000]
