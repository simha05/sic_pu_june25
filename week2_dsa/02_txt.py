class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

# Get the height of the node
def get_height(node):
    if not node:
        return 0
    return node.height

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

# Right rotate
def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2

    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x

# Left rotate
def left_rotate(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2

    x.height = 1 + max(get_height(x.left), get_height(x.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y

# Insert into AVL tree
def insert(node, key):
    if not node:
        return AVLNode(key)
    elif key < node.key:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)

    node.height = 1 + max(get_height(node.left), get_height(node.right))
    balance = get_balance(node)

    # Rebalance if needed
    if balance > 1 and key < node.left.key:
        return right_rotate(node)
    if balance < -1 and key > node.right.key:
        return left_rotate(node)
    if balance > 1 and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    if balance < -1 and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

# Get the node with minimum key in subtree
def get_min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

# Delete a node from AVL tree
def delete(node, key):
    if not node:
        return node
    elif key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:
        if not node.left:
            return node.right
        elif not node.right:
            return node.left
        temp = get_min_value_node(node.right)
        node.key = temp.key
        node.right = delete(node.right, temp.key)

    node.height = 1 + max(get_height(node.left), get_height(node.right))
    balance = get_balance(node)

    # Rebalance
    if balance > 1 and get_balance(node.left) >= 0:
        return right_rotate(node)
    if balance > 1 and get_balance(node.left) < 0:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    if balance < -1 and get_balance(node.right) <= 0:
        return left_rotate(node)
    if balance < -1 and get_balance(node.right) > 0:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

def inorder(node, res):
    if node:
        inorder(node.left, res)
        res.append(node.key)
        inorder(node.right, res)


def main():
    N = int(input())
    values = list(map(int, input().split()))
    K = int(input())

    root = None
    for val in values:
        root = insert(root, val)

    root = delete(root, K)

    result = []
    inorder(root, result)
    print(" ".join(map(str, result)))


if __name__ == "__main__":
    main()
