import ply.lex as lex

# List of token name.

tokens = (

# Reserved Words
'ARRAY', 'BY', 'CHARS', 'DCL', 'DO', 'DOWN', 'ELSE', 'ELSIF', 'END', 'EXIT', 'FI', 'FOR', 'IF', 'IN', 'LOC', 'TYPE', 'OD', 'PROC', 'REF', 'RESULT', 'RETURN', 'RETURNS', 'SYN', 'THEN', 'TO', 'WHILE',

# Predefined words

'BOOL', 'CHAR', 'FALSE', 'INT', 'LENGTH', 'LOWER', 'NULL', 'NUM','PRED', 'PRINT', 'READ', 'SUCC', 'TRUE', 'UPPER',

# Defined token

'COMMA', 'SMC', 'COLON', 'LPARENT', 'RPARENT', 'EQUAL', 'ISEQUAL', 'PEQUAL', 'TEQUAL', 'MEQUAL', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'GTHAN', 'LTHAN', 'GETHAN', 'LETHAN'

)



ARRAY : 'array'
BY : 'by'
CHARS : 'chars'
DCL : 'dcl'
DO : 'do'
DOWN : 'down'
ELSE : 'else'
ELSIF : 'elsif'
END : 'end'
EXIT : 'exit'
FI : 'fi'
FOR : 'for'
IF : 'if'
IN : 'in'
LOC : 'loc'
TYPE : 'type'
OD : 'od'
PROC : 'proc'
REF : 'ref'
RESULT : 'result'
RETURN : 'return'
RETURNS : 'returns'
SYN : 'syn'
THEN : 'then'
TO : 'to'
WHILE : 'while'
BOOL : 'bool'
CHAR : 'char'
FALSE : 'false'
INT : 'int'
LENGTH : 'lenght'
LOWER : 'lower'
NULL : 'null'
NUM : 'num' 
PRED : 'pred'
PRINT : 'print'
READ : 'read'
SUCC : 'succ'
TRUE : 'true'
UPPER : 'upper'
COMMA : ','
SMC : ';'
COLON : ':'
LPARENT : '('
RPARENT : ')'
EQUAL : '='
ISEQUAL : '==' 
PEQUAL : '+='
TEQUAL : '*='
MEQUAL : '-='
PLUS : '+'
MINUS : '-'
TIMES : '*'
DIVIDE : '/'
GTHAN : '>'
LTHAN : '<'
GETHAN : '>='
LETHAN : '<='




