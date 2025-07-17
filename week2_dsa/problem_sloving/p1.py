#  Orange Partitioning

def partition_oranges(oranges):
    n = len(oranges)
    pivot = oranges[-1]  
    
    for i in range(n - 1):
        if oranges[i] <= pivot:
            oranges[i], oranges[k] = oranges[k], oranges[i]
            k += 1

    oranges[k], oranges[-1] = oranges[-1], oranges[k]
    return oranges

n = int(input())
oranges = list(map(int, input().split()))

result = partition_oranges(oranges)

print(*result)
