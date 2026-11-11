# Bar Chart
import matplotlib.pyplot as plt

months = ["Jan","Feb","Mar","Apr","May","June"]
sales = [120,150,180,140,200,230]
profit = [30,40,55,35,65,80]

plt.figure(figsize=(10,7))
bars = plt.bar(months,sales)        # sales
bars1 = plt.bar(months,profit)      # profile
plt.xlabel("Months")
plt.ylabel("Sales")
plt.title("Months - Sales Analysis")
plt.ylim(0,300)
plt.grid(axis="y",linestyle="--",alpha=0.5)

for bar in bars:
    value = bar.get_height()
    plt.text(bar.get_x() + (bar.get_width()/2), value, str(value),ha="center",va="bottom")

for bar in bars1:
    value = bar.get_height()
    plt.text(bar.get_x() + (bar.get_width()/2), value, str(value),ha="center",va="bottom")

plt.savefig("bar_chart.png")
plt.show()










# Line Plot
# import matplotlib.pyplot as plt
# import pandas as pd


# df = pd.read_csv("line.csv")

# # x-axis
# # months = ["Jan","Feb","Mar","Apr","May","June"]
# months = df["month"]
# # y-axis
# # emp1 = [55,60,65,62,72,80]
# emp1 = df["emp1"]
# # emp2 = [60,65,62,72,80,85]
# emp2 = df["emp2"]
# plt.figure(figsize=(10,5))

# plt.plot(months,
#          emp1,
#          marker="o",
#          linestyle="--",
#          linewidth=2,
#          label="emp1")

# plt.plot(months,
#          emp2,
#          marker="o",
#          linestyle="--",
#          linewidth=2,
#          label="emp2",
#          color="red")

# plt.xlabel("Months")
# plt.ylabel("Sales")
# plt.title("Months - Sales Reports")
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

