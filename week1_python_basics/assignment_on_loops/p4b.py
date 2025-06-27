#FIBONACCI NTH TERM

input_number = int(input('Enter the nth term :'))
first_term = 1
second_term = 2
for i in range(3,input_number + 1):
    nth_term = first_term + second_term
    
    first_term = second_term
    second_term = nth_term
print('The Nth term =',nth_term)
