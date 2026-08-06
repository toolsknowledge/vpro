"""
    seaborn
        - Styled Graphs
        - built on top of matplotlib
        - requirements.txt
                seaborn
"""

# Example-1 (Line Plot)
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# tips = tips.head(20)
# sns.lineplot(data=tips,x="size",y="total_bill")
# plt.show()


# Example-2
# import seaborn as sns
# print(sns.get_dataset_names())


# Example-3
# import seaborn as sns
# import matplotlib.pyplot as plt
# iris = sns.load_dataset("iris")
# iris = iris.head(10)
# sns.scatterplot(data=iris,x="sepal_length",y="sepal_width",style="species",hue="species",s=200) 
# plt.show()


# Example-4 (Bar)
# import seaborn as sns
# import matplotlib.pyplot as plt
# diamonds = sns.load_dataset("diamonds")
# diamonds = diamonds.head(10)
# sns.barplot(data=diamonds,x="color",y="carat")
# plt.show()


# Example-5
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.histplot(tips["total_bill"],bins=20,kde=True)
# plt.show()

# Example-6
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.boxplot(data=tips,x="day",y="total_bill")
# plt.show()

# Example-7
import seaborn as sns
import matplotlib.pyplot as plt
flights = sns.load_dataset("flights")
pivot = flights.pivot(index="month",columns="year",values="passengers")
sns.heatmap(pivot,annot=True,fmt="d",cmap="YlGnBu_r")
plt.show()



