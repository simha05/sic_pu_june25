n= int(input("Enter the number of Lines: "))
for rows in range(1,n+1):
    for cols in range(1,n+1):
        if rows == 1 or rows == n or cols == 1 or cols == n:
            print("*", end=" ")
        else:
            print(" ", end=" ")
    print()
