import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

X = [[1,2],
     [1,3],
     [2,2],
     [2,3],
     [3,3],
     [8,8],
     [8,9],
     [9,8],
     [9,9],
     [8.5,8.5],
     [20,20]]

model = DBSCAN(
    eps=1.5,
    min_samples=3
)

labels = model.fit_predict(X)
print(labels)

plt.scatter([point[0] for point in X],
            [point[1] for point in X],
            c=labels,
            cmap="viridis",
            s=100)
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title("DBSCAN Clustering")
plt.show()

