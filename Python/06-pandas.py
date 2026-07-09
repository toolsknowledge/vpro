import pandas as pd


# Example-10
# df1 = pd.DataFrame({
#     "Name" : ["Emp1","Emp2"]
# })

# df2 = pd.DataFrame({
#     "Name" : ["Emp3","Emp4"]
# })

# df3 = pd.concat([df1,df2])
# print(df3)

# df4 = pd.concat([df1,df2],axis=1)
# print(df4)




# Example-9
# df1 = pd.read_csv("one.csv")
# df1 = pd.DataFrame({
#     "EmpID":[101,102,103],
#     "Name":["Emp1","Emp2","Emp3"]
# })

# df2 = pd.read_csv("two.csv")
# df2 = pd.DataFrame({
#     "EmpID":[101,102,103],
#     "Salary":[50000,60000,70000]
# })

# df3 = pd.merge(df1,df2,on="EmpID")
# print(df3)

# df3 = pd.merge(df1,df2,on="EmpID",how="left")
# print(df3)

# df3 = pd.merge(df1,df2,on="EmpID",how="right")
# print(df3)

# df3 = pd.merge(df1,df2,on="EmpID",how="inner")
# print(df3)

# df3 = pd.merge(df1,df2,on="EmpID",how="outer")
# print(df3)





# Example-8
# employees = {
#     "EmpID": [101,102,103,104,105],
#     "Name": ["Sam","John","David","Priya","Anjali"],
#     "Department": ["IT","HR","Finance","IT","Sales"],
#     "Salary": [55000,70000,45000,90000,60000],
#     "Experience": [2,5,1,8,4]
# }
# df = pd.DataFrame(employees)

# df1 = df.sort_values("Salary")
# df2 = df.sort_values("Salary",ascending=False)
# print(df1)
# print(df2)

# df1 = df.sort_values(
#     by=["Department","Salary"],
#     ascending=[False,True]
# )
# print(df1)

# df1 = df.sort_values("Salary",ascending=False).head(3)
# print(df1)

# df1 = df.groupby("Department")["Salary"].sum()
# print(df1)

# df1 = df.groupby("Department")["Salary"].mean()
# print(df1)

# df1 = df.groupby("Department")["Salary"].max()
# print(df1)

# df1 = df.groupby("Department")["Salary"].min()
# print(df1)

# df1 = df.groupby("Department")["Salary"].count()
# print(df1)

# df1 = df.groupby("Department")["Salary"].agg(["min","max","mean","sum","count"])
# print(df1)







# Example-7
# df = pd.read_csv("employees_null.csv")
# print(df)
# print(df.isnull())
# print(df.isnull().sum())

# df["Salary"] = df["Salary"].fillna(df["Salary"].mean())
# print(df["Salary"])

# df["City"] = df["City"].fillna("Unknown")
# print(df["City"])

# clean_df = df.dropna()
# print(clean_df)

# print(df["PerformanceRating"])
# cleaned_df = df.dropna(subset=["PerformanceRating"])
# print(cleaned_df["PerformanceRating"])


# Example-6
# df = pd.read_csv("employees.csv")
# print(df)
# print(df.head())
# print(df.tail())
# print(df.shape)
# print(df.columns)
# print(df.info())
# print(df.describe()) #mean max min std
# print(df["EmpID"])
# print(df[["EmpID","Name","Salary"]])
# print(df[df["Salary"]>50000])
# print(df[(df["Salary"]>50000) & (df["Age"]>23)])
# df["PerformanceBonus"] = df["Salary"] * 0.10
# print(df.info())

# df.loc[0,"Salary"] = 80000
# print(df.head())

# print(df.iloc[19])

# print(df.shape)
# df.drop("Bonus",axis=1,inplace=True)
# print(df.shape)




# Example-4
# data = {
#     "Name" : ["Emp1","Emp2","Emp3","Emp4","Emp5"],
#     "Age" : [25,30,35,40,45],
#     "Salary" : [50000,60000,70000,80000,90000]
# }
# df = pd.DataFrame(data,index=["a","b","c","d","e"])
# print(df)


# Example-3
# marks = [50,60,70,80,90,100]
# students = ["std1","std2","std3","std4","std5","std6"]
# data = pd.Series(marks,index=students)
# print(data["std6"])


# Example-2
# list1 = [10,20,30,40,50]
# data = pd.Series(list1)
# data = pd.Series(list1,index=["a","b","c","d","e"])
# print(data)


# Exampple-1 (version)
# print(pd.__version__)