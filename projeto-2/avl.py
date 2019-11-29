 
"""
 
Python AVL tree example based on 
 
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/lecture-videos/lec06_code.zip
 
Simplified for Rosetta Code example.
 
See also:
 
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/lecture-videos/MIT6_006F11_lec06_orig.pdf
 
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/lecture-videos/lecture-6-avl-trees-avl-sort/
 
"""
 
class AVLNode(object):
    """A node in the AVL tree."""
 
    def __init__(self, parent, k,value):
        """Creates a node.
 
        Args:
            parent: The node's parent.
            k: key of the node.
        """
        self.key = k
        self.parent = parent
        self.left = None
        self.right = None
        self.value = value
 
    def _str(self):
        """Internal method for ASCII art."""
        label = str(self.key)
        if self.left is None:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = self.left._str()
        if self.right is None:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = self.right._str()
        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)
        if (middle - len(label)) % 2 == 1 and self.parent is not None and \
           self is self.parent.left and len(label) < middle:
            label += '.'
        label = label.center(middle, '.')
        if label[0] == '.': label = ' ' + label[1:]
        if label[-1] == '.': label = label[:-1] + ' '
        lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle-2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
          [left_line + ' ' * (width - left_width - right_width) + right_line
           for left_line, right_line in zip(left_lines, right_lines)]
        return lines, pos, width
 
    def __str__(self):
        return '\n'.join(self._str()[0])
 
    def find(self, k,value ):
        """Finds and returns the node with key k from the subtree rooted at this 
        node.
 
        Args:
            k: The key of the node we want to find.
 
        Returns:
            The node with key k.
        """
        if k == self.key and value == self.value:
            return self
        elif k < self.key:
            if self.left is None:
                return None
            else:
                return self.left.find(k, value)
        elif k > self.key:
            if self.right is None:  
                return None
            else:
                return self.right.find(k, value)
        else:
            if self.right:
                ret_right = self.right.find(k, value)
            else:
                ret_right = None
            if self.left:
                ret_left = self.left.find(k, value)
            else:
                ret_left = None
            return ret_left or ret_right
 
    def find_min(self):
        """Finds the node with the minimum key in the subtree rooted at this 
        node.
 
        Returns:
            The node with the minimum key.
        """
        current = self
        while current.left is not None:
            current = current.left
        return current
 
    def next_larger(self):
        """Returns the node with the next larger key (the successor) in the BST.
        """
        if self.right is not None:
            return self.right.find_min()
        current = self
        while current.parent is not None and current is current.parent.right:
            current = current.parent
        return current.parent
 
    def insert(self, node):
        """Inserts a node into the subtree rooted at this node.
 
        Args:
            node: The node to be inserted.
        """
        if node is None:
            return
        if node.key < self.key:
            if self.left is None:
                node.parent = self
                self.left = node
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                node.parent = self
                self.right = node
            else:
                self.right.insert(node)
 
    def delete(self):
        """Deletes and returns this node from the tree."""
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right is not None:
                    self.parent.right.parent = self.parent
            return self
        else:
            s = self.next_larger()
            self.key, s.key = s.key, self.key
            return s.delete()
 
def height(node):
    if node is None:
        return -1
    else:
        return node.height
 
def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1
 
class AVL(object):
    """
    AVL binary search tree implementation.
    """
 
    def __init__(self):
        """ empty tree """
        self.root = None
 
    def __str__(self):
        if self.root is None: return '<empty tree>'
        return str(self.root)
 
    def find(self, k,value):
        """Finds and returns the node with key k from the subtree rooted at this 
        node.
 
        Args:
            k: The key of the node we want to find.
 
        Returns:
            The node with key k or None if the tree is empty.
        """
        return self.root and self.root.find(k,value)
 
    def find_min(self):
        """Returns the minimum node of this BST."""
 
        return self.root and self.root.find_min()
 
    def next_larger(self, k):
        """Returns the node that contains the next larger (the successor) key in
        the BST in relation to the node with key k.
 
        Args:
            k: The key of the node of which the successor is to be found.
 
        Returns:
            The successor node.
        """
        node = self.find(k)
        return node and node.next_larger()   
 
    def left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.right = y.left
        if x.right is not None:
            x.right.parent = x
        y.left = x
        x.parent = y
        update_height(x)
        update_height(y)
 
    def right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.left = y.right
        if x.left is not None:
            x.left.parent = x
        y.right = x
        x.parent = y
        update_height(x)
        update_height(y)
 
    def rebalance(self, node):
        while node is not None:
            update_height(node)
            if height(node.left) >= 2 + height(node.right):
                if height(node.left.left) >= height(node.left.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif height(node.right) >= 2 + height(node.left):
                if height(node.right.right) >= height(node.right.left):
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent
 
    def insert(self, k,value):
        """Inserts a node with key k into the subtree rooted at this node.
        This AVL version guarantees the balance property: h = O(lg n).
 
        Args:
            k: The key of the node to be inserted.
        """
        node = AVLNode(None, k,value)
        if self.root is None:
            # The root's parent is None.
            self.root = node
        else:
            self.root.insert(node)
        self.rebalance(node)
 
    def delete(self, k,value):
        """Deletes and returns a node with key k if it exists from the BST.
        This AVL version guarantees the balance property: h = O(lg n).
 
        Args:
            k: The key of the node that we want to delete.
 
        Returns:
            The deleted node with key k.
        """
        node = self.find(k,value)
        if node is None:
            return None
        to_return = node.value
        if node is self.root:
            pseudoroot = AVLNode(None, 0,None)
            pseudoroot.left = self.root
            self.root.parent = pseudoroot
            deleted = self.root.delete()
            self.root = pseudoroot.left
            if self.root is not None:
                self.root.parent = None
        else:
            deleted = node.delete()   
        ## node.parent is actually the old parent of the node,
        ## which is the first potentially out-of-balance node.
        self.rebalance(deleted.parent)
        return to_return
 
def test(args=None):
    import random, sys

    items = (random.randrange(100) for i in range(int(10)))

 
    tree = AVL()
    print(tree)
    tree.insert(2, "first")
    tree.insert(2, "second")
    tree.insert(2, "third")
    tree.insert(1, "the one")
    for item in items:
        tree.insert(item, None)
        print()
        print(tree)
    deleted= tree.find_min()
    deleted = tree. delete(deleted.key,deleted.value)
    print("took out " +deleted)
    print(tree)
    print("took out " +tree.delete(2, "second"))
    print(tree)
if __name__ == '__main__': test()
