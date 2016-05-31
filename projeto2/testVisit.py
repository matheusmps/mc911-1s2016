import sys
from nodeVisitor import Visitor
from lyaParser import LyaParser

p = LyaParser()
if(len(sys.argv) == 3):
	tree = p.parse_file(sys.argv[1], int(sys.argv[2]))
else:
	tree = p.parse_file(sys.argv[1], 0)

print("")
print("--- TREE ---")
print("")
tree.show()

print("")
print("--- SEMANTIC ---")
print("")
visitor = Visitor()
visitor.visit(tree)
