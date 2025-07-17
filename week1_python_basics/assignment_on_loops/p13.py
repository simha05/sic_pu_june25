# right angled traingle

lines = int(input("Lines: "))
for i in range(1, lines+1):
    print('*' * i)

#Equi lateral Triangle

lines = int(input("Lines: "))
for i in range(1, lines+1):
    print(' ' * (lines - i) + '* ' * i)

#Hollow Square

size = int(input("Size: "))
for i in range(size):
    for j in range(size):
        if i == 0 or i == size-1 or j == 0 or j == size-1:
            print('*', end='')
        else:
            print(' ', end='')
    print()

#Howllow Rhombus

n = int(input("Lines: "))
for i in range(n):
    print(' ' * (n - i - 1), end='')
    for j in range(n):
        if i == 0 or i == n-1 or j == 0 or j == n-1:
            print('*', end='')
        else:
            print(' ', end='')
    print()

# Pascal's Triangle

lines = int(input("Lines: "))
for i in range(lines):
    val = 1
    print(' ' * (lines - i), end='')
    for j in range(i + 1):
        print(val, end=' ')
        val = val * (i - j) // (j + 1)
    print()

#x shape

n = int(input("Size (odd preferred): "))
for i in range(n):
    for j in range(n):
        if j == i or j == n - i - 1:
            print('*', end='')
        else:
            print(' ', end='')
    print()

# Benzene Ring (C6H6) Hexagon

n = int(input("Enter size (suggest 3 to 5): "))
for i in range(n):
    print(' ' * (n - i - 1) + '* ' * n)
for i in range(n - 2, -1, -1):
    print(' ' * (n - i - 1) + '* ' * n)


# Find sum of the Even placed digits in the given number.

num = input("Enter number: ")
sum_even_place = 0

for i in range(1, len(num), 2):  # 0-indexed even place = 1, 3,...
    sum_even_place += int(num[i])

print("Sum of even placed digits:", sum_even_place)

#Find sum of the Odd placed Even digits in the given number.

num = input("Enter number: ")
total = 0

for i in range(0, len(num), 2):  # Odd placed digits = index 0, 2, ...
    digit = int(num[i])
    if digit % 2 == 0:
        total += digit

print("Sum of odd placed even digits:", total)
