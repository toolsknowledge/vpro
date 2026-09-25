import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

# Step 1: Create the dataset
data = {
    "Point": ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2"],
    "X": [2, 2, 8, 5, 7, 6, 1, 4],
    "Y": [10, 5, 4, 8, 5, 4, 2, 9]
}

df = pd.DataFrame(data)

# Step 2: Define initial centroids
centroids = np.array([
    [2, 10],  # Centroid 1: A1
    [5, 8],   # Centroid 2: B1
    [1, 2]    # Centroid 3: C1
])

# Step 3: Extract data points
X = df[["X", "Y"]].values

# Step 4: Calculate Euclidean distances
distances = cdist(X, centroids, metric="euclidean")

# Step 5: Assign each point to the nearest centroid
df["Distance_C1"] = distances[:, 0].round(2)
df["Distance_C2"] = distances[:, 1].round(2)
df["Distance_C3"] = distances[:, 2].round(2)

df["Cluster"] = np.argmin(distances, axis=1) + 1

print("Initial Cluster Assignments:")
print(df.to_string(index=False))

# Step 6: Apply K-Means clustering
model = KMeans(
    n_clusters=3,
    init=centroids,
    n_init=1,
    random_state=42
)

model.fit(X)

# Step 7: Display final clusters
df["Final_Cluster"] = model.labels_ + 1

print("\nFinal Cluster Assignments:")
print(df[["Point", "X", "Y", "Final_Cluster"]]
      .to_string(index=False))

# Step 8: Display final centroids
print("\nFinal Centroids:")

for i, center in enumerate(model.cluster_centers_, start=1):
    print(f"Cluster {i}: ({center[0]:.2f}, {center[1]:.2f})")