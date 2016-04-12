import sys
from parser import LyaParser

parser = LyaParser()
parser.testLexer(sys.argv[1])
