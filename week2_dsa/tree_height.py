class Node:
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None
def height(root):
    if root == None:
        return -1
    depth_left = height(root.left)
    depth_right = height(root.right)
    depth = max(depth_left,depth_right) + 1
    return depth