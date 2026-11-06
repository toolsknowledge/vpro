# Example-1
# import pandas as pd
# print(pd.__version__)


# Example-2
# import pandas as pd
# data = [10,20,30,40,50]
# res = pd.Series(data)
# print(res)

# res1 = pd.Series(data,index=["a","b","c","d","e"])
# print(res1)

# res2 = pd.Series(data,index=["Emp1","Emp2","Emp3","Emp4","Emp5"])
# print(res2)

# res3 = pd.Series(data)
# res3 = res3.to_string(index=False)
# print(res3)


# Example-3
# import pandas as pd
# data = {
#     "name":["Std1","Std2","Std3","Std4","Std5"],
#     "marks":[60,70,80,90,100],
#     "dept":["CSE","IT","CSIT","ECE","EEE"]
# }
# res = pd.DataFrame(data)
# print(res)


# Example-4
# import pandas as pd
# data = pd.read_csv("students.csv")

# print(data)
# print(data.shape)
# print(data.columns)
# print(data.dtypes)

# print(data.head())
# print(data.head(2))

# print(data.tail())
# print(data.tail(3))

# print(data["name"])
# print(data.name)
# print(data[["name","dept"]])

# print(data.loc[0])
# print(data.loc[0:3])

# print(data[data["marks"]>12])

# grade = ["A","B","C","D","E"]
# data["grade"] = grade
# print(data.head())

# print( data.drop("dept",axis=1) )


# print( data.sort_values("marks") )
# print( data.sort_values("marks",ascending=False) )

# print(data["marks"].max())
# print(data["marks"].min())
# print(data["marks"].sum())
# print(data["marks"].mean())

# data["address"] = ["Hyd","Vjy","Chennai","Bng","Kolkata"]
# data.to_csv("latest.csv")


# Example-5
# import pandas as pd
# data = pd.read_csv("emps.csv")
# print(data.groupby("dept")["salary"].mean())
# print(data.groupby("dept")["salary"].max())
# print(data.groupby("dept")["salary"].min())
# print(data.groupby("dept")["salary"].sum())


# Example-6
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


# Example-7
# import pandas as pd
# df = pd.DataFrame({
#     "name":["Std1","Std2","Std3","Std4"],
#     "marks":[80,90,70,60],
#     "age":[20,21,22,23]
# })
# df["marks"] = 100
# print(df)

# df["marks"] = df["marks"] + 10
# print(df)

# df[["marks","age"]] = 0
# print(df)

# Example-8
# import pandas as pd
# df = pd.DataFrame({
#     "Name":["Ram","Ram","Ravi","Ravi"],
#     "products":["Laptop","Mobile","Laptop","Mobile"],
#     "sales":[50000,20000,60000,30000]
# })
# print(df)
# print("------------------------------------------")
# res = df.pivot(index="Name",columns="products",values="sales")
# print(res)


# Example-9
import pandas as pd
df = pd.DataFrame({
    "Name":["Ram","Ravi","Anil","Kiran"],
    "marks":[80,None,90,None]
})
print(df)

# x = df.drop(1,inplace=True)
# print(df)
# print(x)

# df.drop([0,1],inplace=True)
# print(df)

# df.fillna(100,inplace=True)
# print(df)

# df["marks"] = df["marks"].ffill()
# print(df)

# df["marks"] = df["marks"].bfill()
# print(df)

# df["marks"] = df["marks"].fillna(df["marks"].mean())
# print(df)

# df.dropna(inplace=True)
# print(df)

# print(df.isnull())
# print(df.isnull().sum())







  
