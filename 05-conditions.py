# Example-1
# age = 18
# if age>=18:
#     print("Eligible to Vote")

# print("Done !!!")

# Example-2 (if-else)
# age = 16
# if age > 18:
#     print("Eligible for Vote !!!")
# else:
#     print("Not Eligible for Vote !!!")
# print("Done !!!")

# Example-3 (if...elif..else)
# marks = 75
# if marks >= 90:
#     print("Grade A")
# elif marks >= 75:
#     print("Grade B")
# elif marks >= 50:
#     print("Grade C")
# else:
#     print("Fail")

# Example-4 (and)
# age = 19
# citizen = True
# if age>=18 and citizen:
#     print("Eligible to Vote in India")

# Example-5 (or)
# username = "VPro"
# password = "VPro@123"
# if username == "VPro" or password == "VPro@1234":
#     print("Access Granted !!!")


# Example-6 (not)
# is_logged = False
# if not is_logged:          
#     print("Please Login !!!")

# Example-7 (largest of three)
# a,b,c = 10,20,30
# if a >= b and a >= c:
#     print(a)
# elif b >= a and b >= c:
#     print(b)
# else:
#     print(c)

# Example - 8
# str = "" # Empty String (Falsy)
# if str:
#     print("Not Empty")
# else:
#     print("Empty !!!")

# print( "Not Empty !!!" if str else "Empty !!!" )


# Example - 9
# age = 19
# salary = 30000
# if age >= 18:
#     if salary >= 25000:
#         print("Eligible for Loan !!!")
#     else:
#         print("Salary Not Sufficient !!!")
# else:
#     print("Age not sufficient !!!")

# Example - 10
# list1 = ["python","ML","DL","NLP","GENAI","AGENTICAI"]
# if "AGENTICAI" in list1:
#     print("Available")

# Example-11 (match)
# day = 4
# match day:
#     case 0:
#         print("Sunday")
#     case 1:
#         print("Monday")
#     case 2:
#         print("Tuesday")
#     case 3:
#         print("Wednesday")
#     case 4:
#         print("Thursday")
#     case _:
#         print("No Match")

# Example-12
# marks = 90
# match marks:
#     case x if marks>90:
#         print("Grade A")
#     case x if marks>=90 or marks<=75:
#         print("Grade B")
#     case _:
#         print("Pass")
