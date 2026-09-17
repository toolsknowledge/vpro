


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