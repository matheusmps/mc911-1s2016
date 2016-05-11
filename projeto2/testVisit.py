import sys
from nodeVisitor import NodeVisitor
from lyaParser import LyaParser

p = LyaParser()
if(len(sys.argv) == 3):
	tree = p.parse_file(sys.argv[1], int(sys.argv[2]))
else:
	tree = p.parse_file(sys.argv[1], 0)

visitor = NodeVisitor()
visitor.visit(tree)
