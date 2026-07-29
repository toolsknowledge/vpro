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
import pandas as pd
df = pd.read_csv("employees.csv")
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
