import matplotlib.pyplot as plt


# Example-7 (Box Plot)
marks = [35,40,45,50,55,
         60,65,70,75,80,
         85,90,95,98,150]
plt.figure(figsize=(8,6))
plt.boxplot(marks,
            notch=True,
            vert=True,
            patch_artist=True,
            widths=0.5,
            showmeans=False,
            showfliers=False,
            label=['Students'],
            boxprops=dict(facecolor='skyblue',color='blue',linewidth=2),
            medianprops=dict(color='red',linewidth=3),
            whiskerprops=dict(color='green',linewidth=2),
            capprops=dict(color='orange',linewidth=2),
            flierprops=dict(marker='o',markerfacecolor='red',markersize=10)
            )
plt.show()




# Example-6 (Subplot)
# subjects = ["Python","Java","React","SQL"]
# marks = [95,85,75,90]
# plt.figure(figsize=(12,8))

# plt.subplot(2,2,1)
# plt.plot(subjects,marks,marker='o')
# plt.title("Line Plot")

# plt.subplot(2,2,2)
# plt.bar(subjects,marks,color='orange')
# plt.title("Bar Chart")

# plt.subplot(2,2,3)
# plt.pie(marks,labels=subjects,autopct='%1.1f%%')
# plt.title("Pie Chart")

# plt.subplot(2,2,4)
# plt.hist(marks,bins=4,color='green',edgecolor='black')  
# plt.title("Histo Plot")

# plt.tight_layout()
# plt.savefig("vpro6.png")

# plt.show()




# Example-5 (Histo Plot)
# marks = [35,40,42,45,48,
#          50,52,55,58,60,
#          62,65,68,70,72,
#          75,78,80,82,85,
#          88,90,92,95]
# bins - 6
# 95 - 35 = 60 / 6 = 10
# 35 - 45 (bin1) 3
# 45 - 55 (bin2) 4
# 55 - 65 (bin3) 4
# 65 - 75 (bin4) 4
# 75 - 85 (bin5) 4
# 85 - 95 (bin6) 4
# plt.figure(figsize=(10,6))
# plt.hist(marks,
#          bins=6,
#          color='skyblue',
#          edgecolor='black',
#          linewidth=2,
#          alpha=0.8,
#          histtype='stepfilled',
#          rwidth=0.9,
#          label='Students')
# plt.title("Student Marks Distribution",fontsize=18,fontweight='bold')
# plt.xlabel("Marks",fontsize=12)
# plt.ylabel("Number of Students",fontsize=12)
# plt.grid(axis='x',linestyle='--',alpha=0.5)
# plt.xlim(30,100)
# plt.ylim(0,6)
# plt.legend()
# plt.savefig("vpro5.png")
# plt.show()





# Example-4 (Scatter Plot)
# study_hours = [1,2,3,4,5,6,7,8]
# marks = [35,42,50,60,68,75,88,95]
# sizes = [80,100,120,140,160,180,200,220]
# colors = ['red','green','blue','orange','purple','brown','pink','cyan']
# plt.figure(figsize=(10,6))
# plt.scatter(study_hours,
#             marks,
#             s=sizes,
#             c=colors,
#             marker='o',
#             alpha=0.8,
#             edgecolors='black',
#             linewidths=2,
#             label="Students")
# plt.title("Study Hours Vs Marks",fontsize=18,color="red",fontweight="bold")
# plt.xlabel("Study Hours",fontsize=12,color="red")
# plt.ylabel("Marks",fontsize=12,color="red")
# plt.grid(True,linestyle='--',alpha=0.7)
# plt.xlim(0,9)
# plt.ylim(30,100)    
# plt.annotate("Top Student",
#              xy=(8,95),
#              xytext=(6.5,90),
#              arrowprops=dict(facecolor='red',shrink=0.05))
# plt.legend()
# plt.savefig("vpro4.png")
# plt.show()




# Example-3 (Pie Chart)
# subjects = ["Python","Java","React","SQL","AWS"]
# marks = [95,85,70,60,90]
# colors = ['gold','skyblue','lightgreen','orange','pink']
# explode = (0.1,0,0,0,0)
# plt.figure(figsize=(8,8))
# plt.pie(
#     marks,
#     labels=subjects,
#     colors=colors,
#     explode=explode,
#     autopct='%1.1f%%',
#     startangle=90,
#     shadow=True,
#     counterclock=True,
#     radius=0.9,
#     pctdistance=0.7,
#     labeldistance=1.1,
#     wedgeprops={
#         'edgecolor':'black',
#         'linewidth' : 2
#     },
#     textprops={
#         'fontsize':12,
#         'color':'black'
#     }
# )

# plt.title("Student Marks Distribution",fontsize=18,fontweight='bold')
# plt.legend(title="Subjects",loc="upper right")
# plt.savefig("vpro3.png")
# plt.show()






# Example-2 (Bar Graph)
# months = ["Jan","Feb","Mar","Apr","May","Jun"]
# sales = [100,120,140,180,220,300]
# plt.figure(figsize=(10,6))
# bars = plt.bar(months,sales,color='skyblue',edgecolor='black',linewidth=2,width=0.6,label='Sales')

# for bar in bars:
#     plt.text(bar.get_x() + bar.get_width()/2 , 
#              bar.get_height() + 5,
#              bar.get_height(),
#              ha='center',
#              fontsize=10,
#              fontweight='bold',
#              color='red')
    
# plt.xlabel("Months",fontsize=12)
# plt.ylabel("Sales",fontsize=12) 
# plt.title("Months and Sales Data")
# plt.grid(axis='y',linestyle='--',alpha=0.7)
# plt.xlim(2.5,5.5)
# plt.ylim(100,300)

# plt.annotate("Highest Sales",
#              xy=(5,300),
#              xytext=(4,310),
#              arrowprops=dict(facecolor='red',shrink=0.05),
#              fontsize=11,
#              color='red')

# plt.legend()
# plt.savefig("vpro2.png")

# plt.show()




# Example - 1 (Line Plot)
# months = ["Jan","Feb","Mar","Apr","May","Jun"]

# sales = [120,150,180,170,210,250]

# plt.figure(figsize=(10,6))

# plt.plot(
#          months,
#          sales,
#          color='blue',
#          linewidth=3,
#          linestyle='--',

#          marker='o',
#          markersize=10,
         
#          markerfacecolor='yellow',
#          markeredgecolor='red',
#          markeredgewidth=2,

#          label='Months Sales'
#         )

# plt.title('Monthly Sales Data', fontsize=16, fontweight='bold')
# plt.xlabel('Months', fontsize=14)
# plt.ylabel('Sales', fontsize=14)

# plt.grid(True)

# plt.xlim("Jan","Jun")
# plt.ylim(100,300)

# plt.legend()

# plt.annotate("Highest Sales",
#              xy=('Jun',250),
#              xytext=('Apr', 270),
#              arrowprops=dict(facecolor='black', shrink=0.01))


# plt.savefig("vpro1.png")

# plt.show()



