import sys
from lyaParser import LyaParser

p = LyaParser()
p.parse_file(sys.argv[1])