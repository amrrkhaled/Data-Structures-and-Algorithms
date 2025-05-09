import sys
import random

RED = True
BLACK = False

class RBNode:
    def __init__(self, value, color=RED, left=None, right=None, parent=None):
        self.value = value
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

    def is_red(self):
        return self.color == RED


class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(value=None, color=BLACK)
        self.root = self.NIL
        self.size=0

    def inorder(self, node):
        if node != self.NIL:
            # Traverse Left
            self.inorder(node.left)
            # Visit Node
            print(str(node.value) +" , ", end=' ')
            # Traverse Right
            self.inorder(node.right)

    def search_helper(self,node,key):
        if node == self.NIL or key == node.value:
            return node
        if key < node.value:
            return self.search_helper(node.left,key)
        elif key >  node.value:
            return self.search_helper(node.right,key)

    def __print_helper(self, node, indent, last):
        if node != self.NIL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            #Using sys.stdout.write() which prints to the output stream
            #But doesn't add a new line automatically like print()

            #OR use print() and concatenate all the above
            s_color = "RED" if node.color == True else "BLACK"
            print(str(node.value) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def searchTree(self,key):
        return self.search_helper(self.root,key)

    def print_tree(self):
        self.__print_helper(self.root, "", True)

    def insert(self, value):
        new_node = RBNode(value=value, left=self.NIL, right=self.NIL, parent=None)
        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if new_node.value < current.value:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        self.size += 1
        self.fix_insert(new_node)

    def get_uncle(self, node):
        grandparent = node.parent.parent
        if grandparent is None:
            return None
        if node.parent==grandparent.left:
            return grandparent.right
        else:
            return grandparent.left

    def rotate_left(self, x):
        y=x.right
        t2 =y.left

        #Perform Rotation & Update Parents & Their Children
        if t2 != self.NIL:  #if y node has left child when rotating t2 becomes right child of x node
            t2.parent=x
        x.right=t2

        y.left=x
        y.parent=x.parent
        if x.parent is None:  #x is the root
            self.root = y
        elif x == x.parent.left: #x is a left child to parent node
            x.parent.left = y #parent's left child is now y node
        else:  #x is a right child to parent node
            x.parent.right = y #parent's  right child is now y node
        x.parent = y #y is now the parent of x


    def rotate_right(self,x):
        y=x.left
        t2=y.right

        # Perform Rotation & Update Parents & Their Children
        if t2 != self.NIL:
            t2.parent=x
        x.left=t2

        y.parent = x.parent
        if x.parent is None:
            self.root=y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def fix_insert(self, node):
        if node.parent is None:
            node.color = BLACK
            return

        if node.parent.color == BLACK:
            return

        uncle = self.get_uncle(node)
        parent = node.parent
        grandparent = parent.parent

        if uncle and uncle.color == RED:
            parent.color = BLACK
            uncle.color = BLACK
            grandparent.color = RED
            self.fix_insert(grandparent)
            return

        # Case: Right-Right
        if node == parent.right and parent == grandparent.right:
            self.rotate_left(grandparent)
            parent.color = BLACK
            grandparent.color = RED
            return

        # Case: Left-Left
        if node == parent.left and parent == grandparent.left:
            self.rotate_right(grandparent)
            parent.color = BLACK
            grandparent.color = RED
            return

        # Case: Right-Left
        if node == parent.left and parent == grandparent.right:
            self.rotate_right(parent)
            self.rotate_left(grandparent)
            node.color = BLACK
            grandparent.color = RED
            return

        # Case: Left-Right
        if node == parent.right and parent == grandparent.left:
            self.rotate_left(parent)
            self.rotate_right(grandparent)
            node.color = BLACK
            grandparent.color = RED
            return

    def __height(self,node):
        if node is None:
            return -1
        else:
            return 1+max(self.__height(node.left),self.__height(node.right))
    def __black_height(self,node,path):
        # path = 1 go right
        # path = 0 go left

        if node == self.NIL:
            return 0
        else:
            if path :
                if node.color == BLACK :
                    return 1+ self.__black_height(node.right,random.randint(0,1))
                else:
                    return self.__black_height(node.right, random.randint(0, 1))
            else :
                if node.color == BLACK:
                    return 1+ self.__black_height(node.left,random.randint(0,1))
                else:
                    return self.__black_height(node.left,random.randint(0,1))

    def print_height(self):
        h=self.__height(self.root)
        print("Height of Tree : "+str(h))

    def print_black_height(self):
        blk_height = self.__black_height(self.root, random.randint(0, 1))
        print("Black Height of Tree : " + str(blk_height))

    def print_tree_size(self):
        n=self.size
        print("Size of Tree : "+str(n))

if __name__ == "__main__":
    rbt = RedBlackTree()

    for i in range(1, 11):
        rbt.insert(i)

    print("Inorder Traversal of Tree:")
    rbt.inorder(rbt.root)
    print("\n")

    print("Tree Structure:")
    rbt.print_tree()

    # Print tree properties
    print("\nTree Info:")
    rbt.print_tree_size()
    rbt.print_height()
    rbt.print_black_height()
