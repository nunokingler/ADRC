import Tree

tree = Tree.Tree(5)
tree.addNode("10", 4)
tree.addNode("11", 3)
tree.addNode("0000",0)
tree.printTree()
tree.deleteNode("0000")
tree.printTree()