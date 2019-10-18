import Tree

tree = Tree.Tree(1)
counter=0
ui=Tree.TreeUi(tree)

while True:
    try:
        to_print=ui.command(input('Input your command'))
        if isinstance(to_print, str):
            print(to_print)
        else:
            if isinstance(to_print,Tree.Tree):
                to_print=to_print.printTable()
            for key,node in to_print.items():
                if key != "":
                    print("{} : {}".format(key, node))
                else:
                    print("e : {}".format(node))
            print("table has {} entries".format(len(to_print)))

    except Tree.NoSuchCommand as noComm:
        print("Commands:")
        for commands in noComm.args:
            print(commands)
    except Tree.InvalidSyntax as invalid:
        print( invalid.argsx)
