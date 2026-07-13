# mean / average
# num1,num2,num3,num4,num5 = 40,50,60,70,80
# mean = (num1 + num2 + num3 + num4 + num5) / 5
# print(mean) # 60.0


# Deviation (how each element far from mean)
# 40 - 60 = -20
# 50 - 60 = -10
# 60 - 60 = 0
# 70 - 60 = 10
# 80 - 60 = 20
# marks = [40,50,60,70,80]
# mean = sum(marks) / len(marks)
# for mark in marks:
#     deviation = mark - mean
#     print(f"Mark = {mark} and Deviation = {deviation}")


# Standard Deviation (SD) (sum of squares of deviations / number of sample)
# -20 = 400
# -10 = 100
# 0 = 0
# 10 = 100
# 20 = 400
# Total = 1000
# SD = 1000 / 5 = 200.0

# import math
# marks = [40,50,60,70,80]
# mean = sum(marks) / len(marks)

# deviations = [mark-mean for mark in marks]
# print(deviations)

# sqaured_deviations = [deviation**2 for deviation in deviations]
# print(sqaured_deviations)

# variance = sum(sqaured_deviations) / len(marks)
# print(variance)

# standard_deviation = math.sqrt(variance)
# print(standard_deviation)


# Range (diff between max and min value)
# marks = [40,50,60,70,80]
# range = max(marks) - min(marks)
# print(range)

# Median (find the middle value after sorting)
# marks = [40,80,70,60,50]
# marks.sort()
# middle = len(marks) // 2
# print(marks[middle])

# import statistics
# marks = [40,80,70,60,50]
# median = statistics.median(marks)
# print(median)

# Mode - 20
# import statistics
# marks = [10,20,20,30,40]
# print(statistics.mode(marks))

# marks = [10,20,20,30,40]
# frequency = {}
# for mark in marks:
#     if mark in frequency:
#         frequency[mark] += 1
#     else:
#         frequency[mark] = 1

# mode = max(frequency,key = frequency.get)

# print(mode)

# Determinate (det)

"""
    2. 3
    1. 4

    8 - 3 = 5
"""
# import numpy as np
# matrx = np.array([[2,3],[1,4]])
# det = np.linalg.det(matrx)
# print(det)


# import math
# print(math.log10(100))
# print(math.log2(8))


# Correlation
# import numpy as np
# study_hours = [1,2,3,4,5]
# marks = [20,40,60,80,100]

# correlation = np.corrcoef(study_hours,marks)
# print(correlation[0][1])


# import pandas as pd
# data = {
#     "study_hours": [1,2,3,4,5],
#     "marks" : [20,40,60,80,100]
# }
# df = pd.DataFrame(data)
# print(df.corr())

# Covariance
# import numpy as np
# study_hours = [1,2,3,4,5]
# marks = [20,40,60,80,100]
# covariance = np.cov(study_hours,marks)
# print(covariance[0][1])

# import pandas as pd
# data = {
#     "study_hours": [1,2,3,4,5],
#     "marks" : [20,40,60,80,100]
# }
# df = pd.DataFrame(data)
# print(df.cov())

# Normal Distribution
# import numpy as np
# import matplotlib.pyplot as plt

# data = np.random.normal(loc=60,scale=10,size=20)   
# plt.hist(data,bins=3)
# plt.title("Normal Distribution")
# plt.xlabel("Marks")
# plt.ylabel("Frequency")
# plt.show()

# High Bias
# actual = [80,70,90]
# predicted = [60,50,70]

# bias = (sum(predicted) / len(predicted)) - (sum(actual) / len(actual))
# print(bias)


# Error = actual - predicted
# actual = [80,70,90]
# predicted = [60,50,70]

# for a,p in zip(actual,predicted):
#     error = a - p
#     print(error)

# num1, num2 (Features)  num1+num2 (Label)




