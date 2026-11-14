import seaborn as sns
import matplotlib.pyplot as plt

iris = sns.load_dataset("iris")

# Line plot: trend of a measurement across rows
plt.figure()
sns.lineplot(data=iris, x=iris.index, y="sepal_length")
plt.title("Line plot: sepal length by row")

# Bar chart: average petal length per species
plt.figure()
sns.barplot(data=iris, x="species", y="petal_length")
plt.title("Bar chart: mean petal length by species")

# Scatter plot: relationship between two measurements
plt.figure()
sns.scatterplot(data=iris, x="sepal_length", y="petal_length", hue="species")
plt.title("Scatter plot: sepal vs petal length")

# Heatmap: correlation between numeric columns
plt.figure()
sns.heatmap(iris.drop(columns="species").corr(), annot=True, cmap="coolwarm")
plt.title("Heatmap: feature correlation")

# Histogram: distribution of one measurement
plt.figure()
sns.histplot(data=iris, x="sepal_width", bins=15)
plt.title("Histogram: sepal width distribution")

plt.show()
