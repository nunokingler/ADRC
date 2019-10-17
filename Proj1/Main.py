import Tree
#aggregacao e filtragem

tree = Tree.Tree(1)
counter=0
with  open('PrefixTableTest.txt', 'r') as file:
    line = file.readline()
    while line:
        counter+=1
        print("adding line {}".format(counter))
        parts= line.split()
        if len(parts)==2:
            tree.addNode(parts[0], int(parts[1]))
        line = file.readline()


#tree.printTree()
dict=tree.printTable()
if dict!=None:
    for key,node in dict.items():
        if key!="":
            print ("{} : {}".format(key,node))
        else:
            print("e : {}".format(node))
tree.compressTree()