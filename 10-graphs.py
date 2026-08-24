"""
    matplotlib
    **********
        Graphs,plots and Charts
        Ex. lineplot
        Bar Chart
        Pie Chart
        Subplot
        Box Plot
        Histogram
        Heatmap
    pip install mapplotlib

    import matplotlib.pyplot as plt
"""
# Line Plot
# import matplotlib.pyplot as plt
# months = ["January","February","March","April","May","June"]
# std1 = [55,60,65,62,72,80]
# std2 = [65,68,70,75,78,85]
# std3 = [45,50,55,60,58,70]
# plt.figure(figsize=(10,5))
# plt.plot(months,std1,marker="o",linestyle="-",linewidth=2,label="Std1",color="yellow")
# plt.plot(months,std2,marker="s",linestyle="--",linewidth=2,label="Std2")
# plt.plot(months,std3,marker="^",linestyle=":",linewidth=2,label="Std3")
# plt.xlabel("Months")
# plt.ylabel("Marks")
# plt.title("Student Performance")
# plt.xticks(rotation=45)
# plt.ylim(0,100)
# plt.grid()
# plt.legend()
# plt.annotate( "Std1",
#               xy=("June",80),
#               xytext=("May",90),
#               arrowprops=dict(arrowstyle="->") )

# plt.annotate( "Std2",
#               xy=("June",85),
#               xytext=("May",95),
#               arrowprops=dict(arrowstyle="->") )


# plt.savefig("line.png",dpi=300,bbox_inches="tight")

# plt.show()

# Bar Chart
# import matplotlib.pyplot as plt
# import numpy as np

# students = ["Std1","Std2","Std3"]

# python_marks = [85,90,70]
# java_marks = [78,85,72]
# sql_marks= [82,88,75]
# react_marks = [80,92,68]

# x = np.arange(len(students)) # [0,1,2]

# width = 0.2

# plt.figure(figsize=(12,6))

# plt.bar(x - 1.5 * width,        # [0,1,2] - 0.3 = [-0.3,0.7,1.7]
#         python_marks,
#         width,
#         label="Python")

# plt.bar(x - 0.5 * width,        # [0,1,2] - 0.1 = [-0.1,0.9,1.9]
#         java_marks,
#         width,
#         label="java")

# plt.bar(x + 0.5 * width,
#         sql_marks,
#         width,
#         label="sql")

# plt.bar(x + 1.5 * width,
#         react_marks,
#         width,
#         label="react")

# plt.xticks(x,students)

# plt.xlabel("Students")

# plt.ylabel("Marks")

# plt.title("Subject Wise Bar Chart")

# plt.ylim(0,100)

# plt.grid()

# plt.legend()

# plt.show()

# Pie Chart
# import matplotlib.pyplot as plt
# subjects = ["Python","Java","React","SQL","AWS"]
# marks = [95,85,70,60,90]
# colors = ['gold','skyblue','lightgreen','green','pink']
# explode = (0.1,0,0,0,0)
# plt.figure(figsize=(8,8))
# plt.pie(marks,
#         labels=subjects,
#         colors=colors,
#         autopct='%1.1f%%',
#         startangle=90,
#         shadow=True,
#         counterclock=True,
#         radius=1.0,
#         pctdistance=0.6,
#         labeldistance=0.8,
#         explode=explode,
#         wedgeprops={
#             'edgecolor':'black',
#             'linewidth':2
#         },
#         textprops={
#             'fontsize':12,
#             'color':'black'
#         })
# plt.title("Student Marks Distribution",
#           fontsize=18,
#           fontweight='bold')
# plt.legend(title='Subjects',
#            loc='upper right')
# plt.savefig("marks.png")
# plt.show()

# Scatter Plot
# import matplotlib.pyplot as plt
# study_hours = [1, 2, 3, 4, 5, 6, 7, 8]
# marks = [35, 42, 50, 60, 68, 75, 88, 95]
# # Marker Size
# sizes = [80, 100, 120, 140, 160, 180, 200, 220]
# # Marker Colors
# colors = ['red', 'blue', 'green', 'orange',
#           'purple', 'brown', 'pink', 'cyan']
# plt.figure(figsize=(10,6))
# plt.scatter(study_hours,marks,s=sizes,c=colors,marker='o',alpha=0.8,edgecolors='black',linewidths=2,label='Students')
# plt.title("Student Study Hours Vs Marks",fontsize=18,fontweight='bold')
# plt.xlabel("Study Hours")
# plt.ylabel("Marks")
# plt.grid(linestyle='--',alpha=0.5)
# plt.xlim(0,9)
# plt.ylim(20,100)
# plt.annotate("Top Student",
#              xy=(8,95),
#              xytext=(6.5,90),
#              arrowprops=dict(facecolor='red'),fontsize=11)
# plt.legend()
# plt.savefig("scatter.png")
# plt.show()


# Histo
marks = [
    35, 40, 42, 45, 48,
    50, 52, 55, 58, 60,
    62, 65, 68, 70, 72,
    75, 78, 80, 82, 85,
    88, 90, 92, 95
]