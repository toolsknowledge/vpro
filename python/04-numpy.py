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
import numpy as np
arr1 = np.array([10,20,30,40,50])       
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