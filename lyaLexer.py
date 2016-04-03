import tokenRules
import ply.lex as lex
import sys

# Build the lexer
lexer = lex.lex(module=tokenRules)

# read input file
with open(sys.argv[1], 'r') as myfile:
    data=myfile.read()

# Give the lexer read data
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
