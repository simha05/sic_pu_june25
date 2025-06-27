n = int(input("Enter the number of Lines: "))
for rows in range(1,n+1):
    for cols in range(1,n-rows+2):
        print("*", end=" ")
    print()