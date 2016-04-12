from ply import yacc
from lyaLexer import LyaLexer 
from aux.plyParser import PLYParser, Coord, ParseError

class LyaParser(PLYParser):
	
	def __init__(self):
		self.lexer = LyaLexer(lBraceFunc=self._onLeftBrace, rBraceFunc=self._onRightBrace)
		self.lexer.build()
		self.tokens = self.lexer.tokens
		#self.parser = yacc.yacc(module=self, start='program')
		
		# Stack of scopes for keeping track of symbols. _scope_stack[-1] is
        # the current (topmost) scope. Each scope is a dictionary that
        # specifies whether a name is a type. If _scope_stack[n][name] is
        # True, 'name' is currently a type in the scope. If it's False,
        # 'name' is used in the scope but not as a type (for instance, if we
        # saw: int name;
        # If 'name' is not a key in _scope_stack[n] then 'name' was not defined
        # in this scope at all.
		self._scope_stack = [dict()]
		
		# Keeps track of the last token given to yacc (the lookahead token)
		self._last_parser_token = None
		
	def initParser(self):
		self._scope_stack = [dict()]
		self._last_parser_token = None
		
	def parse(self, text, filename='', debuglevel=0):
		self.lexer.reset()
		self.initParser()
		return self.parser.parse(
			input=text,
			lexer=self.lexer,
			debug=debuglevel)
			
	def testLexer(self, filePath):
		self.lexer.listTokens(filePath)
		
	######################--   PRIVATE   --######################
		
	def _spope_push(self):
		self._scope_stack.append(dict())
		
	def _scope_pop(self):
		assert len(self._scope_stack) > 1
		self._scope_stack.pop()
		
	def _onLeftBrace(self):
		print("lbrace")
		self._spope_push()
	
	def _onRightBrace(self):
		print("rbrace")
		self._scope_pop()

