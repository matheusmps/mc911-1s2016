
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens

def p_negative(p):
	'expression : MINUS expression'
	p[0] = -p[2]

def p_binary_operators(p):
    '''expression : expression PLUS term
				  | expression : expression MINUS term
			term  : term TIMES factor
				  | term DIVIDE factor'''
    if p[2] == '+':
    p[0] = p[1] + p[3]
    elif p[2] == '-':
    p[0] = p[1] - p[3]
	elif p[2] == '*':
	p[0] = p[1] * p[3]
	elif p[2] == '/':
	p[0] = p[1] / p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]
    
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


def p_program (p): 
	'''program  : statement
				| statement statement'''
				
def p_statement (p):
	'''statement : declaration_statement
				 | synonym_statement
				 | newmode_statement
				 | procedure_statement
				 | action_statement'''

def p_declaration_statment (p):
	'''declaration_statement : DCL declaration_list'''


# cuidado com os espacos entre as virgulas
def p_declaration_list (p):
	'''declaration_list : declaration
						| declaration COMMA declaration_list'''

def p_declaration (p):
	'''declaration  : id_list mode
					| id_list mode initialization'''	
	
def p_initialization (p) :
	'initialization : EQUAL expression'	
	
def p_id_list (p):
	'''id_list  : ID
				| ID COMMA id_list'''

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

def p_mode (p):
	'''mode : ID
			| discrete_mode
			| reference_mode
			| composite_mode'''

def p_discrete_mode (p):
	'''discrete_mode : INT
					 | BOOL
					 | CHAR
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

def p_location (p):
	'''location : location_name
				| dereferenced_reference
				| string_element
				| string_slice
				| array_element
				| array_slice
				| call_action'''

def p_dereferenced_reference (p):
	'''dereferenced_reference : location ->'''

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
