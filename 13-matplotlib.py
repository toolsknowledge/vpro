"""
    matplotlib
    **********
        used to draw graphs
            Ex.1) line plot
               2) bar graph
               3) scatter plot
               4) pie chart
               5) histo plot
               6) sub plots
               --
               --
    pip install matplotlib

    pip install -r requirements.txt

    import matplotlib.pyplot as plt
"""
# Example-1
# import matplotlib.pyplot as plt

# x-axis data
# months = ["Jan","Feb","Mar","Apr","May","Jun"]
# y-axis data
# sales = [120,150,180,170,210,250]
# create Figure
# plt.figure(figsize=(10,6))
# draw the line plot
# plt.plot(
#     months,
#     sales,
#     color="blue",
#     linewidth=3,
#     linestyle="--",                         # --, -, :, -.
#     marker="o",                             # o, *, s, ^, x, D
#     markersize=10,                          # 5 - small  10 - medium  20 - large,
#     markerfacecolor="yellow",
#     markeredgecolor="red",
#     markeredgewidth=2,
#     label="Monthly Sales"
# )
# plt.title("Line Plot Demonistration",fontsize=18)
# plt.xlabel("Months",fontsize=12)
# plt.ylabel("Sales",fontsize=12)
# plt.grid(True)
# plt.xlim('Jan','Jun')
# plt.ylim(100,300)
# plt.legend()
# plt.annotate(
#     "Highest Sales",
#     xy=("Jun",250),
#     xytext=("May",270),
#     arrowprops=dict(facecolor="black")
# )
# plt.savefig("line_plot.png")
# plt.show()

# Example-2
import matplotlib.pyplot as plt
months = ["Jan","Feb","Mar","Apr","May"]
sales = [100,150,180,200,240]
profit = [20,30,45,55,70]

plt.plot(months,sales, color="red", marker="D", label="Sales")
plt.plot(months,profit,color="green",marker="o", label="Profit")

plt.legend()
plt.savefig("multi_line_plot.png")
plt.show()

