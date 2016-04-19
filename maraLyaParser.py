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
		
	def parse_file(self, filePath, debuglevel=0):
		return self.parse(
			self._readFile(filePath), 
			filename=filePath, 
			debuglevel=debuglevel)
		
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
	
	##################################
	##### PROGRAM AND STATEMENTS #####
	##################################
	
	def p_program(self, p): 
		'''program  : statement_list
					| empty'''
		if p[1] is None:
			p[0] = ast.Program([])
		else:
			p[0] = ast.Program(p[1])
	
	def p_statement_list1(self, p):
		'''statement_list : statement
						  | statement_list statement'''
		if(len(p) == 3):
			p[0] = p[1] + [p[2]]
		else:
			p[0] = [ p[1] ]

	def p_statement(self, p):
		'''statement : declaration_statement
					| newmode_statement
					| synonym_statement'''
					#| action_statement
					#| procedure_statement
		p[0] = p[1]
	
	#######################
	##### DECLARATION #####
	#######################
	
	def p_declaration_statement(self, p):
		'''declaration_statement : DCL declaration_list SMC'''
		p[0] = ast.DeclStmt(p[2])

	def p_declaration_list(self, p):
		'''declaration_list : declaration
							| declaration_list COMMA declaration'''
		if(len(p) == 4):
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1]]
		
	def p_declaration1(self, p):
		'''declaration : id_list mode initialization'''
		p[0] = ast.Declaration(p[1], p[2], p[3])

	def p_declaration2(self, p):
		'''declaration : id_list mode '''
		p[0] = ast.Declaration(p[1], p[2], None)

	def p_id_list(self, p):
		'''id_list  : ID
					| id_list COMMA ID'''
		if(len(p) == 4):
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1]]
			
	################
	##### MODE #####
	################
	
	def p_mode(self, p):
		'''mode : mode_name
				| discrete_mode
				| reference_mode
				| composite_mode'''
		p[0] = p[1]
	
	def p_mode_name(self, p):
		'''mode_name : ID'''
		p[0] = ast.Mode(p[1])
		
	def p_discrete_mode(self, p):
		'''discrete_mode : basic_mode
						 | discrete_range_mode'''
		p[0] = p[1]
        
	def p_basic_mode(self, p):
		'''basic_mode : INT
					  | BOOL
					  | CHAR'''
		p[0] = ast.DiscreteMode(p[1])
		
	def p_discrete_range_mode(self, p):
		'''discrete_range_mode : discrete_mode_name LPAREN literal_range RPAREN
							   | basic_mode LPAREN literal_range RPAREN'''
		p[0] = ast.DiscreteRangeMode(p[1], p[3])
		
	def p_discrete_mode_name(self, p):
		'''discrete_mode_name : ID'''
		p[0] = ast.Mode(p[1])

	def p_litereal_range(self, p):
		'''literal_range : lower_bound COLON upper_bound'''
		p[0] = ast.LiteralRange(p[1], p[3])
		
	def p_reference_mode(self, p):
		'''reference_mode : REF mode'''
		p[0] = ast.ReferenceMode(p[2])
	
	def p_composite_mode(self, p):
		'''composite_mode : string_mode
						  | array_mode'''
		p[0] = p[1]
	
	def p_string_mode(self, p):
		'''string_mode : CHARS LBRACKET string_length RBRACKET'''
		p[0] = ast.StringMode(p[3])
	
	def p_string_length(self,p):
		'''string_length : INTCONST'''
		p[0] = p[1]
	
	def p_array_mode(self, p):
		'''array_mode : ARRAY LBRACKET index_mode_list RBRACKET element_node'''
		index_mode = ast.IndexMode(p[3])
		p[0] = ast.ArrayMode(index_mode, p[5])
	
	def p_index_mode_list(self, p):
		'''index_mode_list : index_mode
						   | index_mode_list COMMA index_mode'''
		if(len(p) == 4):
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1]]
	
	def p_index_mode(self, p):
		'''index_mode : discrete_mode
					  | literal_range'''
		p[0] = p[1]
		
	def p_element_node(self, p):
		'''element_node : mode'''
		p[0] = p[1]
	
	####################
	##### NEW MODE #####
	####################
	
	def p_newmode_statement(self, p):
		'''newmode_statement : TYPE newmode_list SMC'''
		p[0] = ast.NewModeStmt(p[2])
	
	def p_newmode_list(self, p):
		'''newmode_list : mode_definition
						| newmode_list COMMA mode_definition'''
		if(len(p) == 4):
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1]]
	
	def p_mode_definition(self, p):
		'''mode_definition : id_list EQUALS mode'''
		p[0] = ast.ModeDef(p[1], p[3])
	
	def p_synonym_statement(self, p):
		'''synonym_statement : SYN syn_list SMC'''
		p[0] = ast.SynStmt(p[2])
	
	###################
	##### SYNONYM #####
	###################
	
	def p_syn_list(self, p):
		'''syn_list : syn_definition
					| syn_list COMMA syn_definition'''
		if(len(p) == 4):
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1]]
			
	def p_syn_definition(self, p):
		'''syn_definition : id_list EQUALS constant_expression'''
		p[0] = ast.SynDef(p[1], None, p[3])
	
	def p_syn_definition2(self, p):
		'''syn_definition : id_list mode EQUALS constant_expression'''
		p[0] = ast.SynDef(p[1], p[2], p[4])

	####################



	####### TEST #######



	####################



	####################
	##### LOCATION #####
	####################
	
	def p_location(self, p):
		'''location : location_name
					| dereferenced_reference
					| string_element
					| string_slice
					| array_element
					| array_slice'''
					#| call_action
		p[0] = p[1]
	
	def p_location_name(self, p):
		'''location_name : ID'''
		p[0] = ast.Location(p[1])
	
	def p_dereferenced_reference(self, p):
		'''dereferenced_reference : location ARROW'''
		p[0] = ast.DereferencedLocation(p[1])
	
	def p_string_element(self, p):
		'''string_element : string_location LBRACKET start_element RBRACKET'''
		p[0] = ast.StringElement(p[1], p[3])
	
	def p_string_location(self, p):
		'''string_location : ID'''
		p[0] = p[1]
	
	def p_start_element(self, p):
		'''start_element : integer_expression'''
		p[0] = p[1]
	
	def p_string_slice(self, p):
		'''string_slice : string_location LBRACKET left_element COLON right_element RBRACKET'''
		p[0] = ast.StringSlice(p[1], p[3], p[5])
	
	def p_left_element(self, p):
		'''left_element : integer_expression'''
		p[0] = p[1]
	
	def p_right_element(self, p):
		'''right_element : integer_expression'''
		p[0] = p[1]
		
	def p_array_element(self, p):
		'''array_element : array_location LBRACKET expression_list RBRACKET'''
		p[0] = ast.ArrayElement(p[1], p[3])
		
	def p_expression_list(self, p):
		'''expression_list : expression
						   | expression_list COMMA expression'''
		if(len(p) == 4):
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1]]
			
	def p_expression(self, p):
		'''expression : integer_expression'''
		p[0] = p[1]
		
	def p_array_slice(self, p):
		'''array_slice : array_location LBRACKET literal_range RBRACKET'''
		p[0] = ast.ArraySlice(p[1], p[3])
	
	def p_array_location(self, p):
		'''array_location : location'''
		p[0] = p[1]

    ########################### TODO:
    
    #change to expression
	def p_lower_bound(self, p):
		'''lower_bound : INTCONST'''
		p[0] = ast.IntConst(p[1])
    
    #change to expression
	def p_upper_bound(self, p):
		'''upper_bound : INTCONST'''
		p[0] = ast.IntConst(p[1])

    #change to expression
	def p_initialization(self, p):
		'''initialization : EQUALS INTCONST'''
		p[0] = ast.IntConst(p[1])

    #change to expression
	def p_constant_expression(self, p):
		'''constant_expression : INTCONST'''
		p[0] = ast.IntConst(p[1])
    
    #create integer_expression
	def p_integer_expression(self, p):
		'''integer_expression : INTCONST'''
		p[0] = ast.IntConst(p[1])


	### Others

	def p_empty(self, p):
		'empty : '
		p[0] = None
