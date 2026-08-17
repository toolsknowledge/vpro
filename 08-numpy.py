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