"""
    numpy
    *****
        - numerical python
        - better memory utilization
        - perform list operations (speed) 
        - broadcasting
        - vectorization
        - library / module
        - "pip"
    1) create virtual environment
            > cd python
            > python -m venv venv
    2) activate
            > source venv/bin/activate (mac book)
            > venv\Scripts\activate (windows)
    3) create requirements.txt file with numpy
                numpy
    4) download requirements.txt
            > pip install -r requirements.txt
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


# arr2 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])


# Example-3
# import numpy as np
# arr1 = np.zeros((3,3))
# print(arr1)

# arr2 = np.zeros((2,2),dtype=int)
# print(arr2)

# arr3 = np.ones((2,2),dtype=int)
# print(arr3)

# arr4 = np.eye(3)
# print(arr4)

# arr5 = np.identity(2)
# print(arr5)

# arr6 = np.full((3,3),10)
# print(arr6)

# arr7 = np.arange(0,10,2)          # [0,2,4,6,8]  
# print(arr7)

# arr8 = np.linspace(0,1,5)       # 1-0 = 1/5 [0,0.25,0.5,0.75,1]
# print(arr8)


# Example-4
# import numpy as np
# arr1 = np.array([10,20,30,40,50])       
# 10 - 0
# 50 - -1
# 30 - 2
# 40 - -2
# print(arr1[0])
# print(arr1[-3])
# print(arr1[-1])
# print(arr1[::2])
# print(arr1[::3])
# print(arr1[::-1])
# print(arr1[::-2])
# print(arr1[::-3])
# print(arr1[0:3])
# print(arr1[:2]) # 0:2
# print(arr1[:1+1+1]) # 0:3
# print(arr1[2:])
# print(arr1[3:])     # index 3 to last
# print(arr1[-3:])
# print(arr1[-4:-2])



# import numpy as np
# arr1 = np.array([[10,20,30],
#                  [40,50,60]])
# new_row = [70,80,90]
# arr2 = np.vstack((arr1,new_row))
# print(arr2)


# import numpy as np
# arr1 = np.array([[10,20],
#                  [40,50],
#                  [70,80]])
# new_col = np.array([[30],[60],[90]])
# arr2 = np.hstack((arr1,new_col))
# print(arr2)

# import numpy as np
# arr1 = np.array([1,2,3,4,5])
# arr2 = np.delete(arr1,1)
# print(arr2)

# arr2 = np.delete(arr1,[0,3])
# print(arr2)

# import numpy as np

# arr1 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])
# # arr2 = np.delete(arr1,0,axis=0)
# # print(arr2)

# arr2 = np.delete(arr1,2,axis=1)
# print(arr2)

# vectorization
# import numpy as np 
# arr1 = np.array([1,2,3])
# arr2 = np.array([10,11,12])
# arr3 = arr1 + arr2
# print(arr3)

# braodcasting
# import numpy as np
# arr1 = np.array([1,2,3])
# x = 10
# arr2 = arr1 + x
# print(arr2)

# import numpy as np
# arr1 = np.array([10,20,30,40,50,60])    # 1D - ND   
# arr2 = arr1.reshape(2,3)       # 2R - 3C
# print(arr2)


# import numpy as np
# arr1 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])
# arr2 = arr1.flatten()
# print(arr2)

# import numpy as np
# arr1 = np.array([10,50,20,40,30])
# print(np.max(arr1))
# print(np.min(arr1))
# print(np.sum(arr1))
# print(np.mean(arr1))

# arr2 = np.sort(arr1)
# print(arr2)

# arr3 = np.sort(arr1)[::-1]
# print(arr3)

# import numpy as np
# arr1 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])
# res1 = np.sum(arr1,axis=1)      # row wise sum
# print(res1)

# res2 = np.sum(arr1,axis=0)
# print(res2)                    # col wise sum


# import numpy as np
# arr1 = np.array([[1,2],
#                  [3,4]])

# arr2 = np.transpose(arr1)
# print(arr2)

# res = np.linalg.det(arr1)
# print(res)


# import numpy as np
# arr1 = np.array([1,2,3])

# arr2 = arr1             # shallow copy
# arr1[0] = 100
# print(arr2)

# arr2 = arr1.copy()        # deep copy
# arr1[0] = 100
# print(arr2)

# import numpy as np
# arr1 = np.array([[1,2],
#                  [3,4]])

# arr2 = np.array([[5,6],
#                  [7,8]])

# arr3 = arr1 * arr2
# print(arr3)

# arr3 = np.dot(arr1,arr2)
# print(arr3)

# arr3 = arr1 @ arr2
# print(arr3)


# import numpy as np
# marks = np.array([30,40,50,20,70,80,90,10])
# res = np.where(marks>=40,"pass","fail")
# print(res)

# import numpy as np
# arr1 = np.array([4,2])
# arr2 = np.array([3,5])
# print(np.greater(arr1,arr2))
# print(np.less(arr1,arr2))
# print(np.equal(arr1,arr2))


# import numpy as np
# arr1 = np.random.rand(3)
# print(arr1)

# arr2 = np.random.randint(1,10,5)
# print(arr2)


# import numpy as np
#                 #0  1. 2. 3. 4
# arr1 = np.array([50,10,40,20,30])
# print(np.argsort(arr1)) # [1 3 4 2 0]


import numpy as np
arr1 = np.array([1,2,3,4,5])
arr1[0] = 100   # 100 2 3 4 5
arr1[1:4] = 1000        #[100,1000,1000,1000,5]
# 1:4 (1,2,3 included and 4 exluded)
arr1[arr1<6] = 2000
print(arr1)




