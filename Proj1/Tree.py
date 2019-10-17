import random


class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.right = right
        self.left = left

    def change_hop(self, value, lr):
        if lr == 1:
            self.right = value
        if lr == 0:
            self.left = value

    def set_value(self, value):
        self.value = value


class NodeWithParent:
    """Class used for optimization purposes only"""

    def __init__(self, value, left, right, parent):
        self.value = value
        self.right = right
        self.left = left
        self.parent = parent

    def change_hop(self, value, lr):
        if lr == 1:
            self.right = value
        if lr == 0:
            self.left = value

    def set_value(self, value):
        self.value = value

    def inherited(self):
        if self.parent is None:
            return []
        if self.parent.value:
            return [self.parent.value]
        else:
            return self.parent.inherited()


class Tree:

    def __init__(self, default):
        n = Node(default, None, None)
        self.node = n

    def addNode(self, binary, value):
        currNode = self.node
        lastWrittenNode = None
        for i in range(len(binary)):  # for all the characters in the string
            if binary[i] == '1':  # chose the next hop
                nexthop = currNode.right
            else:
                nexthop = currNode.left

            if nexthop is None:  # if there is no node on the way
                newN = Node(None, None, None)  # create a new node
                currNode.change_hop(newN, int(binary[i]))
                nexthop = newN
            elif nexthop.value != None:
                lastWrittenNode = nexthop

            currNode = nexthop
        if len(binary) == 0:
            self.node.value = value
        currNode.set_value(value)

    def getNode(self, binary):
        anchor = self.node
        currNode = self.node
        for i in range(len(binary)):
            if currNode.value is not None:  # save the last value that
                anchor = currNode

            if binary[i] == '1':  # fetch the next node
                nexthop = currNode.right
            else:
                nexthop = currNode.left

            if nexthop is None:  # there is no other node on the way, send the closest node
                return anchor

        return anchor

    def deleteNode(self, binary):
        lastAnchor = self.node
        lastAnchor_i = 0
        currNode = self.node
        for i in range(len(binary)):  # for all the characters in the string
            if currNode.left != None and currNode.right != None:  # if there is another node attached it means we
                # cant delete this node
                lastAnchor = currNode  # save this node as an anchor
                lastAnchor_i = i
            if binary[i] == '1':
                nexthop = currNode.right
            else:
                nexthop = currNode.left
            if nexthop == None:  # there is no node in the tree with this prefix
                return
            else:
                currNode = nexthop
        last_node = currNode
        currNode = lastAnchor
        for i in range(lastAnchor_i, len(binary)):  # for all the nodes from anchor to the node to delete
            if binary[i] == '1':  # remove the node from the tree
                nexthop = currNode.right
                currNode.right = None
            else:
                nexthop = currNode.left
                currNode.left = None
            currNode = nexthop

    def printTree(self):
        dict = {}
        prevlvl = [self.node]
        print("    {}".format(self.node.value))
        currlvl = 0;
        exists = 1;
        while exists:
            currlvl = []
            exists = 0
            for i in prevlvl:
                if i == None:
                    left = None
                    right = None
                else:
                    exists = 1
                    left = i.left
                    right = i.right
                if left is not None:
                    print("  /  ", end=" ")
                else:
                    print("    ", end=" ")
                if right is not None:
                    print(" \\ ", end=" ")
                else:
                    print("    ", end=" ")
                currlvl.append(left)
                currlvl.append(right)
            print("")
            for i in currlvl:
                if i != None:
                    i = i.value
                    if i != None:
                        i = str(i).rjust(4)
                else:
                    i = "    "
                print(i, end=" ")
            print("")
            prevlvl = currlvl

    def printTable(self):
        return treatNode("", self.node)

    def compressTree(self):
        NodeWithParentf = (lambda x, y: NodeWithParent([x.value], x.left, x.right, y))
        nodeList = []
        nodeList.append([NodeWithParentf(self.node, None)])
        level = 0
        exist = True

        # TODO step1 Done
        while exist:
            exist = False
            next_list = []
            for node in nodeList[level]:  # for all nodes on the current level
                has_child = 0
                node_to_append = []
                childs = []
                if node.left is not None:  # add childs to list
                    childs.append(node.left)
                if node.right is not None:
                    childs.append(node.right)
                for child in childs:  # for all the childs
                    if node.value is not None and child.value is None:  # propagate child value if it has none
                        new_node = NodeWithParent(node.value, child.left, child.right, node)
                        next_list.append(new_node)
                    else:
                        new_node = NodeWithParentf(child, node)  # otherwise keep child value
                        next_list.append(new_node)
                    if child != node.right:  # update the corresponding parent arm
                        node.left = new_node
                    else:
                        node.right = new_node
                    exist = True
                    has_child += 1

                if has_child == 1:  # create missing child(a node can only have 0 or 2 childs)
                    if node.left is not None:
                        node.right = NodeWithParent(node.value, None, None, node)
                        node_to_append = node.right
                    else:
                        node.left = NodeWithParent(node.value, None, None, node)
                        node_to_append = node.left
                    next_list.append(node_to_append)
                if has_child:
                    node.value = None
            if exist:  # if therere are more nodes on the next level
                level += 1
                nodeList.append(next_list)
        maxlevel = level
        # TODO step2 Done
        while level >= 0:
            for node in nodeList[level]:  # for all nodes
                if node.left is not None and node.right is not None:  # if its not a leaf node
                    interception = intersection(node.left.value, node.right.value)
                    if not intersection(node.left.value, node.right.value):  # if the intercection returns empty
                        node.value = node.left.value + node.right.value  # the value of the node is the sum of the child values
                    else:
                        node.value = interception  # otherwisethe value of the node is the intercection
                elif node.left is not None:
                    node.value = node.left.value
                elif node.right is not None:
                    node.value = node.right.value
            level -= 1

        level = 0

        while level <= maxlevel:  # TODO step3
            for node in nodeList[level]:
                if intersection(node.inherited(), node.value):
                    node.value = None
                else:
                    rand = random.randint(0, len(node.value) - 1)
                    node.value = node.value[rand]
            level += 1
        level = maxlevel

        new_tree = Tree(None)
        new_tree.node = nodeList[0][0]  # create a new tree in order to run printTable
        diction = new_tree.printTable()  # this returns a dicionary with nodes containinga a value only
        new_tree = Tree(nodeList[0][0])  # this cleans up the tree of nodes with no use
        for key, node in diction.items():  # we then add these nodes to a new tree
            new_tree.addNode(key, node)
        return new_tree  # and return it


def treatNode(currentString, currentNode):
    dict = {}
    if currentNode.value != None:  # add this node to the dictionary
        dict[currentString] = currentNode.value
    if currentNode.left != None:  # add left node dictionary
        dict.update(treatNode(currentString + "0", currentNode.left))
    if currentNode.right != None:  # add right node dictionary
        dict.update(treatNode(currentString + "1", currentNode.right))
    return dict  # return the dictonary


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))
