
class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.right = right
        self.left = left

    def change_hop(self,value,lr):
        if lr==1:
            self.right=value
        if lr==0:
            self.left = value
    def set_value(self, value):
        self.value=value


class Tree:

    def __init__(self,default):
        n = Node(default,None,None)
        self.node = n

    def addNode(self, binary, value):
        currNode=self.node
        lastWrittenNode = None
        for i in range(len(binary)):

            if binary[i]=='1':
                nexthop=currNode.right
            else:
                nexthop=currNode.left

            if nexthop is None:
                newN = Node(None,None,None)
                currNode.change_hop(newN, int(binary[i]))
                nexthop=newN
            elif nexthop.value!=None:
                lastWrittenNode=nexthop

            currNode=nexthop
        currNode.set_value(value)

    def printTree(self):
        dict={}
        prevlvl = [self.node]
        print("    {}".format(self.node.value))
        currlvl=0;
        exists=1;
        while exists:
            currlvl=[]
            exists=0
            for i in prevlvl:
                if i==None:
                    left=None
                    right=None
                else:
                    exists=1
                    left=i.left
                    right=i.right
                if left is not None:
                    print("  /  ", end=" ")
                else :
                    print ("    ", end=" ")
                if right is not None:
                    print(" \\ ", end=" ")
                else :
                    print ("    ", end=" ")
                currlvl.append(left)
                currlvl.append(right)
            print("")
            for i in currlvl:
                if i!=None:
                    i=i.value
                    if i!=None:
                        i=str(i).rjust(4)
                else:
                    i="    "
                print(i , end =" ")
            print("")
            prevlvl=currlvl
