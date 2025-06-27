n = int(input("Enter the number of Lines: "))
for rows in range(n):
    for cols in range(n):
        if rows+cols>=n:
            print("*", end=" ")
        else:
            print(" ", end=" ")
    for k in range(rows - 1):
        print("*", end=" ")
    print()
 