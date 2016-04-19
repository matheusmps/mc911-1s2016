import sys
from maraLyaParser import LyaParser

p = LyaParser()
if(len(sys.argv) > 2):
	tree = p.parse_file(sys.argv[1], int(sys.argv[2]))
elif(len(sys.argv) == 2):
	tree = p.parse_file(sys.argv[1])
else:
	tree = p.parse_file("tests/mTest.lya", 1)

print("")
print("")
print("--- TREE ---")
print("")
tree.show()
