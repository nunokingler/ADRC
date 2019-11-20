import matpy
class Grid(object):
    """docstring for Grid."""

    def __init__(self, arg):
        super(Grid, self).__init__()
        self.nodes = {}
        self.stubs = []
        self.tops  = []
        self.toAdvert = []

    def addRelationship(self, nodeID1,nodeID2,relationship):
        ncreated=False
        if relationship==3: //
            nodeaux=nodeID1
            nodeID1=nodeID2
            nodeID2=nodeaux
            relationship=invertRelationship(relationship)
        try:
            node1=self.nodes[nodeID1]
            node1_was_stub= node1.isStub()
            node1_was_top = node1.isTop()
        except:
            node1=node()
            node1_was_stub= False
            node1_was_top = False
        try:
            node2=self.nodes[nodeID2]
            node2_was_stub= node2.isStub()
            node2_was_top = node2.isTop()
        except:
            node2=node()
            node2_was_stub= False
            node2_was_top = False

        node1.addEdge(node2,relationship)

        if node1_was_top!= node1.isTop():
            if node1_was_top == 1:
                self.tops.remove(node1)
            else:
                self.tops.add(node1)

        if node1_was_stub!= node1.isStub():
            if node1_was_stub == 1:
                self.stubs.remove(node1)
            else:
                self.stubs.add(node1)

        if node2_was_top!= node2.isTop():
            if node2_was_top == 1:
                self.tops.remove(node2)
            else:
                self.tops.add(node2)

        if node2_was_stub!= node2.isStub():
            if node2_was_stub == 1:
                self.stubs.remove(node2)
            else:
                self.stubs.add(node2)

        self.toAdvert.append(node1)
        self.toAdvert.append(node2)


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



class Node(object):
    """docstring fo Node."""

    def __init__(self):
        super(Node, self).__init__()
        self.edges = {}
        self.adverts={}

    def addEdge(self, node,relationship):
            edge=edge(self,node,relationship)
            self.edges[node]=edge#TODO update table and other nodes maybe?
            node.edges[self]=edge

    def sendDestinations(self, relationship):
        to_send=[]
        to_send.append(self)
        for dest,path in self.adverts.itens():
            if self.edges[path].getRel(self) == 1:
                to_send.append(dest)
            elif self.edges[path].getRel(self)==2 and relationship !=2
                to_send.append(dest)
        return to_send

    def getNeighbours(self):#{neighbour1:relationship from this side}
            to_send = {}
            for dest, val in self.edges.itens():
                to_send[dest]= dest.getRel(self)
            return to_send

    def recieveDestinations(self,destDict):#{path:(dest1,dest2,...),path2:(dest21,dest22,...)}
        altered = False
        for path, list in destDict.itens(): #for all the paths in the list
            rel=self.edges[path].getRel(self)   #keep a hold of the relationship between the first node on the path and this node
            for dest in list:               #for all the destinations going through the path node
                try:
                    oldPath=self.edges[self.adverts[dest]].getRel(self) #get the relationship of the last advertizment recieved for the destination

                    if (oldPath==3 and rel<3) or (oldPath==2 and rel==1):# if this new advert has a more favorable relationship keep it
                        self.adverts[dest]= path
                        altered=True
                except Exception as ex:#TODO check no dictionary entry exception
                        self.adverts[dest]= path
                        altered=True
        return altered

    def isStub(self):
        for edge in self.edges:
            if edge.getRel()==1:
                return False
        return True

    def isTop(self):
        for edge in self.edges:
            if edge.getRel()==3:
                return False
        return True


class edge(object):
    """docstring foredge."""

    def __init__(self, node1, node2, relationship):#1
        super(edge, self).__init__()
        self.nodes = []
        self.nodes.append(node1)
        self.nodes.append(node2)
        if relationship<4 and relationship>0:
            self.relationship=relationship # WARNING: DONT USE THIS VALUE, use getRel funtion instead

    def getRel(self,selfnode):
        try:
            index = self.nodes.index(selfnode)
            if index==0
                return [self.nodes[1],self.relationship]
            else:
                return [self.nodes[0],invertRelationship(self.relationship)]
        except Exception as ex:
            print('something went wrong.Node '+selfnode+'tried to be in relationship '+node1+'|'+node2)


def invertRelationship(value):
    if value ==1:
        return 3
    elif value==3:
        return 1
    else:
        return value
