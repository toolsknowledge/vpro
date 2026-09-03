"""
    numpy - numerical python
    numpy library used to perform list operations
    Ex.
            ID
            2D
            ---
            ---
            ND
    numpy provides better memory management
    numpy operations are speed compared to lists (c language)

    numpy supports vectorization

    numpy supports broadcasting

    download
    ********
        pip install numpy
    import
    ******
        import numpy as np

    1) python -m venv venv (or) python3 -m venv venv

    2) create requirements.txt file
                numpy

    3) source venv/bin/activate (mac book)
       venv\Scripts\activate (windows)

    4) pip install -r requirements.txt
                   (or)
       pip3 install -r requirements.txt
                   (or)
       python -m pip install -r requirements.txt
"""

# import numpy as np
# print(np.__version__)


# import numpy as np
# arr1 = np.array([10,20,30])
# print(arr1.shape)
# print(arr1.dtype)
# print(arr1.ndim)

# arr2 = np.array([[10,20,30],
#                  [40,50,60],
#                  [70,80,90]])
# print(arr2.shape)
# print(arr2.dtype)
# print(arr2.ndim)


import numpy as np
arr1 = np.zeros((3,3),dtype=int)
print(arr1)

arr2 = np.ones((2,2),dtype=int)
print(arr2)

arr3 = np.eye(3)
print(arr3)

arr4 = np.full((2,2),10)
print(arr4)

arr5 = np.arange(0,10,2)    # [0,2,4,6,8]
print(arr5)

arr6 = np.linspace(0,1,5)       # 1 - 0 = 1 ---> 1/5 ---> 0. 0.25. 0.5. 0.75  1
print(arr6)





