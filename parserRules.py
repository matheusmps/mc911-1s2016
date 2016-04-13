
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens

#def p_program (p): 
#	'''program  : statement
#				| statement statement'''
				
#def p_statement (p):
#	'''statement : declaration_statement
#				 | synonym_statement
#				 | newmode_statement
#				 | procedure_statement
#				 | action_statement

#def p_declaration_statement (p):
#	'''declaration_statement : DCL declaration_list'''


# cuidado com os espacos entre as virgulas
#def p_declaration_list (p):
#	'''declaration_list : declaration
#						| declaration COMMA declaration_list'''

#def p_declaration (p):
#	'''declaration  : id_list mode
#					| id_list mode initialization
	
#def p_initialization (p) :
#	'initialization : EQUAL expression'	
	
#def p_id_list (p):
#	'''id_list  : ID
#				| ID COMMA id_list'''

#############@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##########

def p_synonym_statement (p):
	'synonym_statement  : SYN synonym_list'

def p_synonym_list (p):
	'''synonym_list : synonym_definition 
					| synonym_definition COMMA synonym_definition'''

def p_synonym_definition (p):
	'''synonym_definition 	: id_list EQUAL expression
							| id_list mode EQUAL expression'''

def p_newmode_statement (p):
	'newmode_statement : TYPE newmode_list'

def p_newmode_list (p):
	'''newmode_list : mode_definition 
					| mode_definition COMMA newmode_list'''

def p_mode_definition (p):
	'mode_definition : id_list EQUAL mode'

#def p_mode (p):
#	'''mode : ID
#			| discrete_mode
			| reference_mode
			| composite_mode

#def p_discrete_mode (p):
#	'''discrete_mode : INT
#					 | BOOL
#					 | CHAR
					 | discrete_range_mode'''

def p_discrete_range_mode (p):
	'''discrete_range_mode  : ID LPAREN literal_range RPAREN
							| discrete_mode LPAREN literal_range RPARENT'''

def p_literal_range (p):
	'''literal_range : expression COLON expression'''

def p_reference_mode (p): 
	'''reference_mode : REF mode'''

def p_composite_mode (p):
	'''composite_mode   : string_mode 
						| array_mode'''

def p_string_mode (p): 
	'''string_mode : CHARS LBRACKET INT RBRACKET'''

def p_aray_mode (p):
	'''array_mode 	: ARRAY LBRACKET index_mode_list RBRACKET mode'''

def p_index_mode_list (p):
	'''index_mode_list  : index_mode
						| index_mode COMMA index_mode_list'''

def p_index_mode (p):
	'''index_mode 	: descrete_mode
					| literal_range'''

#def p_location (p):
#	'''location : location_name
				| dereferenced_reference
				| string_element
				| string_slice
				| array_element
				| array_slice
				| call_action'''

def p_dereferenced_reference (p):
	'''dereferenced_reference : location ARROW'''

# integer_expression as INTCONST token
def p_string_element (p):
	'''string_element : ID LBRACKET INTCONST RBRACKET'''

def p_string_slice (p):
	'''string_slice : ID LBRACKET INTCONST COLON INTCONST RBRACKET'''

def p_array_element (p):
	'''array_element : location LBRACKET expression_list RBRACKET'''

def p_expression_list (p):
	'''expression_list 	: expression
						| expression COMMA expression_list'''

def p_array_slice (p):
	'''array_slice : location LBRACKET expression COLON expression RBRACKET'''


#####@@####### 16h


#def p_primitive_value (p):
#	'''primitive_calue  : literal
						| value_array_element
						| value_array_slice
						| parenthesized_expression'''

def p_literal (p):
	'''literal  : INTCONST
				| boolean_literal
				| CHARCONST
				| NULL
				| STRINGCONST'''

def p_boolean_literal (p):
	'''boolean_literal  : FALSE
						| TRUE'''

def p_value_array_element (p):
	'''value_array_element : primitive_value LBRACKET expression_list RBRACKET'''

def p_value_array_slice (p):
	'''value_array_slice : primitive_value LBRACKET LOWER COLON UPPER RBRACKET'''

def p_parethesized_expression (p):
	'''parenthesized_expression : LPAREN expression RPAREN'''

#def p_expression (p):
#	'''expression 	: operand0 
					| conditional_expression'''

def p_condicional_expression (p):
	'''condicional_expression 	: IF boolean_expression then_expression else_expression FI
								| : IF boolean_expression then_expression elsif_expression else_expression FI'''

def p_boolean_expression (p):
	'''boolean_expresion : expression'''

def p_then_expression (p):
	'''then_expression : THEN expression '''

def p_else_expression (p):
	'''else_expression : ELSE expression '''

def p_elsif_expression (p):
	'''elsif_expression : ELSIF boolean_expression then_expression
						| elsif_expression ELSIF boolean_expression then_expression '''

#def p_operand0 (p):
#	'''operand0 : operand1
#				| operand0 operator1 operand1 '''

#def p_operator1 (p):
#	'''operator1 	: relational_operator
#					| IN'''

#def p_relational_operator (p):
#	'''relational_operator 	: AND
#							| OR
#							| ISEQUAL
#							| NOTEQUAL
#							| GT
#							| GE
#							| LT
#							| LE'''

#def p_operand1 (p):
#	'''operand1 : operand2
#				| operand1 operator2 operand2 '''

#def p_operator2 (p):
#	'''operator2 	: arithmetic_additive_operator
#					| STRCONC'''

#def p_arithmetic_additive_operator (p):
#	'''arithmetic_additive_operator : PLUS
#									| MINUS '''

#def p_operand2 (p):
#	'''operand2 : operand3
#				| operand2 arithmetic_multiplicative_operator operand3 '''

#def p_arithmetic_multiplicative_operator (p):
#	'''arithmetic_multiplicative_operator 	: TIMES
#											| DIV
#											| MOD'''

#def p_operand3 (p):
#	'''operand3 : operand4
#				| monadic_operator operand4
#				| INTCONST '''

#def p_monadic_operator (p):
#	'''monadic_operator : MINUS
#						| NOT'''

#def p_operand4 (p):
#	'''operand4 : location
#				| referenced_location
#				| primitive_value '''

#def p_referenced_location (p):
#	'''referenced_location : ARROW location '''

#def p_action_statement (p):
#	'''action_statement : action
#						| ID COLON action '''

#def p_action (p):
#	'''action 	: bracketed_action
#				| assignment_action
#				| call_action
#				| exit_action
#				| return_action
#				| result_action  '''

def p_bracketed_action (p):
	'''bracketed_action : if_action
						| do_action '''

#def p_assignment_action (p):
#	'''assignment_action : location assigning_operator expression '''

#def p_assigning_operator (p):
#	'''assigning_operator 	: EQUALS
#							| closed_dyadic_operator EQUALS '''

#def p_closed_dyadic_operator (p):
#	'''closed_dyadic_operator 	: arithmetic_additive_operator
#								| arithmetic_multiplicative_operator
#								| STRCONC '''

def p_if_action (p):
	'''if_action 	: IF boolean_expression then_clause FI
					| IF boolean_expression then_clause else_clause FI '''

def p_then_clause (p):
	'''then_clause 	: THEN
					: THEN action_list '''

def p_action_list(p):
	'''action_list 	: action_statement
					| action_statement action_list'''

def p_else_clause (p):
	'''else_clause 	: ELSE action_list
					| ELSIF boolean_expression then_clause
					| ELSIF boolean_expression then_clause else_clause '''

def p_do_action (p):
	'''do_action 	: DO action_list OD 
					| DO control_part SMC action_list OD'''

def p_control_part (p):
	'''control_part : for_control
					| for_control while_control
					| while_control '''

def p_for_control (p):
	'''for_control 	: FOR iteration '''

def p_iteration (p):
	'''iteration 	: step_enumeration
					| range_enumeration '''

def p_step_enumeration (p):
	'''step_enumeration : ID EQUAL expression TO expression
						| ID EQUAL expression step_value TO expression
						| ID EQUAL expression step_value DOWN TO expression
						| ID EQUAL expression DOWN TO expression'''

def p_step_value (p):
	'''step_value : BY INTCONST '''

def p_range_enumeration (p):
	'''range_enumeration 	: ID IN  ID
							| ID DOWN IN ID'''

def p_while_control (p):
	'''while_control : WHILE boolean_expression '''

def p_call_action(p):
	'''call_action 	: procedure_call
					| builtin_call '''

def p_procedure_call (p):
	'''procedure_call 	: ID LPAREN RPAREN
						| ID LPAREN parameter_list RPAREN '''

def p_parameter_list(p):
	'''parameter_list 	: expression
						| expression COMMA parameter_list '''

def p_exit_action(p):
	'''exit_action : EXIT ID '''

def p_return_action(p):
	'''return_action 	: RETURN
						| RETURN expression '''

def p_result_action(p):
	'''result_action : RESULT expression '''

def p_builtin_call (p):
	'''builtin_call : builtin_name LPAREN RPAREN
					| builtin_name LPAREN parameter_list RPAREN '''

def p_builtin_name (p):
	'''builtin_name : NUM
					| PRED
					| SUCC
					| UPPER
					| LOWER
					| LENGTH
					| READ
					| PRINT '''

def p_procedure_statement (p):
	'''procedure_statement : ID COLON procedure_definition SMC'''

def p_procedure_definition (p):
	'''procedure_definition : PROC LPAREN RPAREN SMC END 
							| PROC LPAREN formal_parameter_list RPAREN SMC END
							| PROC LPAREN formal_parameter_list RPAREN result_spec SMC END
							| PROC LPAREN formal_parameter_list RPAREN result_spec SMC statement_list END
							| PROC LPAREN formal_parameter_list RPAREN SMC statement_list END
							| PROC LPAREN RPAREN result_spec SMC statement_list END
							| PROC LPAREN RPAREN SMC statement_list END
							| PROC LPAREN RPAREN result_spec SMC END'''

def p_statement_list (p):
	'''statement_list 	: statement
						| statement statement_list'''

def p_formal_parameter_list (p):
	'''formal_parameter_list 	: formal_parameter
								| formal_parameter COMMA formal_parameter_list '''

def p_formal_parameter (p):
	'''formal_parameter : id_list parameter_spec '''

def p_parameter_spec (p):
	'''parameter_spec  	: mode
						| mode LOC '''

def p_result_spec (p):
	'''result_spec 	: RETURNS LPAREN mode RPAREN
					| RETURNS LPAREN mode LOC RETURNS'''

#def p_comment (p):
#	'''comment 	: bracketed_comment
#				| line_end_comment '''

#def p_bracketed_comment (p):
#	'''bracketed_comment : COMMENT'''

#def p_line_end_comment (p):
#	'''line_end_comment : COMMENTLINE'''


#########@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#############

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
