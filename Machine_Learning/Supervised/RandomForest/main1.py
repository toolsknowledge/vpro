# RandomForest - Classification (0/1) (yes/no) (True/False)
from sklearn.ensemble import RandomForestClassifier

# read from either excel/csv
# link to basic-ui (streamlit) pip install streamlit
# Ex. enter study hours and attendance in text boxes and display result
X = [[1,60],
     [2,65],
     [3,70],
     [4,75],
     [5,80],
     [6,85],
     [7,90],
     [8,90]]
y = [0,0,0,1,1,1,1,1]


model = RandomForestClassifier(n_estimators=11,random_state=42)
model.fit(X,y)
prediction = model.predict([[5,82]])
print(prediction[0])