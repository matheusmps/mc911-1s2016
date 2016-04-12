import sys
from lyaParser import LyaParser

parser = LyaParser()
parser.testLexer(sys.argv[1])
