import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


# Feature
X = np.array([[1,50],
              [2,55],
              [2,60],
              [3,65],
              [4,70],
              [5,75],
              [6,80],
              [7,85]])

# Label (Classification)
y = np.array([0,0,0,0,1,1,1,1])


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=42)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

model = SVC(kernel="linear")
model.fit(X_train,y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test,y_pred)
print(accuracy)


res = model.predict(scaler.transform([[5,72]]))
if res[0] == 1:
    print("Pass")
else:
    print("Fail")












