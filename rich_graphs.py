# seaborn
# used to display rich graphs with less codings
# seaborn library built on top of matplotlib
# seaborn library supports readymade datasets
# Ex. tips, flights, ......
# requirements.txt  --- seaborn
# python -m venv venv
# source venv/bin/activate (mac) / venv\Scripts\activate(windows)
# python -m pip install -r requirements.txt

# Lineplot
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.lineplot(data=tips,x="size",y="total_bill")
# plt.show()

# Scatter plot
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.scatterplot(data=tips,x="size",y="tip",hue="sex")
# plt.show()

# bar plot
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.barplot(data=tips,x="day",y="total_bill")
# plt.show()


# histogram
# import seaborn as sns
# import matplotlib.pyplot as plt
# tips = sns.load_dataset("tips")
# sns.histplot(tips["total_bill"],bins=20,kde=True)
# plt.show()

# lineplot() function
# scatterplot()
# barplot()
# histplot()

# heatmap
import seaborn as sns
import matplotlib.pyplot as plt
flights = sns.load_dataset("flights")
pivot = flights.pivot(index="month",columns="year",values="passengers")
sns.heatmap(pivot,annot=True,fmt="d",cmap="plasma")
plt.show()

"""
    anagrams, anscombe, attention, 
    brain_networks, car_crashes, 
    diamonds, dots, dowjones, exercise, flights, fmri, 
    geyser, glue, healthexp, 
    iris, mpg, penguins, planets, 
    seaice, taxis, tips, titanic
"""















