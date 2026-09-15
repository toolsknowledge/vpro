# import pandas as pd

# data = [10,20,30,40,50]
# res = pd.Series(data)
# print(res)

# res = pd.Series(data,index=['a','b','c','d','e'])
# print(res)

# res = pd.Series(data,index=["Std1","Std2","Std3","Std4","Std5"])
# print(res)

# res = pd.Series(data)
# res  = res.to_string(index=False)
# print(res)


# Example-2
# import pandas as pd
# data = {
#     "name":["Std1","Std2","Std3","Std4","Std5"],
#     "marks":[60,70,80,90,100],
#     "dept":["CSE","IT","CSIT","ECE","EEE"]
# }
# res = pd.DataFrame(data)
# print(res)


# import pandas as pd
# data = pd.read_csv("students.csv")

# print(data)    # display data
# print(data.shape)   # rows and cols
# print(data.columns) # display col names
# print(data.dtypes)   # display col name with datatypes

# print(data.head())  # display first 5 rows
# print(data.head(2)) 
# print(data.head(10))


# print(data.tail())
# print(data.tail(2))
# print(data.tail(15))


# print(data["name"])
# print(data.name)

# print(data[["name","marks"]])

# print(data.loc[0])
# print(data.loc[0:5])  # 0 to 5 included

# print( data[data["marks"]>20] )

# adding column
# grade = ["A","B","C","D","E","A","B","C","D","E","A","B","C","D","E","A","B","C","D","E"]
# data["grade"] = grade
# print(data.head())

# delete column
# print( data.drop("dept",axis=1) )

# Ascending
# data = data.sort_values("marks")
# print(data)

# Decending
# data = data.sort_values("marks",ascending=False)
# print(data)

# print(data["marks"].max())
# print(data["marks"].min())
# print(data["marks"].sum())
# print(data["marks"].mean())

# data["grade"] = ["A","B","C","A","B"]
# data.to_csv("output.csv")

# data.loc[0,"marks"] = 90
# print(data)

# import pandas as pd
# data = pd.read_csv("emps.csv")
# print(data.groupby("dept")["salary"].mean())
# print(data.groupby("dept")["salary"].sum())
# print(data.groupby("dept")["salary"].max())
# print(data.groupby("dept")["salary"].min())









