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

# # x-axis data
# months = ["Jan","Feb","Mar","Apr","May","Jun"]
# # y-axis data
# sales = [120,150,180,170,210,250]
# # create Figure
# plt.figure(figsize=(10,6))
# # draw the line plot
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
# import matplotlib.pyplot as plt
# months = ["Jan","Feb","Mar","Apr","May"]
# sales = [100,150,180,200,240]
# profit = [20,30,45,55,70]

# plt.plot(months,sales, color="red", marker="D", label="Sales")
# plt.plot(months,profit,color="green",marker="o", label="Profit")

# plt.legend()
# plt.savefig("multi_line_plot.png")
# plt.show()


# Example-3 (Bar Chart)
# import matplotlib.pyplot as plt
# import pandas as pd

# months = ["Jan","Feb","Mar","Apr","May","Jun"]
# sales = [100,120,140,180,220,300]

# df = pd.read_csv("monthly_sales.csv")
# x-axis
# Month = df["Month"]
# y-axis
# Sales = df["Sales"]

# plt.figure(figsize=(10,6))
# bars = plt.bar(Month,Sales,color="skyblue",edgecolor="black",width=0.6,label="Sales")
# for bar in bars:
#     plt.text(bar.get_x() + bar.get_width()/2, bar.get_height()+3, bar.get_height(), ha="center", fontsize=10)

# plt.title("Month - Sales",fontsize=18,fontweight="bold")
# plt.xlabel("Months",fontsize=12)
# plt.ylabel("Sales",fontsize=12)

# plt.grid(axis='y',linestyle="--",alpha=0.7)
# plt.xlim(2.5,5.5)
# plt.ylim(100,400)

# plt.annotate("Highest Sales",xy=(5,300),xytext=(4,330),arrowprops=dict(facecolor="red",shrink=0.05),fontsize=11,color='red')

# plt.savefig("Bar.png")

# plt.legend()
# plt.show()

# Example - 4 (Pie Chart)
# import matplotlib.pyplot as plt

# subjects = ["Python","Java","React","SQL","AWS"]
# marks = [95,85,70,60,90]
# colors=["gold","skyblue","lightgreen","orange","pink"]
# explode = (0.1,0,0,0,0)
# plt.figure(figsize=(8,8))
# plt.pie(marks,
#         labels=subjects,
#         colors=colors,
#         explode=explode,
#         autopct='%1.3f%%',
#         startangle=90,
#         counterclock=True,
#         shadow=True,
#         radius=1.2,
#         pctdistance=0.7,
#         labeldistance=1.1,
        
#         textprops={
#             'fontsize':12,
#             'color':'black'
#         },
#         wedgeprops={
#             'edgecolor':'black',
#             'linewidth':2
#         })
# plt.title("Marks Distribution")
# plt.legend(title="Subjects",
#            loc="upper right")

# plt.savefig("Pie.png")
# plt.show()


# Example - 5
# import matplotlib.pyplot as plt

# subjects = ["Python","Java","React","SQL"]
# marks = [95,85,75,90]

# plt.figure(figsize=(12,8))

# # Line Plot
# plt.subplot(2,2,1)
# plt.plot(subjects,marks,marker='o',linestyle="--")
# plt.title("Line Plot")


# # Bar Chart
# plt.subplot(2,2,2)
# plt.bar(subjects,marks,color="orange")
# plt.title("Bar Chart")


# # Pie Chart
# plt.subplot(2,2,3)
# plt.pie(marks,labels=subjects)


# plt.show()


# Example - 6 (Histoplot)
# import matplotlib.pyplot as plt
# marks = [
#     35, 40, 42, 45, 48,
#     50, 52, 55, 58, 60,
#     62, 65, 68, 70, 72,
#     75, 78, 80, 82, 85,
#     88, 90, 92, 95
# ]
# plt.figure(figsize=(10,6))
# bins - 6  
# 60/6 = 10
# 35 - 45       45 - 55         55-65       65-75       75 - 85     85 - 95
# plt.hist(marks,
#          bins=6,
#          color='skyblue',
#          edgecolor='black',
#          linewidth=2,
#          alpha=0.8,
#          histtype='bar',
#          rwidth=0.9,
#          label='Students')
# plt.title("Students Marks Distribution",fontsize=18,fontweight="bold")
# plt.xlabel("Marks")
# plt.ylabel("Students")
# plt.legend()
# plt.show()


# Example-7
# import matplotlib.pyplot as plt

# study_hours = [1, 2, 3, 4, 5, 6, 7, 8]
# marks = [35, 42, 50, 60, 68, 75, 88, 95]
# sizes = [80, 100, 120, 140, 160, 180, 200, 220]
# colors = ['red', 'blue', 'green', 'orange',
#           'purple', 'brown', 'pink', 'cyan']
# plt.figure(figsize=(10,6))
# plt.scatter(study_hours,marks,s=sizes,c=colors,alpha=0.8,edgecolors='black',linewidths=2,label="Students")
# plt.title("Study Hours Vs Marks")
# plt.legend()
# plt.show()


import matplotlib.pyplot as plt
marks = [
    35,40,45,50,55,
    60,65,70,75,80,
    85,90,95,98,150
]
plt.figure(figsize=(8,6))
plt.boxplot(
    marks,
    notch=True,
    vert=True,
    patch_artist=True,
    widths=0.5,
    showmeans=True,
    showfliers=True,
    tick_labels=['Students'],
    boxprops=dict(
        facecolor='skyblue',
        color='blue',
        linewidth=2
    ),
    medianprops=dict(
        color='red',
        linewidth=3
    ),
    whiskerprops=dict(
        color='green',
        linewidth=2
    ),
    capprops=dict(
        color='black',
        linewidth=2
    ),
    flierprops=dict(
        marker='o',
        markerfacecolor='red',
        markersize=20
    )
)
plt.title(
    "Student Marks Analysis",
    fontsize=18
)
plt.ylabel("Marks")
plt.grid(axis='y')
plt.show()




