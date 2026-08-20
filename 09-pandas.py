"""
    pandas
    ******
        "tabular" data
        Excel / CSV / JSON Data
        "clean" the data
        ready "data" for "visulization"

        pip install pandas

        import pandas as pd
"""
# Example-1
# import pandas as pd
# data = [10,20,30,40,50]

# res = pd.Series(data)
# print(res)

# res = pd.Series(data,index=["Std1","Std2","Std3","Std4","Std5"])
# print(res)

# Example - 2
# import pandas as pd

# data = {
#     "name" : ["Std1","Std2","Std3","Std4","Std5"],
#     "age" : [20,22,24,26,28],
#     "marks" : [50,60,70,80,90]
# }

# df = pd.DataFrame(data)
# print(df)

# df = pd.DataFrame(data,index=[101,102,103,104,105])
# print(df)

# Example-3
# import pandas as pd
# df = pd.read_csv("students.csv")

# print(df)
# print(df.head())
# print(df.head(2))
# print(df.head(10))
# print(df.tail())
# print(df.tail(2))
# print(df.tail(10))
# print(df.shape)
# print(df.columns)
# print(df.dtypes)

# print(df["name"])
# print(df[["name","age"]])

# print(df.loc[0])
# print(df.loc[0:2])
# print(df.loc[1:5])
# print(df.loc[2:])

# print(df[df["marks"]>10])

# df["Grade"] = ["A","B","C","D","E","A","B","C","D","E","A","B","C","D","E","A","B","C","D","E"]
# # print(df)

# df.loc[0,"marks"] = 100


# print( df.drop("age",axis=1) )
# print( df.sort_values("marks") )
# print( df.sort_values("marks",ascending=False) )

# print( df["marks"].sum() )
# print( df["marks"].min() )
# print( df["marks"].max() )
# print( df["marks"].mean() )

# Example - 4
# import pandas as pd
# df = pd.read_csv("employees.csv")

# df.index.name="empid"
# print(df)

# df.index = ["E101","E102","E103","E104","E105"]
# df.index.name = "empid"
# print(df)

# Example - 5
# import pandas as pd
# df = pd.read_csv("students.csv")
# df.drop(2,inplace=True)
# print(df)

# df.drop([1,3],inplace=True)
# print(df)

# df.drop(df.index[:2],inplace=True)
# print(df)

# df.drop(df.index[-2:],inplace=True)
# print(df)



# Example-6
# import pandas as pd
# data = {
#     "Name": ["Ravi", "Sita", "John", "Anu"],
#     "Age": [20, None, 21, 22],
#     "Marks": [85, 90, None, 78],
#     "City": ["Hyderabad", "Chennai", None, "Bangalore"]
# }
# df = pd.DataFrame(data)     # convert object to DataFrame

# print(df.isna())          # know missing values in table (Ex. True (missed))
# print(df.isnull())

# print(df.isna().sum())        # know col wise missing count (Ex. Age:1, Marks:1,....)
# print(df.isna().sum().sum())  # know the total missings in table (Ex. 3)

# print(df[df.isna().any(axis=1)])  # know rows whose have null

# print(df.columns[df.isna().any()])    # know which cols have null

# print(df.isna().any().any())      # check table have missed data or not
# print(df.isna().values.any())

# print(df)
# print("--------------------------------")
# new_df = df.dropna()  # delete rows
# print(new_df)

# print(df.dropna(axis=1))    # delete colums

# df["Age"] = df["Age"].fillna(0)
# df["Marks"] = df["Marks"].fillna(df["Marks"].mean())
# df["City"] = df["City"].fillna(df["City"].mode())
# print(df)


# Example-7
# import pandas as pd
# data = {
#     "Temp" : [30,None,None,35,None]
# }
# df = pd.DataFrame(data)
# print(df)
# print("-----------------")
# df["Temp"] = df["Temp"].ffill()
# print(df)

# df["Temp"] = df["Temp"].bfill()
# print(df)