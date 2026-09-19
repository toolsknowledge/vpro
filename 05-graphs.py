import matplotlib.pyplot as plt
axes, fig = plt.subplot()
axes[0] = [2,2,1]




# import pandas as pd
# df = pd.DataFrame({
#     "name":["Ravi","Sita","John","Anil"],
#     "age":[25,30,28,35],
#     "city":["Hyderabad","Delhi","Mumbai","Chennai"]
# },index=["A","B","C","D"])
# print(df)
# print(df.loc["A"])
# print(df.loc["B":"D"])
# print(df.loc["C","name"])
# print(df.loc[:,"name"])
# print(df.loc[:,"age"])
# print(df.loc["A":"B","name"])
# print(df.loc["A":"C",["name","age"]])

# print(df.iloc[0])
# print(df.iloc[0:3])
# print(df.iloc[:,1])
# print(df.iloc[0:2,0])

# heatmap
# python std1 - 90(dark green). std2 - 60(green). std3 - 40(light green)
# import matplotlib.pyplot as plt
# students = ["Std1","Std2","Std3","Std4"]
# subjects = ["Python","Java","SQL","React"]
# marks = [[80,70,85,75],
#          [90,85,88,92],
#          [60,65,70,68],
#          [85,90,92,88]]
# plt.imshow(marks,cmap="coolwarm")        # viridis, plasma,magma, cividis,coolwarm,
# plt.xticks(range(len(subjects)),subjects)
# plt.yticks(range(len(students)),students)
# plt.colorbar(label="marks")
# plt.title("Marks Distribution")
# plt.savefig("heat.png")
# plt.show()





# box-plot (analysis 1st quarter, half year, 3rd querter,.....)
# import matplotlib.pyplot as plt

# python_marks = [45,50,52,55,58,60,65,68,70,72]
# java_marks = [40,48,50,55,60,62,65,70,75,90]
# sql_marks = [50,55,58,60,62,65,68,70,72,95]

# plt.boxplot([python_marks,java_marks,sql_marks])
# plt.xticks([1,2,3],["Python","Java","SQL"])
# plt.title("Subject wise marks distribution")
# plt.ylabel("Marks")
# plt.grid(axis='y',linestyle="--",alpha=0.5)
# plt.savefig("box.png")
# plt.show()





# # pie-chart
# import matplotlib.pyplot as plt

# expenses = [30,40,15,10,5]
# categories = ["Rent","Salaries","Marketing","Food","Other"]
# colors = ["red","blue","green","orange","purple"]
# explode = [0,0.1,0,0,0]
# plt.pie(expenses,labels=categories,colors=colors,explode=explode,startangle=90,autopct='%1.1f%%')
# plt.title("Demo Pie Chart")
# plt.legend()
# plt.savefig("pie.png")
# plt.show()



# # histogram (categorize the data)
# import matplotlib.pyplot as plt
# marks = [45,50,52,55,58,
#          60,62,65,67,68,
#          70,72,75,78,80,
#          82,85,88,90,92]
# # bins - 5
# # 92 - 45 = 47 / 5 = 9
# # 45 - 54
# # 54 - 63
# # 63 - 72
# # 72 - 81
# # 81 - last
# plt.hist(marks, bins=5)
# plt.title("Students Marks Distribution")
# plt.xlabel("Marks")
# plt.ylabel("Number of Students")
# plt.grid(axis='y',linestyle="--",alpha=0.5)
# plt.savefig("histo.png")
# plt.show()












# Subplots
# import matplotlib.pyplot as plt

# plt.subplot(2,2,1)
# plt.plot([1,2,3],[10,20,30])
# plt.xlabel("Hours")
# plt.ylabel("Marks")
# plt.title("Line Plot")

# plt.subplot(2,2,2)
# # bar chart
# plt.bar([1,2,3],[10,20,30])
# plt.xlabel("Hours")
# plt.ylabel("Marks")
# plt.title("Line Plot")

# # scatter plot

# # multi line plot

# plt.tight_layout()
# plt.show()









# Scatter Plot
# import pandas as pd
# import matplotlib.pyplot as plt

# data = pd.read_csv("scatter_ex.csv")
# hours = data["hours"]
# marks = data["marks"]

# plt.scatter(hours,marks,marker="o",c="red",s=120)

# plt.xlabel("Hours")
# plt.ylabel("Marks")
# plt.title("Hours <> Marks")
# plt.savefig("scatter.png")
# plt.show()




# # Bar Chart
# import matplotlib.pyplot as plt

# months = ["Jan","Feb","Mar","Apr","May","June"]
# sales = [120,150,180,140,200,230]
# profit = [30,40,55,35,65,80]

# plt.figure(figsize=(10,5))
# bars = plt.bar(months,sales)        # sales
# bars1 = plt.bar(months,profit)      # profile
# plt.xlabel("Months")
# plt.ylabel("Sales")
# plt.title("Months - Sales Analysis")
# plt.ylim(0,300)
# plt.grid(axis="y",linestyle="--",alpha=0.5)

# for bar in bars:
#     value = bar.get_height()
#     plt.text(bar.get_x() + (bar.get_width()/2), value, str(value),ha="center",va="bottom")

# for bar in bars1:
#     value = bar.get_height()
#     plt.text(bar.get_x() + (bar.get_width()/2), value, str(value),ha="center",va="bottom")

# plt.savefig("bar_chart.png")
# plt.show()




# Line Plot
# import matplotlib.pyplot as plt
# # read data from excel sheet
# # read data from databases ---> excel sheet (pandas) (matplotlib)
# # x-axis
# months = ["Jan","Feb","Mar","Apr","May","June"]
# # y-axis
# emp1 = [55,60,65,62,72,80]
# emp2 = [60,65,62,72,80,85]
# # reserve the space for grpahs
# plt.figure(figsize=(10,5))
# plt.plot(months,
#          emp1,
#          marker="o",
#          linestyle="-",
#          linewidth=2,
#          label="emp1")
# plt.plot(months,
#          emp2,
#          marker="x",
#          linestyle=":",
#          linewidth=3,
#          label="emp2",
#          color="red")
# plt.xlabel("Months")
# plt.ylabel("Sales")
# plt.title("Line Plot")
# plt.xticks(rotation=45)
# plt.ylim(0,100)
# plt.grid()
# plt.legend()
# plt.annotate("emp1 highest sales",
#              xy=("June",80),
#              xytext=("May",90),
#              arrowprops=dict(arrowstyle="->"))
# plt.savefig("lineplot.png")
# plt.show()