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

	'ID',
	
	'INTCONST', 'FLOATCONST', 'STRINGCONST', 'CHARCONST',

	# DELIMETERS
	'COMMA', 'SMC', 'COLON', 'PERIOD',
	'LPAREN', 'RPAREN', 
	'LBRACKET', 'RBRACKET',
	'LBRACE', 'RBRACE',

	# ASSIGNEMENT
	'EQUALS', 'PLUSEQ', 'TIMESEQ', 'MINUSEQ', 'DIVEQ', 'MODEQ',
	
	# OPERATOR
	'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD',
	
	# RELATIONAL
	'NOTEQUAL', 'ISEQUAL', 'GT', 'GE', 'LT', 'LE', 
	'AND', 'OR', 'NOT',
	
	# INCREMENT/DECREMENT
	'PLUSPLUS', 'MINUSMINUS',
	
	# OTHER
	'COMMENTLINE', 'COMMENTDELIMETER'

)

##############
### RULES ####
##############

# KEYWORDS
t_ARRAY = r'array'
t_BY = r'by'
t_CHARS = r'chars'
t_DCL = r'dcl'
t_DO = r'do'
t_DOWN = r'down'
t_ELSE = r'else'
t_ELSIF = r'elsif'
t_END = r'end'
t_EXIT = r'exit'
t_FI = r'fi'
t_FOR = r'for'
t_IF = r'if'
t_IN = r'in'
t_LOC = r'loc'
t_TYPE = r'type'
t_OD = r'od'
t_PROC = r'proc'
t_REF = r'ref'
t_RESULT = r'result'
t_RETURN = r'return'
t_RETURNS = r'returns'
t_SYN = r'syn'
t_THEN = r'then'
t_TO = r'to'
t_WHILE = r'while'
t_BOOL = r'bool'
t_CHAR = r'char'
t_FALSE = r'false'
t_INT = r'int'
t_LENGTH = r'lenght'
t_LOWER = r'lower'
t_NULL = r'null'
t_NUM = r'num' 
t_PRED = r'pred'
t_PRINT = r'print'
t_READ = r'read'
t_SUCC = r'succ'
t_TRUE = r'true'
t_UPPER = r'upper'

#  IMPLEMENT !!!!!!!

#t_ID = r''

def t_INTCONST(t):
    r'\d+'
    t.value = int(t.value)    
    return t

#t_FLOATCONST= r''
#t_STRINGCONST= r''
#t_CHARCONST= r''

t_COMMA = r','
t_SMC = r';'
t_COLON = r':'
t_PERIOD = r'\.'
t_LPAREN = r'\(' 
t_RPAREN = r'\)' 
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# TALVEZ TENHA QUE MUDAR O BRACES
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_EQUALS = r'='
t_PLUSEQ = r'\+='
t_TIMESEQ = r'\*='
t_MINUSEQ = r'-='
t_DIVEQ = r'/='
t_MODEQ = r'%='

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIV     = r'/'

t_NOTEQUAL = r'!='
t_ISEQUAL = r'=='
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'	

#t_COMMENT = r''
t_COMMENTLINE = r'\\\\'

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
