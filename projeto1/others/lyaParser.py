from ply import yacc
from lyaLexer import LyaLexer 
from aux.plyParser import PLYParser, Coord, ParseError
from aux.readFileHelper import FileHelper

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
		self.parse(self._readFile(filePath), filePath)
		
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
		'''program  : statement
					| statement statement'''
					
		
	def p_statement(self, p):
		'''statement : declaration_statement
					| comment
					| action_statement'''
					#| synonym_statement
					#| newmode_statement
					#| procedure_statement

	def p_declaration_statement(self, p):
		'''declaration_statement : DCL declaration_list SMC'''

	# cuidado com os espacos entre as virgulas
	def p_declaration_list(self, p):
		'''declaration_list : declaration
							| declaration COMMA declaration_list'''

	def p_declaration(self, p):
		'''declaration  : id_list mode'''

	def p_id_list(self, p):
		'''id_list  : ID
					| id_list COMMA ID'''

	def p_mode (self, p):
		'''mode : ID
				| discrete_mode'''
        
	def p_discrete_mode (self, p):
		'''discrete_mode : INT
						| BOOL
						| CHAR'''
#### Funcionando ate aqui

#	def p_initialization (self, p) :
#		'''initialization : EQUAL INTCONST SMC'''

	def p_action_statement (self, p):
		'''action_statement : action
							| ID COLON action '''

	def p_action (self, p):
		'''action 	: assignment_action'''
#					| bracketed_action
#					| call_action
#					| exit_action
#					| return_action
#					| result_action  '''

	def p_assignment_action (self, p):
		'''assignment_action : location assigning_operator expression '''

	def p_assigning_operator (self, p):
		'''assigning_operator 	: EQUALS
							| closed_dyadic_operator EQUALS '''

	def p_closed_dyadic_operator (self, p):
		'''closed_dyadic_operator 	: arithmetic_additive_operator
									| arithmetic_multiplicative_operator
									| STRCONC '''

	def p_expression (self, p):
		'''expression 	: operand0'''

	def p_operand0 (self, p):
		'''operand0 : operand1
					| operand0 operator1 operand1 '''

	def p_operator1 (self, p):
		'''operator1 	: relational_operator
						| IN'''

	def p_relational_operator (self, p):
		'''relational_operator 	: AND
								| OR
								| ISEQUAL
								| NOTEQUAL
								| GT
								| GE
								| LT
								| LE'''

	def p_operand1 (self, p):
		'''operand1 : operand2
					| operand1 operator2 operand2 '''

	def p_operator2 (self, p):
		'''operator2 	: arithmetic_additive_operator
						| STRCONC'''

	def p_arithmetic_additive_operator (self, p):
		'''arithmetic_additive_operator : PLUS
										| MINUS '''

	def p_operand2 (self, p):
		'''operand2 : operand3
					| operand2 arithmetic_multiplicative_operator operand3 '''

	def p_arithmetic_multiplicative_operator (self, p):
		'''arithmetic_multiplicative_operator 	: TIMES
												| DIV
												| MOD'''

	def p_operand3 (self, p):
		'''operand3 : operand4
					| monadic_operator operand4
					| INTCONST '''

	def p_monadic_operator (self, p):
		'''monadic_operator : MINUS
							| NOT'''

	def p_operand4 (self, p):
		'''operand4 : primitive_value
					| location 
					| referenced_location'''


	def p_referenced_location (self, p):
		'''referenced_location : ARROW location '''

	def p_location (self, p):
		'''location : ID'''

	def p_primitive_value (self, p):
		'''primitive_value  : literal'''

	def p_literal (self, p):
		'''literal  : INTCONST
					| boolean_literal
					| CHARCONST
					| NULL
					| STRINGCONST'''

	def p_boolean_literal (self, p):
		'''boolean_literal  : FALSE
							| TRUE'''

#### Comments
	def p_comment (self, p):
		'''comment 	: bracketed_comment
					| line_end_comment '''

	def p_bracketed_comment (self, p):
		'''bracketed_comment : COMMENT'''

	def p_line_end_comment (self, p):
		'''line_end_comment : COMMENTLINE'''
