class BinaryTreeNode:
    def __init__(self, left, right, ch):
        self.left = left
        self.right = right
        self.ch = ch

def main():
    n = int(input())
    treeOne = []
    treeTwo = []

    for _ in range(n-1):
        left, right, ch = input().split()
        treeOne.append(BinaryTreeNode(int(left), int(right), ch))

    for _ in range(n-1):
        left, right, ch = input().split()
        treeTwo.append(BinaryTreeNode(int(left), int(right), ch))

    for i in range(n-1):
        if (treeOne[i].left != treeTwo[i].left or
            treeOne[i].right != treeTwo[i].right or
            treeOne[i].ch == treeTwo[i].ch):
            print("no")
            return

    print("yes")

if __name__ == "__main__":
    main()
