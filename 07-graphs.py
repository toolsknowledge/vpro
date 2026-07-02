import matplotlib.pyplot as plt

# Example-3 (Pie Chart)






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



