from ply import yacc
from lyaLexer import LyaLexer 
from aux.plyParser import PLYParser, Coord, ParseError

class LyaParser(PLYParser):
	
	def __init__(self):
		self.lexer = LyaLexer(
			error_func=self._lex_error,
			lBraceFunc=self._lex_onLeftBrace, 
			rBraceFunc=self._lex_onRightBrace)
		
		self.lexer.build()
		self.tokens = self.lexer.tokens
		#self.parser = yacc.yacc(module=self, start='program')
		
		# Stack of scopes for keeping track of symbols. 
		# _scope_stack[-1] is the current (topmost) scope.  
		# If _scope_stack[n][name] is True, 'name' is currently a symbol in the scope.
		# Otherwise 'name' is not used in this scope at all.
		self._scope_stack = [dict()]
		
		
	def initParser(self):
		self._scope_stack = [dict()]
		
	def parse(self, text, filename='', debuglevel=0):
		self.lexer.reset()
		self.initParser()
		return self.parser.parse(
			input=text,
			lexer=self.lexer,
			debug=debuglevel)
			
	def testLexer(self, filePath):
		self.lexer.filename = filePath
		self.lexer.listTokens(filePath)
		
	######################--   PRIVATE   --######################
	
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
		print("lbrace")
		self._spope_push()
	
	def _lex_onRightBrace(self):
		print("rbrace")
		self._scope_pop()
		
	def _add_identifier(self, name, coord):
		self._scope_stack[-1][name] = True

	def _get_yacc_lookahead_token(self):
		return self.lexer.last_token
