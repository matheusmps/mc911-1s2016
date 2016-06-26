import sys
from nodeVisitor import Visitor
from lyaParser import LyaParser
from genCode import CodeGenerator

p = LyaParser()
if(len(sys.argv) == 2):
	tree = p.parse_file(sys.argv[1], 0)
else:
	tree = p.parse_file("examples/mTest.lya", 0)

print("")
print("--- TREE ---")
print("")
tree.show()

print("")
print("--- SEMANTIC ---")
print("")
visitor = Visitor()
visitor.visit(tree)

print("")
print("--- GEN CODE ---")
print("")
codeGen = CodeGenerator()
codeGen.visit(tree)
codeGen.printInstructions()

