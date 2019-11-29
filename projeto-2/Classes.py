import math
import os
import cmd
import avl


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
        print("type 'help' for help!")

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

    def do_3tables(self, arg):
        'calculates commercial path to every node'
        if not arg:
            print("please refer to the help for command documentation")
            return None
        arglist = arg.split()
        if len(arglist) != 1:
            print("wrong argument number, please refer to the help for command documentation")
            return None
        try:
            start = int(arglist[0])
            nodeStart = self.nodes[start]
        except Exception as ex:  # one of the nodes is not in the nodeList
            print("node does not exist or node is not integer")
            return None

        Q1 = []
        Q2 = []
        Q3 = []
        for node in self.nodes.values():
            node.resetDistPrev()
        nodeStart.n_next_hops = 0
        nodeStart.prev = None
        nodeStart.lastRelationship = 4
        nodeStart.is_in_collection = 1

        nodeStartDest = Dest(nodeStart.ID)
        nodeStartDest.n_next_hops = 0
        dest_list = {}
        # insert_node_ordered_array(nodeList,nodeStart)
        # nodeList.insert(nodeStart.dist, nodeStart)
        Q1.append(nodeStartDest)
        dest_list[nodeStart.ID] = (nodeStartDest,None)
        reached = False

        while Q1 or Q2 or Q3:

            if Q1:
                current_nodeDest = Q1[0]
                Q1.remove(current_nodeDest)
            elif Q2:
                current_nodeDest = Q2[0]
                Q2.remove(current_nodeDest)
            else:
                current_nodeDest = Q3[0]
                Q3.remove(current_nodeDest)

            current_node = self.nodes[current_nodeDest.ID]


            for edge in list(current_node.edges.values()):
                relative = edge.getRelative(current_node)
                new_path = edge.getRelationship(relative)
                if relative.n_next_hops > current_node.n_next_hops + 1:
                    if current_node.is_in_collection == 1:
                        created = False
                        if relative.is_in_collection == -1:
                            relative.is_in_collection = 1
                            destination = Dest(relative.ID)
                            created = True
                        else:
                            destination = dest_list[relative.ID][0]
                        changed = False

                        if new_path == 1:
                            Q1.append(destination)
                            relative.is_in_collection = 1
                            changed = True
                        elif current_node.n_next_hops == 0 and new_path == 2:
                            Q2.append(destination)
                            relative.is_in_collection = 2
                            changed = True
                        elif current_node.n_next_hops == 0 and new_path == 3:
                            Q3.append(destination)
                            relative.is_in_collection = 3
                            changed = True

                        if changed:
                            destination.path = list(current_nodeDest.path)
                            destination.path.append(current_node.ID)
                            destination.n_next_hops = current_nodeDest.n_next_hops + 1
                            relative.n_next_hops = current_node.n_next_hops + 1
                            dest_list[relative.ID] = (destination, None)
                        elif created:
                            relative.is_in_collection=-1

                    elif current_node.is_in_collection == 2:
                        if relative.n_next_hops > current_node.n_next_hops + 1:
                            created = False
                            if relative.is_in_collection == -1:
                                relative.is_in_collection = 1
                                destination = Dest(relative.ID)
                                created = True
                            else:
                                destination = dest_list[relative.ID][1]

                            if new_path == 1:
                                Q2.append(relative)
                                relative.is_in_collection = 2
                                destination.path = list(current_nodeDest.path)
                                destination.path.append(current_node.ID)
                                destination.n_next_hops = current_nodeDest.n_next_hops + 1
                                relative.n_next_hops = current_node.n_next_hops + 1
                                if not created:
                                    dest_list[relative.ID] = (dest_list[relative.ID][0], destination)
                                else:
                                    dest_list[relative.ID] = (None, destination)
                            elif created:
                                relative.is_in_collection = -1
                    else:
                        if relative.n_next_hops > current_node.n_next_hops + 1:
                            created= False
                            if relative.is_in_collection == -1:
                                relative.is_in_collection = 1
                                destination = Dest(relative.ID)
                                created = True
                            else:
                                destination = dest_list[relative.ID][1]

                            changed = False
                            if new_path == 1:
                                Q3.append(destination)
                                relative.is_in_collection = 3
                                destination.has_peak = True
                                changed = True
                            elif new_path == 2 and not destination.has_peak:
                                Q3.append(destination)
                                relative.is_in_collection = 3
                                destination.has_peak = True
                                changed = True
                            elif new_path == 3 and not destination.has_peak:
                                Q3.append(destination)
                                relative.is_in_collection = 3
                                changed = True

                            if changed:
                                destination.path = list(current_nodeDest.path)
                                destination.path.append(current_node.ID)
                                destination.n_next_hops = current_nodeDest.n_next_hops + 1
                                relative.n_next_hops = current_node.n_next_hops + 1
                                if not created:
                                    dest_list[relative.ID] = (dest_list[relative.ID][0], destination)
                                else:
                                    dest_list[relative.ID] = (None, destination)
                            elif created:
                                relative.is_in_collection= -1
        for dest in dest_list.values():
            if dest[0] and dest[1]:
                print("found coomercial path from {} to {} with {} jumps |{}| shortest {} |{}|".format(nodeStart.ID, dest[0].ID, dest[0].n_next_hops, dest[0].path, dest[1].n_next_hops, dest[1].path))
            elif dest[0]:
                print("found coomercial path from {} to {} with {} jumps |{}|".format(nodeStart.ID, dest[0].ID, dest[0].n_next_hops, dest[0].path))
            elif dest[1]:
                print("found coomercial path from {} to {} with {} jumps |{}|".format(nodeStart.ID, dest[1].ID, dest[1].n_next_hops, dest[1].path))

            else:
                print("uh oh")

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
        # nodeList = list(self.nodes.values()) OLD NODELIST
        # nodeList = []
        nodeList = avl.AVL()
        for node in self.nodes.values():
            node.resetDistPrev()
        nodeStart.dist = 0
        nodeStart.prev = None
        nodeStart.lastRelationship = 4
        nodeStart.is_in_collection = 1
        # insert_node_ordered_array(nodeList,nodeStart)
        nodeList.insert(nodeStart.dist, nodeStart)
        reached = False

        while nodeList and not reached:
            min = nodeList.find_minimum()  # currNode = take_smallest(nodeList)#takeSmallerRelationshipNode(nodeList)#TODO change this to be a ordered array or something
            min = nodeList.find_minimum()
            min = nodeList.find_minimum()

            currNode = nodeList.delete(min.key, min.value)
            currNode.is_in_collection = False
            if reached and currNode.lastRelationship >= nodeEnd.lastRelationship:
                break
            for edge in list(currNode.edges.values()):
                relative = edge.getRelative(currNode)
                if currNode.lastRelationship == 1 or currNode.lastRelationship == 4:
                    if relative.n_next_hops > currNode.n_next_hops + 1:  # +1 for each edge
                        relative.n_next_hops = currNode.n_next_hops + 1
                        relative.prev = currNode
                        relative.lastRelationship = edge.getRelationship(relative)
                        if relative.is_in_collection:
                            nodeList.delete(relative.n_next_hops, relative)
                        nodeList.insert(relative.n_next_hops, relative)
                        relative.is_in_collection = True
                elif currNode.lastRelationship == 2:
                    if (
                            relative.lastRelationship == 2 or relative.lastRelationship == 0) and relative.n_next_hops > currNode.n_next_hops + 1 and edge.getRelationship(
                            currNode) != 2:
                        relative.n_next_hops = currNode.n_next_hops + 1
                        relative.prev = currNode
                        relative.lastRelationship = 2
                        if relative.is_in_collection:
                            nodeList.delete(relative.n_next_hops, relative)
                        nodeList.insert(relative.n_next_hops, relative)
                        relative.is_in_collection = True
                elif currNode.lastRelationship == 3:
                    if edge.getRelationship(
                            currNode) == 1 and relative.n_next_hops > currNode.n_next_hops + 1:  # if current node is provider
                        relative.n_next_hops = currNode.n_next_hops + 1
                        relative.prev = currNode
                        relative.lastRelationship = edge.getRelationship(relative)
                        if relative.is_in_collection:
                            nodeList.delete(relative.n_next_hops, relative)
                        nodeList.insert(relative.n_next_hops, relative)
                        relative.is_in_collection = True

                if relative.ID == nodeEnd.ID and not math.isinf(relative.n_next_hops):
                    reached = True
        if reached:
            path = [nodeEnd.ID]
            currNode = nodeEnd.prev
            connectioninfo = [0, 0, 0]  # provider->client, equal, client->provider
            lastNode = nodeEnd
            while currNode != None:
                path.insert(0, currNode.ID)
                usedEdge = currNode.getEdge(lastNode)
                connectioninfo[usedEdge.getRelationship(currNode) - 1] += 1  # TODO add connection statistics
                lastNode = currNode
                currNode = currNode.prev
            print("reached node {} from {} with {} jumps using path {} ,jumps (p->c,p->p,c->p){}".format(nodeEnd.ID,
                                                                                                         nodeStart.ID,
                                                                                                         nodeEnd.n_next_hops,
                                                                                                         path,
                                                                                                         connectioninfo))
            return

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
            currNode = takeSmallerDistanceNode(nodeList)  # TODO change this to be a ordered array or something
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


class Dest(object):
    def __init__(self, ID):
        self.path = []
        self.ID = ID
        self.n_next_hops = math.inf
        self.has_peak = False

    def reset(self):
        self.path = []
        self.n_next_hops = math.inf
        self.has_peak = False


class Node(object):
    """docstring fo Node."""

    def __init__(self, ID):
        super(Node, self).__init__()
        self.edges = {}
        self.adverts = {}
        self.n_next_hops = math.inf
        self.prev = None
        self.ID = ID
        self.path_type = 0
        self.is_in_collection = -1
        self.path = []
        self.has_peaked = False
        self.next = None

    def resetDistPrev(self):
        self.n_next_hops = math.inf
        self.prev = None
        self.path_type = 0
        self.is_in_collection = -1
        self.path = []
        self.has_peaked = False

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

    def getEdge(self, otherNode):
        try:
            edge = self.edges[otherNode.ID]
        except Exception as ex:
            return None
        return edge

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
            print('something went wrong.Node ' + selfnode + 'tried to be in relationship ' + self.nodes[0] + '|' +
                  self.nodes[0])

    def getRelationship(self, selfnode):
        try:
            index = self.nodes.index(selfnode)
            if index == 0:
                return self.relationship
            else:
                return invertRelationship(self.relationship)
        except Exception as ex:
            print('something went wrong.Node ' + selfnode + 'tried to be in relationship ' + self.nodes[1] + '|' +
                  self.nodes[0])

    def getRel(self, selfnode):
        try:
            index = self.nodes.index(selfnode)
            if index == 0:
                return [self.nodes[1], self.relationship]
            else:
                return [self.nodes[0], invertRelationship(self.relationship)]
        except Exception as ex:
            print('something went wrong.Node ' + selfnode + 'tried to be in relationship ' + self.nodes[1] + '|' +
                  self.nodes[0])


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
