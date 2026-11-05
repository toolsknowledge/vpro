"""
    numpy
    *****
        numerical python
        lists operations
        better "memory" management
        numpy operations are "speed"
        vectorization
        broadcasting
"""

# Example-1
# import numpy as np
# print(np.__version__)

# Example-2
# import numpy as np
# arr1 = np.array([10,20,30,40,50])
# print(arr1.shape)
# print(arr1.dtype)
# print(arr1.ndim)


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
# print(arr1[0:2])                    # 0 included and 2 excluded
# print(arr1[:1+1+1]) # 0:3           # 0 inluded and 3 excluded
# print(arr1[2:])                     # index 2 to end
# print(arr1[-2:])                    # -2 to end
# print(arr1[-4:-2])                  # -4 included and -2 excluded
# print(arr1[::2])                    # [10, 30, 50]
# print(arr1[::3])                    # [10, 40]
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
# print(arr1[:,0])    # all-rows and col-0
# print(arr1[:,2])    # all-rows and col-2
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


# Example-21
import numpy as np
arr1 = np.array([10,20,30])

# arr2 = arr1           # shallow copy
arr2 = arr1.copy()      # deep copy

arr1[0] = 1000
print(arr2)         # [1000   20   30]