class Node(object):
    """
    Node contains two objects - a leaf and a right child, both may be a Node or both None, latter representing a leaf
    """

    def __init__(self, left=None, right=None):
        super(Node, self).__init__()
        self.left = left
        self.right = right

    def __str__(self):
        """
        Default inorder print
        """

        if self.left is None and self.right is None:
            return "(   )"
        else:
            return "( " + str(self.left) + " " + str(self.right) + " )"

    def __eq__(self, other):
        if self.left is None and self.right is None:
            return other.left is None and other.right is None
        elif other.left is None and other.right is None:
            return False
        else:
            return self.left == other.left and self.right == other.right



def mirrorTree(node):
    """
    Returns the mirror image of the tree rooted at node
    """
    head = Node()
    if node.left is None:
        head.right = None
    else:
        head.right = mirrorTree(node.left)

    if node.right is None:
        head.left = None
    else:
        head.left = mirrorTree(node.right)

    return head

def allTrees(n):
    """
    Returns a list of all unique trees with n internal nodes
    """

    if n == 0:
        return [Node()]

    trees_n = []
    for i in range(n):
        trees_n.extend([Node(x,y) for x in allTrees(i) for y in allTrees(n - 1 - i)])

    return trees_n

def allSymTrees(n):
    """
    Returns a list of all unique symmetrical trees with n internal nodes
    """

    if (n == 0):
        return [Node()]

    
    if (n % 2 == 0):
        return []

    l = (n - 1) / 2
    l = int(l)
    sym_trees_n = [Node(x,mirrorTree(x)) for x in allTrees(l)]

    return sym_trees_n

if __name__ == '__main__':
    for x in allTrees(int(input())):
        print(x)
