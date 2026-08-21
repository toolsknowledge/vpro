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
import matplotlib.pyplot as plt
import numpy as np

students = ["Std1","Std2","Std3"]

python_marks = [85,90,70]
java_marks = [78,85,72]
sql_marks= [82,88,75]
react_marks = [80,92,68]

x = np.arange(len(students)) # [0,1,2]

width = 0.2

plt.figure(figsize=(12,6))

plt.bar(x - 1.5 * width,        # [0,1,2] - 0.3 = [-0.3,0.7,1.7]
        python_marks,
        width,
        label="Python")

plt.bar(x - 0.5 * width,        # [0,1,2] - 0.1 = [-0.1,0.9,1.9]
        java_marks,
        width,
        label="java")

plt.bar(x + 0.5 * width,
        sql_marks,
        width,
        label="sql")

plt.bar(x + 1.5 * width,
        react_marks,
        width,
        label="react")

plt.xticks(x,students)

plt.xlabel("Students")

plt.ylabel("Marks")

plt.title("Subject Wise Bar Chart")

plt.ylim(0,100)

plt.grid()

plt.legend()

plt.show()
