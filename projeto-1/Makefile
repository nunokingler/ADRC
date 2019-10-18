GROUPNUMBER = 1337

PKGFILES = \
	Main.py\
	Makefile\
	PrefixTree.py\
	Tree.py\
	res

clean:
	$(RM) *.zip

dist:
	mkdir p1.${GROUPNUMBER}
	cp -r ${PKGFILES} p1.${GROUPNUMBER}
	zip -r p1.${GROUPNUMBER}.zip p1.${GROUPNUMBER}
	$(RM) -r p1.${GROUPNUMBER}

.PHONY: clean dist
