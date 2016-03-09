import ply.lex as lex
import sys

# List of token name.

##################
### KEYWORKDS ####
##################

keywords = (
	# Reserved Words
	'ARRAY', 'BY', 'CHARS', 'DCL', 'DO', 'DOWN', 'ELSE', 'ELSIF', 'END', 'EXIT', 'FI', 'FOR', 'IF', 'IN', 
	'LOC', 'TYPE', 'OD', 'PROC', 'REF', 'RESULT', 'RETURN', 'RETURNS', 'SYN', 'THEN', 'TO', 'WHILE',

	# Predefined words
	'BOOL', 'CHAR', 'FALSE', 'INT', 'LENGTH', 'LOWER', 'NULL', 'NUM','PRED', 'PRINT', 'READ', 'SUCC', 'TRUE', 'UPPER'
)

# Defined tokens
tokens = keywords + (

	# DELIMETERS
	'COMMA', 'SMC', 'COLON', 'LPAREN', 'RPAREN', 'EQUAL', 

	# ASSIGNEMENT
	'PEQUAL', 'TEQUAL', 'MEQUAL', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
	
	# RELATIONAL
	'ISEQUAL', 'GTHAN', 'LTHAN', 'GETHAN', 'LETHAN', 'NUMBER'

)

##############
### RULES ####
##############

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

########################
### READ INPUT FILE ####
########################

# Build the lexer
lexer = lex.lex()

# open file
with open(sys.argv[1], 'r') as myfile:
    data=myfile.read()

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
