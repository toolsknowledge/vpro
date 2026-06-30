import pandas as pd

# Example-7
df = pd.read_csv("employees_null.csv")
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