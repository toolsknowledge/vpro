from sklearn.linear_model import LinearRegression # y = mx + c  y = m1x1 + m2x2 + m3x3 + ..... + c
import numpy as np

# distance  passengers waiting time
X = np.array([[2,1,0],
              [3,2,5],
              [5,1,2],
              [6,3,5],
              [8,2,10]])

# Fare
y = np.array([70,100,130,160,210])


model = LinearRegression()

model.fit(X,y)
print(f"distance slope {model.coef_[0]}")
print(f"passengers slope {model.coef_[1]}")
print(f"time slope {model.coef_[2]}")
print(f"constant {model.intercept_}")

prediction = model.predict([[7,2,5]])
print(prediction[0])