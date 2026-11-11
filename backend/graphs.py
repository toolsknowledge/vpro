# Line Plot
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("line.csv")

# x-axis
# months = ["Jan","Feb","Mar","Apr","May","June"]
months = df["month"]
# y-axis
# emp1 = [55,60,65,62,72,80]
emp1 = df["emp1"]
# emp2 = [60,65,62,72,80,85]
emp2 = df["emp2"]
plt.figure(figsize=(10,5))

plt.plot(months,
         emp1,
         marker="o",
         linestyle="--",
         linewidth=2,
         label="emp1")

plt.plot(months,
         emp2,
         marker="o",
         linestyle="--",
         linewidth=2,
         label="emp2",
         color="red")

plt.xlabel("Months")
plt.ylabel("Sales")
plt.title("Months - Sales Reports")
plt.xticks(rotation=45)
plt.ylim(0,100)
plt.grid()
plt.legend()
plt.annotate("emp1 highest sales",
             xy=("June",80),
             xytext=("May",90),
             arrowprops=dict(arrowstyle="->"))
plt.savefig("lineplot.png")
plt.show()

