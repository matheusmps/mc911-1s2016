
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
