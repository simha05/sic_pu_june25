#Taxation Problem:
#Level 1: Basic Input and Salary Calculation

employee_name = input("Enter the Name: ")
employee_id = int(input("Enter the ID: "))
empolyee_salary = int(input("Enter employee basic salary: "))
employee_allowences = int(input("Enter the empolyee special allowences: "))
bonus = int(input("Enter the employee bonus: "))
Gross_Monthly_Salary = empolyee_salary+employee_allowences
employee_bonus = bonus/100 * Gross_Monthly_Salary
Annual_Gross_Salary = (Gross_Monthly_Salary*12)+employee_bonus
print(Gross_Monthly_Salary)
print(Annual_Gross_Salary)