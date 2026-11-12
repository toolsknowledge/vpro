# import matplotlib
import matplotlib.pyplot as plt

# x-axis
months = ["Jan","Feb","Mar","Apr","May","June"]
# y-axis
emp1 = [55,60,65,62,72,80]
emp2 = [60,65,62,72,80,85]

plt.figure(figsize=(10,5))

plt.plot(months,
         emp1,
         marker="o",
         linestyle="-",
         linewidth="2",
         label="emp1")

plt.plot(months,
         emp2,
         linestyle="--",
         linewidth="3",
         label="emp2",
         marker="x")

plt.xlabel("Months")
plt.ylabel("Sales")
plt.title("Months - Sales Report")
plt.xticks(rotation=45)
plt.ylim(0,100)
plt.grid()
plt.legend()
plt.annotate("emp1 highest sales",
             xy=("June",80),
             xytext=("May",90),
             arrowprops=dict(arrowstyle="->"))
plt.savefig("line.png")
plt.show()



