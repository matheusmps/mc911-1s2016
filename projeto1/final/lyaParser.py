from ply import yacc
from lyaLexer import LyaLexer 
from aux.plyParser import PLYParser, Coord, ParseError
from aux.readFileHelper import FileHelper
import aux.ast as ast

class LyaParser(PLYParser):

	def __init__(self):
		self.lexer = LyaLexer(
			error_func=self._lex_error)
		
		self.lexer.build()
		self.tokens = self.lexer.tokens
		self.parser = yacc.yacc(module=self, start='program')

	def initParser(self):
		pass

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

	def p_error(self, p):
		if p:
			self._parse_error(
				'before: %s' % p.value,
				self._coord(lineno=p.lineno,
					column=self.lexer.find_tok_column(p)))
		else:
			self._parse_error('At end of input', '')


	######################--   PRIVATE   --######################


	def _readFile(self, filePath):
		return FileHelper(filePath).readFile()

	def _lex_error(self, msg, line, column):
		self._parse_error(msg, self._coord(line, column))


	######################--   RULES  --######################


	############ PROGRAM AND STATEMENTS ############


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
					| synonym_statement
					| action_statement
					| procedure_statement'''
		p[0] = p[1]


	############ DECLARATION STATEMENT ############


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

	def p_initialization(self, p):
		'''initialization : EQUALS expression'''
		p[0] = p[2]


	############ MODE ############


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

	def p_lower_bound(self, p):
		'''lower_bound : expression'''
		p[0] = p[1]

	def p_upper_bound(self, p):
		'''upper_bound : expression'''
		p[0] = p[1]

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


	############ NEW MODE STATEMENT ############


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


	############ SYNONYM STATEMENT ############


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

	def p_constant_expression(self, p):
		'''constant_expression : expression'''
		p[0] = p[1]


	############ PRIMITIVE VALUES ############


	def p_primitive_value (self, p):
		'''primitive_value  : literal
							| value_array_element
							| value_array_slice
							| parenthesized_expression'''
		p[0] = p[1]

	def p_literal (self, p):
		'''literal  : integer_literal
					| boolean_literal
					| char_literal
					| empty_literal
					| string_literal'''
		p[0] = p[1]

	def p_integer_literal (self, p):
		'''integer_literal : INTCONST '''
		p[0] = ast.IntConst(p[1])

	def p_boolean_literal (self, p):
		'''boolean_literal  : FALSE
							| TRUE'''
		p[0] = ast.Boolean(p[1])

	def p_char_literal (self, p):
		'''char_literal : CHARCONST '''
		p[0] = ast.CharConst(p[1])

	def p_string_literal (self, p):
		'''string_literal : STRINGCONST '''
		p[0] = ast.StrConst(p[1])

	def p_empty_literal (self, p):
		'''empty_literal : NULL '''
		p[0] = ast.EmptyConst()

	def p_value_array_element(self, p):
		'''value_array_element : array_primitive_value LBRACKET expression_list RBRACKET'''
		p[0] = ast.ValueArrayElement(p[1], p[3])

	def p_value_array_slice(self, p):
		'''value_array_slice : array_primitive_value LBRACKET literal_range RBRACKET'''
		p[0] = ast.ValueArraySlice(p[1], p[3])

	def p_array_primitive_value(self, p):
		'''array_primitive_value : primitive_value'''
		p[0] = p[1]

	def p_parenthesized_expression(self, p):
		'''parenthesized_expression : LPAREN expression RPAREN'''
		p[0] = p[2]


	############ ACTION STATEMENT ############


	def p_action_statement (self, p):
		'''action_statement : action SMC
							| label COLON action SMC '''
		if(len(p) == 5):
			p[0] = ast.ActionStatement(p[3], p[1])
		else:
			p[0] = ast.ActionStatement(p[1], None)

	def p_label(self,p):
		'''label : ID'''
		p[0] = ast.Label(p[1])

	def p_action (self, p):
		'''action 	: assignment_action
					| bracketed_action
					| call_action
					| exit_action
					| return_action
					| result_action '''
		p[0] = p[1]


	############ ASSIGNEMENT ACTION ############


	def p_assignment_action (self, p):
		'''assignment_action : location assigning_operator expression '''
		p[0] = ast.Assignment(p[1], p[2], p[3])

	def p_assigning_operator (self, p):
		'''assigning_operator 	: EQUALS
								| closed_dyadic_operator EQUALS '''
		if(len(p) == 3):
			p[0] = p[1] + p[2] 
		else:
			p[0] = p[1]

	def p_closed_dyadic_operator (self, p):
		'''closed_dyadic_operator	: arithmetic_additive_operator
									| arithmetic_multiplicative_operator
									| string_concatenation_operator '''
		p[0] = p[1]

	def p_expression_list(self, p):
		'''expression_list : expression
						   | expression_list COMMA expression'''
		if(len(p) == 4):
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1]]

	def p_expression (self, p):
		'''expression 	: operand0
						| conditional_expression'''
		p[0] = p[1]

	def p_operand0 (self, p):
		'''operand0 : operand1
					| operand0 operator1 operand1 '''
		if(len(p) == 4):
			p[0] = ast.Expression(p[1], p[2], p[3])
		else:
			p[0] = p[1]

	def p_operator1 (self, p):
		'''operator1 	: relational_operator
						| membership_operator'''
		p[0] = p[1]

	def p_membership_operator (self,p):
		'''membership_operator : IN'''
		p[0] = p[1]

	def p_relational_operator (self, p):
		'''relational_operator 	: AND
								| OR
								| ISEQUAL
								| NOTEQUAL
								| GT
								| GE
								| LT
								| LE'''
		p[0] = p[1]	

	def p_operand1 (self, p):
		'''operand1 : operand2
					| operand1 operator2 operand2 '''
		if(len(p) == 4):
			p[0] = ast.Expression(p[1], p[2], p[3])
		else:
			p[0] = p[1]

	def p_operator2 (self, p):
		'''operator2 	: arithmetic_additive_operator
						| string_concatenation_operator'''
		p[0] = p[1]

	def p_arithmetic_additive_operator (self, p):
		'''arithmetic_additive_operator : PLUS
										| MINUS '''
		p[0] = p[1]

	def p_string_concatenation_operator (self, p):
		'''string_concatenation_operator : STRCONC'''
		p[0] = p[1]

	def p_operand2 (self, p):
		'''operand2 : operand3
					| operand2 arithmetic_multiplicative_operator operand3 '''
		if(len(p) == 4):
			p[0]= ast.Expression(p[1], p[2], p[3])
		else:
			p[0] = p[1]

	def p_arithmetic_multiplicative_operator (self, p):
		'''arithmetic_multiplicative_operator 	: TIMES
												| DIV
												| MOD'''
		p[0] = p[1]

	def p_operand3 (self, p):
		'''operand3 : operand4
					| monadic_operator operand4'''
		if(len(p) == 3):
			p[0] = ast.Expression(p[2], p[1], None)
		else:
			p[0] = p[1]

	def p_monadic_operator (self, p):
		'''monadic_operator : MINUS
							| NOT'''
		p[0] = p[1]

	def p_operand4 (self, p):
		'''operand4 : primitive_value
					| location
					| referenced_location'''
		p[0] = p[1]

	############ CONDITIONAL EXPRESSION ############
	
	def p_conditional_expression(self, p):
		'''conditional_expression : IF boolean_expression then_expression else_expression FI'''
		p[0] = ast.ConditionalExpression(p[2], p[3], None, p[4])

	def p_conditional_expression2(self, p):
		'''conditional_expression : IF boolean_expression then_expression elseif_expression_list else_expression FI'''
		p[0] = ast.ConditionalExpression(p[2], p[3], p[4], p[5])

	def p_boolean_expression(self, p):
		'''boolean_expression : expression'''
		p[0] = p[1]

	def p_then_expression(self, p):
		'''then_expression : THEN expression'''
		p[0] = p[2]

	def p_else_expression(self, p):
		'''else_expression : ELSE expression'''
		p[0] = p[2]

	def p_elseif_expression_list(self, p):
		'''elseif_expression_list : elseif_expression
								  | elseif_expression_list elseif_expression'''
		if(len(p) == 3):
			p[0] = p[1] + [p[2]]
		else:
			p[0] = [p[1]]

	def p_elseif_expression(self, p):
		'''elseif_expression : ELSIF boolean_expression then_expression'''
		p[0] = ast.ConditionalExpression(p[2], p[3], None, None)


	############ LOCATION ############


	def p_referenced_location (self, p):
		'''referenced_location : ARROW location '''
		p[0] = ast.ReferencedLocation(p[2])

	def p_location(self, p):
		'''location : location_name
					| string_reference
					| dereferenced_reference
					| array_element
					| array_slice
					| call_action'''
		p[0] = p[1]

	def p_location_name(self, p):
		'''location_name : ID'''
		p[0] = ast.Location(p[1])

	def p_string_reference(self, p):
		'''string_reference : location_name LBRACKET integer_expression RBRACKET'''
		p[0] = ast.StringElement(p[1], p[3])

	def p_string_reference2(self, p):
		'''string_reference : location_name LBRACKET literal_range RBRACKET'''
		p[0] = ast.StringSlice(p[1], p[3])

	def p_dereferenced_reference(self, p):
		'''dereferenced_reference : location ARROW'''
		p[0] = ast.DereferencedLocation(p[1])

	def p_array_element(self, p):
		'''array_element : location LBRACKET expression_list RBRACKET'''
		p[0] = ast.ArrayElement(p[1], p[3])

	def p_array_slice(self, p):
		'''array_slice : location LBRACKET literal_range RBRACKET'''
		p[0] = ast.ArraySlice(p[1], p[3])


	############ BRACKETED ACTION ############


	def p_bracketed_action(self, p):
		'''bracketed_action : if_action
							| do_action'''
		p[0] = p[1]


	############ IF ACTION ############


	def p_if_action(self, p):
		'''if_action : IF boolean_expression then_clause FI'''
		p[0] = ast.IfAction(p[2], p[3], None)

	def p_if_action2(self, p):
		'''if_action : IF boolean_expression then_clause else_clause FI'''
		p[0] = ast.IfAction(p[2], p[3], p[4])

	def p_then_clause(self, p):
		'''then_clause : THEN 
					   | THEN action_statement_list'''
		if(len(p) == 3):
			p[0] = p[2]
		else:
			p[0] = None

	def p_else_clause(self, p):
		'''else_clause : ELSE
					   | ELSE action_statement_list'''
		if(len(p) == 3):
			p[0] = [ast.ElseClause(p[2])]
		else:
			p[0] = []

	def p_else_clause2(self, p):
		'''else_clause : elseif_clause'''
		p[0] = p[1]

	def p_elseif_clause(self, p):
		'''elseif_clause : ELSIF boolean_expression then_clause'''
		p[0] = [ast.ElseIfClause(p[2], p[3])]

	def p_elseif_clause2(self, p):
		'''elseif_clause : ELSIF boolean_expression then_clause else_clause'''
		p[0] = [ast.ElseIfClause(p[2], p[3])] + p[4]
		

	def p_action_statement_list(self, p):
		'''action_statement_list : action_statement
								 | action_statement_list action_statement'''
		if(len(p) == 3):
			p[0] = p[1] + [p[2]] 
		else:
			p[0] = [p[1]]


	############ DO ACTION ############


	def p_do_action(self, p):
		'''do_action : DO OD'''
		p[0] = ast.DoAction(None, None)

	def p_do_action2(self, p):
		'''do_action : DO control_part SMC OD'''
		p[0] = ast.DoAction(p[2], None)

	def p_do_action3(self, p):
		'''do_action : DO control_part SMC action_statement_list OD'''
		p[0] = ast.DoAction(p[2], p[4])

	def p_do_action4(self, p):
		'''do_action : DO action_statement_list OD'''
		p[0] = ast.DoAction(None, p[2])

	def p_control_part(self, p):
		'''control_part : for_control
						| while_control'''
		p[0] = [p[1]]

	def p_control_part2(self, p):
		'''control_part : for_control while_control'''
		p[0] = [p[1], p[2]]

	def p_for_control(self, p):
		'''for_control : FOR iteration'''
		p[0] = ast.For(p[2])

	def p_iteration(self, p):
		'''iteration : step_enumeration
					 | range_enumeration'''
		p[0] = p[1]

	def p_step_enumeration(self, p):
		'''step_enumeration : loop_counter EQUALS start_value end_value'''
		p[0] = ast.StepEnumeration(p[1], p[3], None, p[4], False)

	def p_step_enumeration2(self, p):
		'''step_enumeration : loop_counter EQUALS start_value step_value end_value'''
		p[0] = ast.StepEnumeration(p[1], p[3], p[4], p[5], False)

	def p_step_enumeration3(self, p):
		'''step_enumeration : loop_counter EQUALS start_value DOWN end_value'''
		p[0] = ast.StepEnumeration(p[1], p[3], None, p[5], True)

	def p_step_enumeration4(self, p):
		'''step_enumeration : loop_counter EQUALS start_value step_value DOWN end_value'''
		p[0] = ast.StepEnumeration(p[1], p[3], p[4], p[5], True)

	def p_loop_counter(self, p):
		'''loop_counter : ID'''
		p[0] = ast.Location(p[1])

	def p_start_value(self, p):
		'''start_value : discrete_expression'''
		p[0] = p[1]

	def p_step_value(self, p):
		'''step_value : BY integer_expression'''
		p[0] = p[2]

	def p_end_value(self, p):
		'''end_value : TO discrete_expression'''
		p[0] = p[2]

	def p_discrete_expression(self, p):
		'''discrete_expression : expression'''
		p[0] = p[1]

	def p_range_enumeration(self, p):
		'''range_enumeration : loop_counter IN discrete_mode'''
		p[0] = ast.RangeEnumeration(p[1], p[3], False)

	def p_range_enumeration2(self, p):
		'''range_enumeration : loop_counter DOWN IN discrete_mode'''
		p[0] = ast.RangeEnumeration(p[1], p[4], True)

	def p_while_control(self, p):
		'''while_control : WHILE boolean_expression'''
		p[0] = ast.While(p[2])


	############ PROCEDURE STATEMENT ############


	def p_procedure_statement(self, p):
		'''procedure_statement : label COLON procedure_definition SMC'''
		p[0] = ast.ProcedureStmnt(p[1], p[3])

	def p_procedure_definition1 (self, p):
		'''procedure_definition : PROC LPAREN RPAREN SMC END
								| PROC LPAREN formal_parameter_list RPAREN SMC statement_list END
								| PROC LPAREN RPAREN SMC statement_list END'''
		if(len(p) == 6):
			p[0] = ast.ProcedureDef(None, None, None)
		elif(len(p) == 8):
			p[0] = ast.ProcedureDef(p[3], None, p[6])
		else:
			p[0] = ast.ProcedureDef(None, None, p[5])

	def p_procedure_definition2 (self, p):
		'''procedure_definition : PROC LPAREN formal_parameter_list RPAREN SMC END
								| PROC LPAREN formal_parameter_list RPAREN result_spec SMC END
								| PROC LPAREN formal_parameter_list RPAREN result_spec SMC statement_list END'''
		if(len(p) == 9):
			p[0] = ast.ProcedureDef(p[3], p[5], p[7])
		elif(len(p) == 8):
			p[0] = ast.ProcedureDef(p[3], p[5], None)
		else:
			p[0] = ast.ProcedureDef(p[3], None, None)

	def p_procedure_definition3 (self, p):
		'''procedure_definition : PROC LPAREN RPAREN result_spec SMC statement_list END
								| PROC LPAREN RPAREN result_spec SMC END'''
		if(len(p) == 8):
			p[0] = ast.ProcedureDef(None, p[4], p[6])
		else:
			p[0] = ast.ProcedureDef(None, p[4], None)

	def p_formal_parameter_list (self, p):
		'''formal_parameter_list 	: formal_parameter
									| formal_parameter COMMA formal_parameter_list '''
		if(len(p) == 4):
			p[0] = [p[1]] + p[3]
		else:
			p[0] = [p[1]]

	def p_formal_parameter (self, p):
		'''formal_parameter : id_list parameter_spec '''
		p[0] = ast.FormalParameter(p[1], p[2])

	def p_parameter_spec (self, p):
		'''parameter_spec 	: mode
							| mode parameter_attribute'''
		if(len(p) == 3):
			p[0] = ast.ParameterSpecs(p[1], p[2])
		else:
			p[0] = ast.ParameterSpecs(p[1], None)

	def p_parameter_attribute (self, p):
		'''parameter_attribute : LOC'''
		p[0] = p[1]

	def p_result_spec (self, p):
		'''result_spec 	: RETURNS LPAREN mode RPAREN
						| RETURNS LPAREN mode result_attribute RPAREN'''
		if(len(p) == 6):
			p[0] = ast.ResultSpecs(p[3], p[4])
		else:
			p[0] = ast.ResultSpecs(p[3], None)

	def p_result_attribute (self,p):
		'''result_attribute : LOC'''
		p[0] = p[1]


	############ CALL ACTION #############


	def p_call_action (self,p):
		'''call_action	: procedure_call
						| builtin_call'''
		p[0] = p[1]

	def p_procedure_call (self, p):
		'''procedure_call : ID LPAREN RPAREN
						  | ID LPAREN parameter_list RPAREN '''
		if(len(p) == 5):
			p[0] = ast.ProcedureCall(p[1], p[3])
		else:
			p[0] = ast.ProcedureCall(p[1], None)

	def p_parameter_list(self, p):
		'''parameter_list : parameter
						  | parameter COMMA parameter_list '''
		if(len(p) == 4):
			p[0] = [p[1]] + p[3]
		else:
			p[0] = [p[1]]

	def p_parameter(self, p):
		'''parameter : expression'''
		p[0] = p[1]

	#def p_procedure_name(self, p):
	#	'''procedure_name : ID'''
	#	p[0] = ast.Location(p[1])

	def p_exit_action(self, p):
		'''exit_action	: EXIT label'''
		p[0] = ast.ExitAction(p[2])

	def p_return_action(self, p):
		'''return_action 	: RETURN
							| RETURN result'''
		if(len(p) == 3):
			p[0] = ast.ReturnAction(p[2])
		else:
			p[0] = ast.ReturnAction(None)

	def p_result_action(self, p):
		'''result_action : RESULT result'''
		p[0] = ast.ResultAction(p[2])

	def p_result (self, p):
		'''result : expression'''
		p[0] = p[1]

	def p_builtin_call(self, p):
		'''builtin_call : builtin_name LPAREN RPAREN 
						| builtin_name LPAREN parameter_list RPAREN'''
		if(len(p) == 5):
			p[0] = ast.BuiltinCall(p[1],p[3])
		else:
			p[0] = ast.BuiltinCall(p[1],p[3])

	def p_builtin_name(self, p):
		'''builtin_name : NUM
						| PRED
						| SUCC
						| UPPER
						| LOWER
						| LENGTH
						| READ
						| PRINT '''
		p[0] = p[1]


    ########################### TODO:


    #create integer_expression
	def p_integer_expression(self, p):
		'''integer_expression : expression'''
		p[0] = p[1]


	### Others

	def p_empty(self, p):
		'empty : '
		p[0] = None
