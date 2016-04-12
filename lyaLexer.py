import ply.lex as lex
import sys

class LyaLexer(object):
	def __init__(self, lBraceFunc, rBraceFunc):
		self.last_token = None
		self.lBraceFunc = lBraceFunc
		self.rBraceFunc = rBraceFunc

	def reset(self):
		self.lexer.lineno = 1
		self.last_token = None
	
	def build(self, **kwargs):
		self.lexer = lex.lex(object=self, **kwargs)
		
	def input(self, text):
		self.lexer.input(text)
		
	def token(self):
		self.last_token = self.lexer.token()
		return self.last_token
		
	def listTokens(self, filePath):
		""" Used only for tests. """
		self.input(self._readFile(filePath))
		while True:
			tok = self.token()
			if not tok: 
				break      # No more input
			print(tok)
	
	### PRIVATE ###
	
	def _readFile(self, filePath):
		with open(filePath, 'r') as myFile:
			data = myFile.read()
		return data

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

		'INTCONST', 'STRINGCONST', 'CHARCONST',

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
		'COMMENTLINE', 'COMMENT', 'STRCONC', 'ARROW'
		
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

	def t_LBRACE(self, t):
		r'\{'
		self.lBraceFunc()
		return t
		
	def t_RBRACE(self, t):
		r'\}'
		self.rBraceFunc()
		return t

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
	t_MOD 	  = r'%'

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

	t_STRCONC = r'&'
	t_ARROW = r'->'

	def t_INTCONST(self, t):
		r'\d+'
		t.value = int(t.value)    
		return t
		
	t_STRINGCONST = r'\".+\"'
	t_CHARCONST = r'\'.\''

	# This code handles reserved words as well
	# It reduces an expression to this rule and try to look for a reserved word.
	def t_ID(self, t):
		r'[a-zA-z_][\w]*'
		
		# Check for reserved words
		# 'ID' is the default value if it does not find t.value in the reserved words list.
		t.type = self.reserved.get(t.value, 'ID') 
		return t

	# Define a rule so we can track line numbers
	def t_newline(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	# A string containing ignored characters (spaces and tabs)
	t_ignore  = ' \t'

	# Error handling rule
	def t_error(self, t):
		print("Illegal character '%s'" % t.value[0])
		t.lexer.skip(1)

