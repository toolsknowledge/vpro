from sklearn.linear_model import LinearRegression       # y = mx + c
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("fare.csv")
X = df[["distance"]]
y = df[["fare"]]

model = LinearRegression()

model.fit(X,y)

print(f"Slope/m/coef {model.coef_[0]}")
print(f"Constant/Intercept {model.intercept_}")


prediction = model.predict([[6]])
print(f"Prediction : {prediction[0]}")

prediction1 = model.predict([[10]])
print(f"Prediction : {prediction1[0]}")


# Scatter
plt.scatter(X,y,label="Actual Data")


X_line = np.array([[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]])
y_line = model.predict(X_line)
plt.plot(X_line,y_line,label="Regression Line")

plt.scatter(6,prediction[0],label="Fare",marker="X",s=150)
plt.scatter(10,prediction1[0],label="Fare",marker="X",s=150,c="Red")
plt.show()