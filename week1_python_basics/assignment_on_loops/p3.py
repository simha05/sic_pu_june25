number = int(input("Enter the number: "))
prime_numbers = {"2","3","5","7"}
count = 0
for i in str(number):
    if i in prime_numbers:
        count = count + 1
print(count)