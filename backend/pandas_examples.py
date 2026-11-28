# pandas is the python library / module
# pandas will deal excel sheets / csv files / json files /....
# pandas deals tabular data (rows & cols)
# by using pandas able to clean the data
# requirements.txt -- pandas
# python -m venv venv
# source venv/bin/activate (mac book) / venv\Scripts\activate
# pip install -r requirements.txt / python -m pip install -r requirements.txt
# import pandas as pd

# Example-1
# import pandas as pd
# data = [10,20,30,40,50]
# res = pd.Series(data)
# print(res)

# res = pd.Series(data, index=["a","b","c","d","e"])
# print(res)

# res = pd.Series(data, index=["std1","std2","std3","std4","std5"])
# print(res)

# res = pd.Series(data)
# res = res.to_string(index=False)
# print(res)


# Example-2
# import pandas as pd
# data = {
#     "name" : ["std1","std2","std3","std4","std5"],
#     "marks" : [60,70,80,90,100],
#     "dept" : ["CSE","IT","CSIT","ECE","EEE"]
# }
# res = pd.DataFrame(data)
# print(res)



# Example-3
# import pandas as pd
# data = pd.read_csv("students.csv")
# print(data)
# print(data.shape)
# print(data.columns)
# print(data.dtypes)

# print(data.head())
# print(data.head(2))
# print( data.head(10) )

# print( data.tail() )
# print( data.tail(1) )
# print( data.tail(2) )

# print( data["name"] )
# print( data.name )

# print( data[["name","marks"]])    # display two cols at a time

# print( data[data["marks"]>12] )

# print( data.loc[0] )
# print( data.loc[4] )
# print(data.loc[0:2])    # 0 included and 2 included    # 3 students data
# print( data.iloc[0:2] )   # 0 included and 2 excluded

# data = data.sort_values("marks")
# print(data)

# data = data.sort_values("marks",ascending=False)
# print(data)

# print( data["marks"].max() )
# print( data["marks"].min() )
# print( data["marks"].sum() )
# print( data["marks"].mean() )

# new_col = ["A Grade","B Grade","C Grade","D Grade","E Grade"]
# data["grade"] = new_col
# data.to_csv("output.csv")

# data = data.drop("dept",axis=1)
# print(data)

# print( data.loc[0,"marks"] )
# std5 matks
# name of 4th student
# age of 3rd std

# data.loc[0,"marks"] = 100
# print(data)


# Example-3
# import pandas as pd
# data = pd.read_csv("emps.csv")
# print( data.groupby("dept")["salary"].max() )
# print( data.groupby("dept")["salary"].min() )
# print( data.groupby("dept")["salary"].sum() )
# print( data.groupby("dept")["salary"].mean() )


# Example-4
# import pandas as pd
# students = pd.DataFrame({
#     "student_id":[101,102,103,104],
#     "name":["Std1","Std2","Std3","Std4"]
# })
# marks = pd.DataFrame({
#     "student_id":[101,102,103,105],
#     "marks":[80,90,75,88]
# })
# res = pd.merge(students,marks,on="student_id",how="inner")
# print(res)

# res = pd.merge(students,marks,on="student_id",how="left")
# print(res)

# res = pd.merge(students,marks,on="student_id",how="right")
# print(res)

# res = pd.merge(students,marks,on="student_id",how="outer")
# print(res)


# Example-5
# import pandas as pd
# data = pd.DataFrame({
#     "name":["Std1","Std2","Std3","Std4"],
#     "marks":[80,90,70,60],
#     "age":[20,21,22,23]
# })
# data["marks"] = data["marks"] + 10
# print(data)

# data[["marks","age"]] = 0
# print(data)


# Example-6
# import pandas as pd
# data = pd.DataFrame({
#     "Name":["Ram","Ram","Ravi","Ravi"],
#     "products":["Laptop","Mobile","Laptop","Mobile"],
#     "sales":[50000,20000,60000,30000]
# })
# print(data)
# print("------------------------")
# res = data.pivot(index="Name",columns="products",values="sales")
# print(res)


# Example-7
import pandas as pd
data = pd.DataFrame({
    "Name":["Ram","Ravi","Anil","Kiran"],
    "marks":[80,None,90,None]
})

# data["marks"] = data["marks"].ffill()
# print(data)


# data["marks"] = data["marks"].bfill()
# print(data)

# data["marks"] = data["marks"].fillna(50)
# print(data)

# data["marks"] = data["marks"].fillna( data["marks"].mean() )
# print(data)

# print( data.isnull() )
# print( data.isna() )

# print( data.isnull().sum() )

# data.drop(1,inplace=True)
# print(data)


# data.drop([0,2,3],inplace=True)
# print(data)

# res = data.dropna()
# print(res)      # 2 rec
# print(data)     # 4 rec   # inplace=True (immutable nature)


data.dropna(inplace=True)
print(data)     # 2 rec