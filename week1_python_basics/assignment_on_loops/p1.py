num = int(input("Enter the number: "))
biggest_digit = 0
for i in str(num):
    if int(i) > biggest_digit:
        biggest_digit = int(i)
        print('biggest digit in a number',biggest_digit )
