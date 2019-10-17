#import Tree
import PrefixTree
#aggregacao e filtragem

tree = PrefixTree.Tree(1)
counter=0
with  open('ex.txt', 'r') as file:
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
print("previous size {}".format(len(dict)))
"""
if dict!=None:
    for key,node in dict.items():
        if key!="":
            print ("{} : {}".format(key,node))
        else:
            print("e : {}".format(node))"""
print('compressing')
dict=tree.compressTree().printTable()
print("new size {}".format(len(dict)))
"""
if dict!=None:
    for key,node in dict.items():
        if key!="":
            print ("{} : {}".format(key,node))
        else:
            print("e : {}".format(node))"""