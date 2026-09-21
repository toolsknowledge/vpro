"""
    FAISS - Facebook AI Similarity Search
    META
    Search - are too speed
    Embeddings only

    database - index
    tables - index
    row - vector
    primary key - ID
"""

# import faiss
# print(faiss.__version__)


import numpy as np
import faiss
dimensions = 4
index = faiss.IndexFlatL2(dimensions)
data = np.array([[1,2,3,4],
                 [5,6,7,8],
                 [9,10,11,12]],dtype='float32')
index.add(data)

# print(index.reconstruct(0))
# print(index.reconstruct(1))
# print(index.reconstruct(2))

new_data = np.array([[100,200,300,400],
                 [500,600,700,800]],dtype='float32')
index.add(new_data)
# print(index.ntotal)


search_data = np.array([[1,2,3,4]],dtype='float')
distance,indexes = index.search(search_data,2)
print(distance)
print(indexes)

faiss.write_index(index,"demo.index")
