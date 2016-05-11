import sys
from lyaParser import LyaParser

p = LyaParser()
if(len(sys.argv) > 2):
	tree = p.parse_file(sys.argv[1], int(sys.argv[2]))
elif(len(sys.argv) == 2):
	tree = p.parse_file(sys.argv[1])
else:
	tree = p.parse_file("examples/mTest.lya", 0)

print("")
print("")
print("--- TREE ---")
print("")
tree.show()
