import sys
from lyaLexer import LyaLexer

lexer = LyaLexer()
lexer.listTokens(sys.argv[1])
