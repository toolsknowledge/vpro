"""
    seaborn
    *******
        used to display "styled graphs"
        built on top of "matplotlib"
        
        pip install seaborn

        import seaborn as sns
"""
# ScatterPlot
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.scatterplot(x="total_bill",y="tip",data=tips)
# plt.show()



# Bar Plot
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.barplot(x="day",y="total_bill",data=tips)
# plt.show()

# histogram
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.histplot(tips["total_bill"],bins=20)
# plt.show()


# box plot
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.boxplot(x="day",y="total_bill",data=tips)
# plt.show()

# import seaborn as sns
# iris = sns.load_dataset("iris")
# print(iris.head())

# flights = sns.load_dataset("flights")
# print(flights.head())

# penguins = sns.load_dataset("penguins")
# print(penguins.head())


import seaborn as sns
import matplotlib.pyplot as plt

marks = [[80,90,70],
         [60,75,85],
         [95,88,92]]

sns.heatmap(marks,cmap="Reds", annot=True)
plt.show()

