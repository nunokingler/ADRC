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
        exist = 1

        # TODO step1 Done
        while exist:
            exist = 0
            nextList = []
            for node in nodeList[level]:
                haschild = 0
                if node.left is not None:
                    exist = 1
                    haschild += 1
                    child = node.left
                    if node.value is not None and child.value is None:
                        nodeToAppend = NodeWithParent(node.value, child.left, child.right, node)
                        nextList.append(nodeToAppend)
                    else:
                        nodeToAppend = NodeWithParentf(child, node)
                        nextList.append(nodeToAppend)
                    node.left = nodeToAppend
                if node.right is not None:
                    exist = 1
                    haschild += 1
                    child = node.right
                    if node.value is not None and child.value is None:
                        nodeToAppend = NodeWithParent(node.value, child.left, child.right, node)
                        nextList.append(nodeToAppend)
                    else:
                        nodeToAppend = NodeWithParentf(child, node)
                        nextList.append(nodeToAppend)
                    node.right = nodeToAppend
                if haschild == 1:
                    if node.left is not None:
                        node.right = NodeWithParent(node.value, None, None, node)
                        nodeToAppend = node.right
                    else:
                        node.left = NodeWithParent(node.value, None, None, node)
                        nodeToAppend = node.left
                    nextList.append(nodeToAppend)
                if haschild:
                    node.value = None
            if exist:
                level += 1
                nodeList.append(nextList)

        # TODO step2 Done
        while level >= 0:
            for node in nodeList[level]:
                if node.left is not None and node.right is not None:
                    interception = intersection(node.left.value, node.right.value)
                    if intersection(node.left.value, node.right.value) == []:
                        node.value = node.left.value + node.right.value
                    else:
                        node.value = interception
                elif node.left is not None:
                    node.value = node.left.value
                elif node.right is not None:
                    node.value = node.right.value
            level -= 1
        None
        # TODO step3


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
