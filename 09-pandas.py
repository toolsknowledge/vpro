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
import pandas as pd
df = pd.read_csv("students.csv")
# df.drop(2,inplace=True)
# print(df)

# df.drop([1,3],inplace=True)
# print(df)

# df.drop(df.index[:2],inplace=True)
# print(df)

# df.drop(df.index[-2:],inplace=True)
# print(df)