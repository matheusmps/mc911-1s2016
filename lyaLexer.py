import tokenRules

import ply.lex as lex
import sys

class LyaLexer(object):
	def __init__(self):
		self.lexer = lex.lex(module=tokenRules)
		self.last_token = None
		
	def input(self, text):
		self.lexer.input(text)
		
	def token(self):
		self.last_token = self.lexer.token()
		return self.last_token
		
	def listTokens(self, filePath):
		""" Used only for tests. """
		self.input(self._readFile(filePath))
		while True:
			tok = self.token()
			if not tok: 
				break      # No more input
			print(tok)
			
	### PRIVATE
	
	def _readFile(self, filePath):
		with open(filePath, 'r') as myFile:
			data = myFile.read()
		return data
		
	

