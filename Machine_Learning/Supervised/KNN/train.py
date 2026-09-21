import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import joblib

# Training data
X = np.array([
    [1000],
    [1200],
    [1500],
    [1800],
    [2000]
])

y = np.array([
    30,
    36,
    45,
    54,
    60
])

# Create model
model = KNeighborsRegressor(n_neighbors=3)

# Train
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model saved successfully!")

# python train.py