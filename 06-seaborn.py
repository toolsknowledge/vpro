"""
    seaborn
    *******
        display "plots" and "graphs"
        built on top of "matplotlib"
        styled "graphs"
        "less coding" able to build "rich graphs"
        "seaborn" provides "predefined" "datasets"

        pip install seaborn

        import seaborn as sns
"""

# lineplot
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.lineplot(data=tips, x="size", y="total_bill")
# plt.show()

# scatter plot
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.scatterplot(data=tips, x="size", y="tip",hue="sex")
# plt.show()


# bar plot
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.barplot(data=tips, x="day", y="total_bill")
# plt.show()


# histo
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.histplot(tips["total_bill"],bins=20,kde=False)
# plt.show()


# heatmap
# import seaborn as sns
# import matplotlib.pyplot as plt

# flights = sns.load_dataset("flights")
# print(flights.head(10))
# pivot = flights.pivot(index="month",columns="year",values="passengers")
# sns.heatmap(pivot,annot=True,fmt="d",cmap="plasma")
# plt.show()



