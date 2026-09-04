# BaseModel = define the schema(rules and regulations)
from pydantic import BaseModel
# delas - tabular data
import pandas as pd
# Algo - Classification
from sklearn.tree import DecisionTreeClassifier
# import root algo
from sklearn import tree
# graphs
import matplotlib.pyplot as plt
from fastapi import FastAPI
data = pd.read_excel("Decision.xlsx")
df = pd.DataFrame(data)
X = df[["Weather","Temperatures"]]
y = df["Play"]
model = DecisionTreeClassifier()
model.fit(X,y)      # 0.445
plt.scatter(df["Weather"],df["Play"],color="green")
# plt.show()
class Game(BaseModel):
    Weather:int
    Temp:int

app = FastAPI()
@app.post("/game")
def game(input:Game):
    res = model.predict([[input.Weather,input.Temp]])

    return {
        "decision" : int(res[0])
    }
