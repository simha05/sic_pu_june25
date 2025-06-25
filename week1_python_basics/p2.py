'''
accept the avg score from the student and give her the result as follows:
0 to 69 fail
70 to 84 is second class
85 to 95 first class
96 to 100 excellent
'''

average_score = int(input("enter the student average score:"))

if average_score >= 0 and average_score <= 69:
    print(average_score,'fail')
elif average_score >= 70 and average_score <= 84:
    print(average_score,'second class')
elif average_score >= 85 and average_score <= 95:
    print(average_score, 'first class')
elif average_score >= 96 and average_score <= 100:
    print(average_score, 'excellent')
else:
    print('invalid input')