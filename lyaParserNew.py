from ply import yacc
from lyaLexer import LyaLexer 
from aux.plyParser import PLYParser, Coord, ParseError
from aux.readFileHelper import FileHelper
import aux.ast as ast

class LyaParser(PLYParser):
	
	def __init__(self):
		self.lexer = LyaLexer(
			error_func=self._lex_error,
			lBraceFunc=self._lex_onLeftBrace, 
			rBraceFunc=self._lex_onRightBrace)
		
		self.lexer.build()
		self.tokens = self.lexer.tokens
		self.parser = yacc.yacc(module=self, start='program')
		
		# Stack of scopes for keeping track of symbols. 
		# _scope_stack[-1] is the current (topmost) scope.  
		# If _scope_stack[n][name] is True, 'name' is currently a symbol in the scope.
		# Otherwise 'name' is not used in this scope at all.
		self._scope_stack = [dict()]
		
		
	def initParser(self):
		self._scope_stack = [dict()]
		
	def parse_file(self, filePath):
		return self.parse(self._readFile(filePath), filePath, 1)
		
	def parse(self, text, filename='', debuglevel=0):
		self.lexer.reset(filename)
		self.initParser()
		return self.parser.parse(
			input=text,
			lexer=self.lexer,
			debug=debuglevel)
			
	def testLexer(self, filePath):
		self.lexer.filename = filePath
		self.lexer.listTokens(self._readFile(filePath))
		
	######################--   PRIVATE   --######################
	
	def _readFile(self, filePath):
		return FileHelper(filePath).readFile()
	
	## SCOPE IS REALLY NECESSARY??? 
	## IN THE EXAMPLE IS USED BECAUSE OF TYPEDEF
	
	def _spope_push(self):
		self._scope_stack.append(dict())
		
	def _scope_pop(self):
		assert len(self._scope_stack) > 1
		self._scope_stack.pop()
		
	def _lex_error(self, msg, line, column):
		self._parse_error(msg, self._coord(line, column))
		
	def _lex_onLeftBrace(self):
		#print("lbrace")
		self._spope_push()
	
	def _lex_onRightBrace(self):
		#print("rbrace")
		self._scope_pop()
		
	def _add_identifier(self, name, coord):
		self._scope_stack[-1][name] = True

	def _get_yacc_lookahead_token(self):
		return self.lexer.last_token

	######################--   RULES  --######################
	
	def p_program(self, p): 
		'''program  : statement_list
					| empty'''
		if p[1] is None:
			p[0] = ast.Program([])
		else:
			p[0] = ast.Program(p[1])
	
	def p_statement_list1(self, p):
		'''statement_list : statement'''
		p[0] = [p[1]]

	def p_statement_list2(self, p):
		'''statement_list : statement_list statement'''
		p[0] = p[1] + [p[2]]
		
	def p_statement(self, p):
		'''statement : declaration_statement'''
					#| action_statement
					#| synonym_statement
					#| newmode_statement
					#| procedure_statement
		p[0] = p[1]
	
	def p_declaration_statement(self, p):
		'''declaration_statement : DCL declaration_list SMC'''
		p[0] = ast.DeclStmt(p[2])

	# cuidado com os espacos entre as virgulas
	def p_declaration_list(self, p):
		'''declaration_list : declaration
							| declaration_list COMMA declaration'''
		if(len(p) == 4):
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1]]
		
	def p_declaration2(self, p):
		'''declaration : id_list mode initialization'''
		p[0] = ast.Declaration(p[1], p[2], p[3])

	def p_declaration1(self, p):
		'''declaration : id_list mode '''
		p[0] = ast.Declaration(p[1], p[2], None)

	def p_id_list(self, p):
		'''id_list  : ID
					| id_list COMMA ID'''
		if(len(p) == 4):
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1]]
	
	def p_mode(self, p):
		'''mode : INT
				| BOOL
				| CHAR'''
		p[0] = p[1]
	
	def p_mode_name(self, p):
		'''mode_name : ID'''
		p[0] = p[1]
        
	def p_discrete_mode(self, p):
		'''discrete_mode : INT
						 | BOOL
						 | CHAR'''
		p[0] = p[1]
						 
	def p_initialization(self, p):
		'''initialization : EQUALS INTCONST'''
		p[0] = p[2]
	
	### Others
	
	def p_empty(self, p):
		'empty : '
		p[0] = None
