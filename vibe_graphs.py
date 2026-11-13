import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Sample data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [120, 150, 170, 160, 200, 230]

categories = ["A", "B", "C", "D", "E"]
values = [23, 45, 56, 78, 33]

pie_labels = ["Rent", "Food", "Travel", "Savings"]
pie_sizes = [35, 25, 15, 25]

hist_data = np.random.normal(50, 12, 500)

box_data = [np.random.normal(m, s, 100) for m, s in [(50, 10), (60, 15), (45, 8)]]

x = np.random.rand(60) * 10
y = 2 * x + np.random.randn(60) * 2

# Subplots (2 rows x 3 cols)
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle("Vibe Graphs Dashboard", fontsize=16)

# 1) Line plot
axes[0, 0].plot(months, sales, marker="o", color="tab:blue")
axes[0, 0].set_title("Line Plot")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Sales")

# 2) Bar chart
axes[0, 1].bar(categories, values, color="tab:orange")
axes[0, 1].set_title("Bar Chart")

# 3) Pie chart
axes[0, 2].pie(pie_sizes, labels=pie_labels, autopct="%1.1f%%")
axes[0, 2].set_title("Pie Chart")

# 4) Histogram
axes[1, 0].hist(hist_data, bins=20, color="tab:green", edgecolor="black")
axes[1, 0].set_title("Histogram")

# 5) Box plot
axes[1, 1].boxplot(box_data, tick_labels=["G1", "G2", "G3"])
axes[1, 1].set_title("Box Plot")

# 6) Scatter plot
axes[1, 2].scatter(x, y, color="tab:red", alpha=0.7)
axes[1, 2].set_title("Scatter Plot")

plt.tight_layout()
plt.savefig("vibe_graphs.png")
plt.show()
