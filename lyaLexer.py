import ply.lex as lex
import sys

# List of token name.

#-----------------------------#
#------ RESERVED WORDS -------#
#-----------------------------#

reserved = {
	# Reserved Words
	'array' : 'ARRAY',
	'by' : 'BY',
	'chars' : 'CHARS',
	'dcl' : 'DCL',
	'do' : 'DO',
	'down' : 'DOWN',
	'else' : 'ELSE',
	'elseif' : 'ELSIF',
	'end' : 'END',
	'exit' : 'EXIT',
	'fi' : 'FI',
	'for' : 'FOR',
	'if' : 'IF',
	'in' : 'IN',
	'loc' : 'LOC',
	'type' : 'TYPE',
	'od' : 'OD',
	'proc' : 'PROC',
	'ref' : 'REF',
	'result' : 'RESULT',
	'return' : 'RETURN',
	'returns' : 'RETURNS',
	'syn' : 'SYN',
	'then' : 'THEN',
	'to' : 'TO',
	'while' : 'WHILE',

	# Predefined words
	'bool' : 'BOOL',
	'char' : 'CHAR',
	'false' : 'FALSE',
	'int' : 'INT',
	'length' : 'LENGTH',
	'lower' : 'LOWER',
	'null' : 'NULL',
	'num' : 'NUM',
	'pred' : 'PRED',
	'print' : 'PRINT',
	'read' : 'READ',
	'succ' : 'SUCC',
	'true' : 'TRUE',
	'upper' : 'UPPER'
}

#---------------------#
#------ TOKENS -------#
#---------------------#
tokens = [

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
	'COMMENTLINE', 'COMMENT'
	
] + list(reserved.values())

#--------------------#
#------ RULES -------#
#--------------------#

t_COMMA = r','
t_SMC = r';'
t_COLON = r':'
t_PERIOD = r'\.'
t_LPAREN = r'\(' 
t_RPAREN = r'\)' 
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# TALVEZ TENHA QUE MUDAR O BRACES
# IMPLEMENTAR!!!
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

t_COMMENT = r'/\*.*\*/'
t_COMMENTLINE = r'\\\\'

def t_INTCONST(t):
    r'\d+'
    t.value = int(t.value)    
    return t
    
#def t_FLOATCONST(t):
#	r'\d+\.\d+'
#    t.value = float(t.value)
#    return t
    
t_STRINGCONST = r'\".+\"'
t_CHARCONST = r'\'.\''

def t_ID(t):
	r'[a-zA-z_][\w]*'
	t.type = reserved.get(t.value, 'ID')
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

#------------------------#
#------ READ FILE -------#
#------------------------#

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
