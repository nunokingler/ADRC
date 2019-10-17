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
        for i in range(len(binary)):

            if binary[i] == '1':
                nexthop = currNode.right
            else:
                nexthop = currNode.left

            if nexthop is None:
                newN = Node(None, None, None)
                currNode.change_hop(newN, int(binary[i]))
                nexthop = newN
            elif nexthop.value != None:
                lastWrittenNode = nexthop

            currNode = nexthop
        if len(binary) == 0:
            self.node.value = value
        currNode.set_value(value)

    def deleteNode(self, binary):
        lastAnchor = self.node
        lastAnchor_i = 0
        currNode = self.node
        for i in range(len(binary)):
            if currNode.left != None and currNode.right != None:
                lastAnchor = currNode
                lastAnchor_i = i
            if binary[i] == '1':
                nexthop = currNode.right
            else:
                nexthop = currNode.left
            if nexthop == None:
                return
            else:
                currNode = nexthop
        last_node = currNode
        currNode = lastAnchor
        for i in range(lastAnchor_i, len(binary)):
            if binary[i] == '1':
                nexthop = currNode.right
                currNode.rigt = None
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
        NodeWithParentf = (lambda x,y: NodeWithParent([x.value], x.left, x.right, y))
        nodeList = []
        nodeList.append([NodeWithParentf(self.node, None)])
        level = 0
        exist = 1

        #TODO step1 Done
        while exist:
            exist = 0
            nextList = []
            for node in nodeList[level]:
                haschild=0
                if node.left is not None:
                    exist = 1
                    haschild+=1
                    child = node.left
                    if node.value is not None and child.value is None:
                        nodeToAppend = NodeWithParent(node.value, child.left, child.right, node)
                        nextList.append(nodeToAppend)
                    else:
                        nodeToAppend=NodeWithParentf(child, node)
                        nextList.append(nodeToAppend)
                    node.left=nodeToAppend
                if node.right is not None:
                    exist = 1
                    haschild+=1
                    child = node.right
                    if node.value is not None and child.value is None:
                        nodeToAppend=NodeWithParent(node.value, child.left, child.right, node)
                        nextList.append(nodeToAppend)
                    else:
                        nodeToAppend=NodeWithParentf(child, node)
                        nextList.append(nodeToAppend)
                    node.right=nodeToAppend
                if haschild==1:
                    if node.left is not None:
                        node.right=NodeWithParent(node.value, None, None, node)
                        nodeToAppend= node.right
                    else:
                        node.left=NodeWithParent(node.value, None, None, node)
                        nodeToAppend=node.left
                    nextList.append(nodeToAppend)
                if haschild:
                    node.value=None
            if exist:
                level += 1
                nodeList.append(nextList)

        #TODO step2 Done
        while level >= 0:
            for node in nodeList[level]:
                if node.left is not None and node.right is not None:
                    interception = intersection(node.left.value,node.right.value)
                    if intersection(node.left.value,node.right.value) == []:
                        node.value=node.left.value + node.right.value
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
    if currentNode.value != None:
        dict[currentString] = currentNode.value
    if currentNode.left != None:
        dict.update(treatNode(currentString + "0", currentNode.left))
    if currentNode.right != None:
        dict.update(treatNode(currentString + "1", currentNode.right))
    return dict


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))
