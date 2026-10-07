"""
    numpy - numerical python
    library / python module
    we will download with the help of "pip"

    used to perform list/arrays operations Ex. 1D,2D,3D,....ND
    we can achieve "better memory" management
    numpy operations are "speed"

    1) create virtual environment
        > python -m venv venv
                (or)
        > python3 -m venv venv

    2) activate
        > source venv/bin/activate (mac book)
                (or)
        > venv\Scripts\activate (windows)

    3) create requirements.txt file
            numpy

    4) install requirements.txt file
            > pip install -r requirements.txt
                        (or)
            > pip3 install -r requirements.txt
                        (or)
            > python -m pip install -r requirements.txt
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
# arr1 = np.zeros((3,3))      # float 0.0
# print(arr1)

# arr2 = np.zeros((2,2),dtype="int")  # int ex. 0
# print(arr2)

# arr3 = np.eye(2)        
# print(arr3)

# arr4 = np.identity(3)
# print(arr4)

# arr5 = np.full((2,2),5)
# print(arr5)

# arr6 = np.arange(0,10,2)
# print(arr6)     # [0,2,4,6,8]

# arr7 = np.linspace(0,1,5)       # 1-0 = 1/5 = [0.   0.25 0.5  0.75 1.  ]
# print(arr7)


# Example-4
# import numpy as np
# arr1 = np.array([10,20,30,40,50])
# 10 - 0, -5
# 30 - 2, -3
# 50 - 4, -1
# print(arr1[0])
# print(arr1[-3])
# print(arr1[4])
# print(arr1[-2])
# print(arr1[::2])
# print(arr1[::3])
# print(arr1[::-1])
# print(arr1[::-2])
# print(arr1[::-3])
# print(arr1[0:3])        # 0 included and 3 excluded
# print(arr1[:2])         # 0 included and 2 excluded
# print(arr1[:1+1])       # 0 include and 2 excluded
# print(arr1[2:])         # index 2 to last
# print(arr1[-3:])        # -3 to last index
# print(arr1[-2:])        # -2 to last
# print(arr1[-5:])        # -5 to last
# print(arr1[-5:-2])      # -5 included and -2 onwards excluded
# print(arr1[-4:-1])      # -4 included and -1 onwards excluded


# Example-5
# import numpy as np
# arr1 = np.array([[10,20],
#                  [30,40]])
# print(arr1[0][0])
# print(arr1[1,1])


# Example-6
# import numpy as np
# arr1 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])

# print(arr1[:,0])
# print(arr1[:,2])
# print(arr1[:,0:2])      # all rows, 0th and 1st col included
# print(arr1[:,1:])
# print(arr1[0:1:,0])
# print(arr1[1:2:,1])
# print(arr1[2:,2])


# Example-7
# import numpy as np
# arr1 = np.array([10,20,30])
# arr2 = np.append(arr1,40)
# print(arr2)     # [10 20 30 40]
# print(arr1)     # [10 20 30]
# Note : append() is immutable function in numpy


# Example-8
# import numpy as np
# arr1 = np.array([1,2,3,4,5])
# arr1[0] = 100
# print(arr1)

# arr1[1:4] = 1000        # 1 included and 4 excluded
# print(arr1)

# arr1[arr1<6] = 2000
# print(arr1)







