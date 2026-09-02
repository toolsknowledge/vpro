from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
X = np.array([[1],[2],[3],[4],[5]])
y = np.array([50,60,75,100,135])
ploy = PolynomialFeatures(degree=2)
X_poly = ploy.fit_transform(X)          # [[1],[2],[3].....] ----> [[1,1,1],[2,2,4],[3,3,9]]
model = LinearRegression()
model.fit(X_poly,y)
print(model.coef_[0])
print(model.intercept_)
prediction = model.predict(ploy.transform(np.array([[6]])))
print(prediction[0])