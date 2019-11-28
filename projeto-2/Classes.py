import math
import os
import cmd


class CouldNotOpenFile(Exception):
    def __init__(self):
        None


class Grid(cmd.Cmd):
    """Command line implementation"""
    intro = 'Welcome to the shell!'
    prompt = '(input) '
    file = None

    def emptyline(self):
        """
            nullify emptyline
        """
        print()

    def __init__(self):
        super(Grid, self).__init__()
        self.nodes = {}
        self.stubs = []
        self.tops = []
        self.toAdvert = []

    def do_foo(self, arg):
        'function with breakpoint for development purposes'
        print("stop fooing around!")

    def do_file(self, arg):
        if not arg:
            print("please refer to the help for command documentation")
            return None
        try:
            script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
            rel_path = arg  # "res/" + arg
            abs_file_path = os.path.join(script_dir, rel_path)
            print('opening:' + abs_file_path)
            with open(abs_file_path, 'r') as file:
                line = file.readline()
                while line:
                    parts = line.split()
                    if len(parts) == 3:
                        self.do_addRelationship(line)

                    line = file.readline()
        except Exception as ex:
            print(
                "there was a problem opening that file up, you should try again later or check the command documentation")

    def do_addRelationship(self, arg):
        'Add a relationship between nodes: addRelationship (int)nodeID1 (int)nodeID2 (int)relationship(from 1-nodeID1 is provider of nodeID2 2-both are equal 3- nodeID1 is customer of nodeID2)'
        if not arg:
            print("please refer to the help for command documentation")
            return None
        arglist = arg.split()
        if len(arglist) != 3:
            print("please refer to the help for command documentation")
            return None
        try:
            nodeID1 = int(arglist[0])
            nodeID2 = int(arglist[1])
            relationship = int(arglist[2])
        except Exception as ex:
            print("please refer to the help for command documentation")
            return None

        if relationship == 3:
            nodeaux = nodeID1
            nodeID1 = nodeID2
            nodeID2 = nodeaux
            relationship = invertRelationship(relationship)
        try:
            node1 = self.nodes[nodeID1]
        except:
            node1 = Node(nodeID1)
            self.nodes[nodeID1] = node1
        try:
            node2 = self.nodes[nodeID2]
        except:
            node2 = Node(nodeID2)
            self.nodes[nodeID2] = node2

        node1.addEdge(node2, relationship)

    def do_comPath(self, arg):
        'calculates commercial path to every node'
        if not arg:
            print("please refer to the help for command documentation")
            return None
        arglist = arg.split()
        if len(arglist) != 2:
            print("wrong argument number, please refer to the help for command documentation")
            return None
        try:
            start = int(arglist[0])
            end = int(arglist[1])
            nodeStart = self.nodes[start]
            nodeEnd = self.nodes[end]
        except Exception as ex:  # one of the nodes is not in the nodeList
            print("node does not exist or node is not integer")
            return None
        nodeList = list(self.nodes.values())

        for node in self.nodes.values():
            node.resetDistPrev()
        nodeStart.dist = 0
        nodeStart.prev = None
        nodeStart.lastRelationship = 4
        reached = False

        while nodeList:
            currNode = takeSmallerRelationshipNode(nodeList)#TODO change this to be a ordered array or something
            if reached and currNode.lastRelationship >= nodeEnd.lastRelationship:
                break
            for edge in list(currNode.edges.values()):
                relative = edge.getRelative(currNode)
                if currNode.lastRelationship == 1 or currNode.lastRelationship == 4:
                    if relative.dist > currNode.dist + 1:  # +1 for each edge
                        relative.dist = currNode.dist + 1
                        relative.prev = currNode
                        relative.lastRelationship = edge.getRelationship(relative)
                elif currNode.lastRelationship == 2:
                    if (relative.lastRelationship == 2 or relative.lastRelationship==0) and relative.dist > currNode.dist+1 and edge.getRelationship(currNode)!= 2tes:
                        relative.dist = currNode.dist + 1
                        relative.prev = currNode
                        relative.lastRelationship = 2
                elif currNode.lastRelationship == 3:
                    if edge.getRelationship(currNode) == 1 and relative.dist>currNode.dist+1:#if current node is provider
                        relative.dist = currNode.dist + 1
                        relative.prev = currNode
                        relative.lastRelationship = edge.getRelationship(relative)

                if relative.ID == nodeEnd.ID and not math.isinf(relative.dist):
                    reached = True
        if reached:
            path = [nodeEnd.ID]
            currNode = nodeEnd.prev
            while currNode != None:
                path.insert(0, currNode.ID)
                currNode = currNode.prev
            print("reached node {} from {} with {} jumps using path {} ".format(nodeEnd.ID,nodeStart.ID,nodeEnd.dist,path))

    def do_dijPath(self, arg):
        'calculates shortest overall path from node to all other nodes: dijkstraPath nodeID'
        if not arg:
            print("please refer to the help for command documentation")
            return None
        arglist = arg.split()
        if len(arglist) != 1:
            print("please refer to the help for command documentation")
            return None
        try:
            start = int(arg[0])
            nodeStart = self.nodes[start]
        except Exception as ex:  # one of the nodes is not in the nodeList
            return -1

        nodeList = list(self.nodes.values())
        nodeNameList = list(self.nodes.keys())

        for node in self.nodes.values():
            node.resetDistPrev()
        nodeStart.dist = 0
        nodeStart.prev = None

        while nodeList:
            currNode = takeSmallerDistanceNode(nodeList)#TODO change this to be a ordered array or something
            for edge in list(currNode.edges.values()):
                relative = edge.getRelative(currNode)
                if relative.dist > currNode.dist + 1:  # +1 for each edge
                    relative.dist = currNode.dist + 1
                    relative.prev = currNode

        for node in self.nodes.values():
            path = [node.ID]
            currNode = node.prev
            while currNode != None:
                path.insert(0, currNode.ID)
                currNode = currNode.prev
            print(
                "using node {} as a start we can get to node {} in {} jumps using path {}".format(nodeStart.ID, node.ID,
                                                                                                  node.dist, path))

    def dijkstraPathtoNode(self, start, end):
        try:
            nodeStart = self.nodes[start]
            nodeEnd = self.nodes[end]
        except Exception as ex:  # one of the nodes is not in the nodeList
            return -1

        nodeList = list(self.nodes.values())
        nodeNameList = list(self.nodes.keys())

        for node in self.nodes.values():
            node.resetDistPrev()
        nodeStart.dist = 0
        nodeStart.prev = None

        currNode = takeSmallerDistanceNode(nodeList)

        for edge in node.edges:
            relative = edge.getRel(currNode)
            if relative.dist > currNode.dist + 1:  # +1 for each edge
                relative.dist = currNode.dist + 1
                relative.prev = currNode
        if nodeEnd.prev == None:
            print("No path for that nodeEnd")
            return None

        path_taken = []
        path_taken.append(nodeEnd)
        pathNode = nodeEnd.prev
        jump_number = 1
        while pathNode != None:
            path_taken.insert(pathNode, 0)
            jump_number += 1
            pathNode = pathNode.prev
        return (pathNode, jump_number)


def takeSmallerDistanceNode(list):
    max = math.inf
    to_return = None

    for i, node in enumerate(list):
        if node.dist < max:
            max = node.dist
            to_return = node
    if to_return != None:
        list.remove(to_return)
    return to_return
def takeSmallerRelationshipNode(list):
    max = 0
    to_return = None

    for i, node in enumerate(list):
        if node.lastRelationship > max:
            max = node.lastRelationship
            to_return = node
    if to_return != None:
        list.remove(to_return)
    return to_return


"""
    def calculate(self):
        adverts= set(self.toAdvert)
        for node in self.stubs:
            if node is in adverts:# TODO
                neighbours = node.getNeighbours()                 #get neighbours from stubs
                neighbour_relationships = [node.sendDestinations(1),node.sendDestinations(2),node.sendDestinations(3)]#get advert lists
                for neighbour, relationship in neighbours.itens(): # for all neighbours
                    updated = neighbour.sendDestinations(neighbour_relationships[relationship])#if the neighbour updated its table
                    if updated:
                        if not (neighbour is in adverts):
                            toAdvert.insert(0,neighbour) #give list to neighbours and add them to the TOP of toAdvert if it comes back true
        for node in self.toAdvert
            #get neighbours
            #get nodeList
            #give nodeList
            #add back nodes to top of adverts if they return true
            #remove current node from the toAdvertList

"""


class Node(object):
    """docstring fo Node."""

    def __init__(self, ID):
        super(Node, self).__init__()
        self.edges = {}
        self.adverts = {}
        self.dist = math.inf
        self.prev = None
        self.ID = ID
        self.lastRelationship = 0

    def resetDistPrev(self):
        self.dist = math.inf
        self.prev = None
        self.lastRelationship = 0

    def _is_valid_operand(self, other):
        return (hasattr(other, "dist") and
                hasattr(other, "prev"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.ID == other.ID)

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.ID) < (other.ID)

    def addEdge(self, node, relationship):
        edge = Edge(self, node, relationship)
        self.edges[node.ID] = edge  # TODO update table and other nodes maybe?
        node.edges[self.ID] = edge

    def sendDestinations(self, relationship):
        to_send = []
        to_send.append(self)
        for dest, path in self.adverts.itens():
            if self.edges[path].getRel(self) == 1:
                to_send.append(dest)
            elif self.edges[path].getRel(self) == 2 and relationship != 2:
                to_send.append(dest)
        return to_send

    def getNeighbours(self):  # {neighbour1:relationship from this side}
        to_send = {}
        for dest, val in self.edges.itens():
            to_send[dest] = dest.getRel(self)
        return to_send

    def recieveDestinations(self, destDict):  # {path:(dest1,dest2,...),path2:(dest21,dest22,...)}
        altered = False
        for path, list in destDict.itens():  # for all the paths in the list
            rel = self.edges[path].getRel(
                self)  # keep a hold of the relationship between the first node on the path and this node
            for dest in list:  # for all the destinations going through the path node
                try:
                    oldPath = self.edges[self.adverts[dest]].getRel(
                        self)  # get the relationship of the last advertizment recieved for the destination

                    if (oldPath == 3 and rel < 3) or (
                            oldPath == 2 and rel == 1):  # if this new advert has a more favorable relationship keep it
                        self.adverts[dest] = path
                        altered = True
                except Exception as ex:  # TODO check no dictionary entry exception
                    self.adverts[dest] = path
                    altered = True
        return altered

    def isStub(self):
        for edge in self.edges:
            if edge.getRel() == 1:
                return False
        return True

    def isTop(self):
        for edge in self.edges:
            if edge.getRel() == 3:
                return False
        return True


class Edge(object):
    """docstring foredge."""

    def __init__(self, node1, node2, relationship):  # 1
        super(Edge, self).__init__()
        self.nodes = []
        self.nodes.append(node1)
        self.nodes.append(node2)
        if relationship < 4 and relationship > 0:
            self.relationship = relationship  # WARNING: DONT USE THIS VALUE, use getRel funtion instead

    def getRelative(self, selfnode):
        try:
            index = self.nodes.index(selfnode)
            if index == 0:
                return self.nodes[1]
            else:
                return self.nodes[0]
        except Exception as ex:
            print('something went wrong.Node ' + selfnode + 'tried to be in relationship ' + self.nodes[0] + '|' + self.nodes[0])

    def getRelationship(self, selfnode):
        try:
            index = self.nodes.index(selfnode)
            if index == 0:
                return self.relationship
            else:
                return invertRelationship(self.relationship)
        except Exception as ex:
            print('something went wrong.Node ' + selfnode + 'tried to be in relationship ' + self.nodes[1] + '|' + self.nodes[0])

    def getRel(self, selfnode):
        try:
            index = self.nodes.index(selfnode)
            if index == 0:
                return [self.nodes[1], self.relationship]
            else:
                return [self.nodes[0], invertRelationship(self.relationship)]
        except Exception as ex:
            print('something went wrong.Node ' + selfnode + 'tried to be in relationship ' + self.nodes[1] + '|' + self.nodes[0])


def invertRelationship(value):
    if value == 1:
        return 3
    elif value == 3:
        return 1
    else:
        return value


if __name__ == "__main__":
    grid = Grid()
    grid.cmdloop()
