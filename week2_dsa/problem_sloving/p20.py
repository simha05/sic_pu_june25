class TreeNode:
    def __init__(self, x):
        self.x = x
        self.left = None
        self.right = None

def insert(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.x:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

def height(root):
    if root is None:
        return -1 
    left_height = height(root.left)
    right_height = height(root.right)
    return 1 + max(left_height, right_height)

n = int(input())
values = list(map(int, input().split()))

root = None
for val in values:
    root = insert(root, val)

print(height(root))
