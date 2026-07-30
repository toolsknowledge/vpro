"""
    pandas - data analysis
           - data cleaning
           - data transformation 
           - data visualization preparation (Line Plot, Bar Chart, Scatter Plot, Histo Plot....)
           - handling tabular data (rows & cols)
           - CSV / Excel / JSON /.....

    pip install pandas
        (or)
    
    requirements.txt
    pandas
    pip install -r requirements.txt
"""

# Example - 1
# import pandas as pd
# print(pd.__version__)

# Example - 2
# import pandas as pd
# data = [10,20,30,40,50]
# res = pd.Series(data)
# res = pd.Series(data,index=["a","b","c","d","e"])
# print(res)
# print(res["b"])

# Example - 3
# import pandas as pd
# data = [60,70,80,90,100]
# res = pd.Series(data,index=["Std1","Std2","Std3","Std4","Std5"])
# print(res["Std5"])

# Example - 4
# import pandas as pd
# employees = {
#     "EmpId" : [101,102,103,104,105],
#     "Department" : ["IT","Admin","HR","Finance","Tech"],
#     "Salary" : [60000,70000,80000,90000,1000000]
# }
# res = pd.DataFrame(employees)
# res = pd.DataFrame(employees,index=[1,2,3,4,5])
# print(res)


# Example - 5
# import pandas as pd
# df = pd.read_csv("employees.csv")
# print(df)
# print( df.head() )
# print( df.tail() )
# print(df.head(10))
# print( df.shape )
# print( df.columns )
# print( df.info() )
# print( df[["EmpID","City","PerformanceRating"]])
# print(df.describe())

# print( df[ df["Salary"]>50000 ] )
# print(df[ (df["Salary"]>50000) & (df["Age"]>23) ])

# print( df.sort_values("Salary") )
# print( df.sort_values("Salary",ascending=False))

# print( df.groupby("Department")["Salary"].max() )
# print( df.groupby("Department")["Salary"].min() )
# print( df.groupby("Department")["Salary"].mean() )
# print( df.groupby("Department")["Salary"].count() )

# print( df[ df["Department"] == "IT" ]["Salary"].max() )
# print( df[ df["Department"] == "IT" ]["Salary"].min() )
# print( df[ df["Department"] == "IT" ]["Salary"].mean() )
# print( df[ df["Department"] == "IT" ]["Salary"].count() )

# print( df["Name"].str.upper() )
# print( df["Name"].str.lower() )
# print( df[df["Name"].str.contains("Asha")] )

# print(df[0:3])
# print(df[:2])
# print(df[:0+1])
# print(df[10:11])



# import pandas as pd
# df = pd.read_csv("employees_simple.csv")
# print(df)

# df = pd.read_csv("employees_simple.csv")
# print( df.to_string(index=False) )

# df = pd.read_csv("employees_simple.csv")
# df.set_index("Name",inplace=True)
# print(df)

# df = pd.read_csv("employees_simple.csv")
# print(df)

# print(df.loc[0])
# print(df.loc[0:2])
# print(df.loc[0,"Salary"])

# print(df.iloc[2])
# print(df.iloc[2,2])
# print(df.iloc[0:2])

# df = df.set_index("Name")
# print(df)
# print(df.loc["Sam"])
# print(df.loc["David"])

# print(df)
# print(df.loc[:,["Name","Age"]])
# print(df.loc[2:,["Name","Salary"]])
# print(df.loc[0:1 :, ["Name","Age"]])


# import pandas as pd
# employees = {
#     "EmpID" : [101,102,103,104,105],
#     "Name" : ["Sam","John","David","Priya","Anjali"],
#     "Department" : ["IT","HR","Finance","IT","Sales"],
#     "Salary" : [55000,70000,45000,90000,60000],
#     "Experience" :[2,5,1,8,4]
# }
# df = pd.DataFrame(employees)

# print(df)
# print( df.sort_values("Salary") )

# print( df.sort_values("Salary",ascending=False) )

# print(df.sort_values(
#     by=["Department","Salary"],
#     ascending=[True,True]
# ))

# print( df.sort_values("Salary",ascending=False).head(1))

# print( df.groupby("Department")["Salary"].sum() )
# print( df.groupby("Department")["Salary"].max() )
# print( df.groupby("Department")["Salary"].min() )
# print( df.groupby("Department")["Salary"].mean() )
# print( df.groupby("Department")["EmpID"].count() )

# print( df.groupby("Department")["Salary"].agg(["min","max","mean","sum","count"]))


# import pandas as pd
# emps = {
#     "EmpID" : [101,102,103,104,105],
#     "Name" : ["Sam","John","David","Priya","Anjali"]
# }
# df1 = pd.DataFrame(emps)

# salaries = {
#     "EmpID" : [101,102,103,104,106],
#     "Salary" : [55000,70000,45000,90000,60000]
# }
# df2 = pd.DataFrame(salaries)

# result = pd.merge(df1,df2,on="EmpID")
# print(result)

# result = pd.merge(df1,df2,on="EmpID",how="left")
# print(result)

# result = pd.merge(df1,df2,on="EmpID",how="right")
# print(result)

# import pandas as pd
# df1 = pd.DataFrame({
#     "Name" : ["Emp1","Emp2"]
# })

# df2 = pd.DataFrame({
#     "Name" : ["Emp3","Emp4"]
# })

# print( pd.concat([df1,df2]) )
# print( pd.concat([df1,df2],axis=1) )


# import pandas as pd
# employees = {
#     "EmpID" : [101,102,103,104,105],
#     "Name" : ["Sam","John","David","Priya","Anjali"],
#     "Department" : ["IT","HR","Finance","IT","Sales"],
#     "Salary" : [55000,70000,45000,90000,60000],
#     "Experience" :[2,5,1,8,4]
# }
# df = pd.DataFrame(employees)

# df["AnnualSalary"] = df["Salary"] * 12
# print(df)

# df.drop("Experience",axis=1,inplace=True)
# print(df)


import pandas as pd
df = pd.read_csv("employees_null.csv")
# print(df)
# print(df.isnull())
# print(df.isnull().sum())
# print( df.fillna({"Name":"Unknown","Age":0,"Salary":0.0,"Bonus":0.0},inplace=True) )
# print( df["Salary"].fillna(df["Salary"].mean(),inplace=True) ) 








