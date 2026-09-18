# KNN Classification using Scikit-learn

from sklearn.neighbors import KNeighborsClassifier

# -------------------------------------------------
# 1. Training Data
# -------------------------------------------------

X = [
    [5.3, 3.7],
    [5.1, 3.8],
    [7.2, 3.0],
    [5.4, 3.4],
    [5.1, 3.3],
    [5.4, 3.9],
    [7.4, 2.8],
    [6.1, 2.8],
    [7.3, 2.9],
    [6.0, 2.7],
    [5.8, 2.8],
    [6.3, 2.3],
    [5.1, 2.5],
    [6.3, 2.5],
    [5.5, 2.4]
]

# -------------------------------------------------
# 2. Target / Output
# -------------------------------------------------

y = [
    "Setosa",
    "Setosa",
    "Virginica",
    "Setosa",
    "Setosa",
    "Setosa",
    "Virginica",
    "Versicolor",
    "Virginica",
    "Versicolor",
    "Virginica",
    "Versicolor",
    "Versicolor",
    "Versicolor",
    "Versicolor"
]

# -------------------------------------------------
# 3. Create KNN Model
# -------------------------------------------------

knn = KNeighborsClassifier(n_neighbors=3)

# -------------------------------------------------
# 4. Give training data to the model
# -------------------------------------------------

knn.fit(X, y)

# -------------------------------------------------
# 5. New / Test Flower
# -------------------------------------------------

new_flower = [[5.2, 3.1]]

# -------------------------------------------------
# 6. Predict Species
# -------------------------------------------------

prediction = knn.predict(new_flower)

print("New Flower:")
print("Sepal Length :", new_flower[0][0])
print("Sepal Width  :", new_flower[0][1])

print("\nPredicted Species:", prediction[0])


# Find the 3 nearest neighbors

distances, indexes = knn.kneighbors(new_flower)

print("\nNearest Neighbors:")

for i in range(3):

    index = indexes[0][i]
    distance = distances[0][i]

    print(
        "Rank:", i + 1,
        "| Data:", X[index],
        "| Species:", y[index],
        "| Distance:", round(distance, 3)
    )