import seaborn as sns
import matplotlib.pyplot as plt

taxis = sns.load_dataset("taxis")
print(taxis.head())

iris = sns.load_dataset("iris")
print(iris.head())


# Example-5 (pairplot)
# tips = sns.load_dataset("tips")
# sns.pairplot(tips)
# plt.show()


# Example-4 (HeatMap)
# tips = sns.load_dataset("tips")
# corr = tips.corr(numeric_only=True)
# sns.heatmap(
#     corr,
#     annot=True,
#     cmap="coolwarm"
# )
# plt.show()


# Example-3 (Box Plot)
# tips = sns.load_dataset("tips")
# sns.boxplot(
#     x="day",
#     y="total_bill",
#     data=tips
# )
# plt.show()


# Example-2 (histplot)
# tips = sns.load_dataset("tips")
# sns.histplot(tips["total_bill"],bins=20,kde=True)
# plt.show()


# Example-1 (Scatter Plot)
# tips = sns.load_dataset("tips")
# tips = tips.head()
# sns.scatterplot(x="total_bill",y="tip",data=tips)
# plt.show()