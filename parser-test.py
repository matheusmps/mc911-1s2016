import sys
from lyaParserNew import LyaParser

p = LyaParser()
tree = p.parse_file(sys.argv[1])

print()
print()
print()
tree.show()