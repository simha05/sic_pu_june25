# PRINT PRIME NUMBER IN DECREASING ORDER BETWEEN M AND N

m, n = input('Enter the values of m and n :').split()
m=int(m)
n=int(n)
for i in range(n,m,-1):
    fact = 0
    for j in range(1,i+1):
        if i % j == 0:
            fact = fact + 1
    if fact == 2:
        print(i)
