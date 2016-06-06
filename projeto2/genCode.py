import nodeVisitor
import util.ast as ast

class CodeGenerator(nodeVisitor.NodeVisitor):
	
	def __init__(self):
		self.program = []
		self.environment = None
	
	def printInstructions(self):
		print("\n\n")
		print("---- INSTRUCTIONS ----")
		for val in self.program:
			if type(val) is not tuple:
				print("\n ### %s ###" % val)
			else:
				print("(", end="")
				for i, value in enumerate(val):
					if value is not None:
						if i == 0:
							print("'%s'" % value, end="")
						else:
							print(", '%s'" % value, end="")
				print(")")

	def addInstruction(self, opcode, operand1, operand2):
		inst = (opcode, operand1, operand2)
		self.program.append(inst)

	def addComment(self, message):
		self.program.append(message)

	def calculateSizeAloc(self, node):
		counter = 0
		for key, value in node.symtab.items():
			declNode = value.get("node")
			if isinstance(declNode, ast.Declaration):
				counter = counter + self.environment.countAlocSizeForMode(declNode.mode)
		return counter

	def getSymbolInformation(self, name):
		sym = self.environment.lookupComplete(name)
		if sym is not None:
			return (sym.get("scope_level"), sym.get("offset"))
		else:
			return None

	def loadLocation(self, node, left_side = False):
		sym = self.environment.lookup(node.idName)
		mode = sym.mode
		if isinstance(mode, ast.ReferenceMode) or isinstance(mode, ast.DiscreteRangeMode):
			mode = mode.mode
		
		if isinstance(mode, ast.StringMode) or isinstance(mode, ast.ArrayMode):
			base = self.getSymbolInformation(node.idName)
			self.addInstruction('ldr', base[0], base[1])

			# or ArrayElement???
			if isinstance(node, ast.StringSlice) or isinstance(node, ast.ArraySlice) or isinstance(node, ast.StringElement):
				self.loadSliceLocations(node, left_side)
		elif not left_side:
			if isinstance(node, ast.Location):
				sym = self.getSymbolInformation(node.idName)
				self.addInstruction('ldv', sym[0], sym[1])
			elif isinstance(node, ast.ReferencedLocation):
				sym = self.getSymbolInformation(node.idName)
				self.addInstruction('ldr', sym[0], sym[1])
			elif isinstance(node, ast.DereferencedLocation):
				sym = self.getSymbolInformation(node.idName)
				self.addInstruction('lrv', sym[0], sym[1])


	def saveLocation(self, node):
		if isinstance(node, ast.StringElement) or isinstance(node, ast.StringSlice) or isinstance(node, ast.ArraySlice) or isinstance(node, ast.ArrayElement):
			size = self.environment.countAlocSizeForLocation(node)
			self.addInstruction('smv', size, None)
		else:
			sym = self.environment.lookup(node.idName)
			mode = sym.mode
			
			if isinstance(mode, ast.ReferenceMode) or isinstance(mode, ast.DiscreteRangeMode):
				mode = mode.mode
				
			if isinstance(mode, ast.StringMode) or isinstance(mode, ast.ArrayMode):
					size = self.environment.countAlocSizeForMode(mode)
					self.addInstruction('smv', size, None)
			else:
				sym = self.getSymbolInformation(node.idName)
				self.addInstruction('stv', sym[0], sym[1])

	### -------------------------------------------------------------- ###

	def visit_Program(self, node):
		self.environment = node.environment
		node.environment.printStack()
		self.addInstruction('stp', None, None)
		self.addInstruction('alc', self.calculateSizeAloc(node), None)
		for statement in node.statements:
			self.visit(statement)

	#def visit_DeclStmt(self, node):
	#generic

	def visit_Declaration(self, node):
		for name in node.idList:
			if node.init is not None:
				self.visit(node.init)
				sym = self.getSymbolInformation(name)
				self.addInstruction('stv', sym[0], sym[1])

	### -------------------------------------------------------------- ###

	### MODE ###

	#def visit_Mode(self, node):
	# generic

	#def visit_DiscreteMode(self, node):

	#def visit_ReferenceMode(self, node):

	#def visit_DiscreteRangeMode(self, node):

	#def visit_LiteralRange(self, node):

	#def visit_StringMode(self, node):

	# def visit_ArrayMode(self, node):
	# como saber quanto de memoria sera alocado
	# se as expressoes sao avaliadas em tempo de execucao

	# def visit_IndexMode(self, node):

	### -------------------------------------------------------------- ###

	### MODE / SYN DEFINITION ###

	#def visit_ModeDef(self, node):

	#def visit_NewModeStmt(self, node):

	#def visit_SynDef(self, node):

	### -------------------------------------------------------------- ###

	### LOCATION ###

	def visit_Location(self, node):
		#sym = self.getSymbolInformation(node.idName)
		#self.addInstruction('ldv', sym[0], sym[1])
		self.loadLocation(node)

	def visit_ReferencedLocation(self, node):
		#sym = self.getSymbolInformation(node.idName)
		#self.addInstruction('ldr', sym[0], sym[1])
		self.loadLocation(node)

	def visit_DereferencedLocation(self, node):
		#sym = self.getSymbolInformation(node.idName)
		#self.addInstruction('lrv', sym[0], sym[1])
		self.loadLocation(node)

	def visit_StringElement(self, node):
		#sym = self.getSymbolInformation(node.idName)
		#self.addInstruction('ldr', sym[0], sym[1])
		#self.visit(node.start_element)
		#self.addInstruction('idx', 1, None)
		self.loadLocation(node)

	def visit_StringSlice(self, node):
		#self.loadSliceLocations(node)
		self.loadLocation(node)

	def visit_ArrayElement(self, node):
		self.loadLocation(node)

	def visit_ArraySlice(self, node):
		#self.loadSliceLocations(node)
		self.loadLocation(node)

	def loadSliceLocations(self, node, left_side = False):
		if isinstance(node, ast.StringElement):
			self.visit(node.start_element)
		else:
			self.addInstruction('ldc', node.literalRange.lowerBound.val, None)
			
		sym = self.environment.lookup(node.idName)
		definedLowerBound = self.getLowerBoundForMode(sym.mode)
		self.addInstruction('ldc', definedLowerBound, None)
		self.addInstruction('sub', None, None)
		self.addInstruction('idx', 1, None)
		if not left_side: self.addInstruction('grc', None, None)

	### -------------------------------------------------------------- ###

	def visit_Assignment(self, node):
		self.addComment("assignment 1")
		self.loadLocation(node.location, True)
		#print(node.expression)
		self.visit(node.expression)
		self.saveLocation(node.location)

	def visit_BinaryExpression(self, node):
		self.visit(node.operand1)
		self.visit(node.operand2)
		opcode = node.checkType.binaryOpInst.get(node.operator)
		self.addInstruction(opcode, None, None)

	def visit_UnaryExpression(self, node):
		self.visit(node.operand)
		opcode = node.checkType.unaryOpInst.get(node.operator)
		self.addInstruction(opcode, None, None)

	def visit_RelationalExpression(self, node):
		self.visit(node.operand1)
		self.visit(node.operand2)
		opcode = node.checkType.relOpInst.get(node.operator)
		self.addInstruction(opcode, None, None)

	#def visit_ConditionalExpression(self, node):

	### -------------------------------------------------------------- ###

	def visit_IntConst(self, node):
		self.addInstruction('ldc', node.val, None)

	def visit_CharConst(self, node):
		self.addInstruction('ldc', node.val, None)

	def visit_Boolean(self, node):
		self.addInstruction('ldc', node.val, None)

	#def visit_StrConst(self, node):

	#def visit_EmptyConst(self, node):

	### -------------------------------------------------------------- ###

	#def visit_ValueArrayElement(self, node):

	#def visit_ValueArraySlice(self, node):

	### -------------------------------------------------------------- ###

	#def visit_ActionStatement(self, node):

	#def visit_Label(self, node):

	#def visit_IfAction(self, node):

	#def visit_ElseIfClause(self, node):

	#def visit_ElseClause(self, node):

	#def visit_DoAction(self, node):

	#def visit_For(self, node):

	#def visit_StepEnumeration(self, node):

	#def visit_RangeEnumeration(self, node):

	#def visit_While(self, node):

	#def visit_ProcedureStmnt(self, node):
	
	def visit_BuiltinCall(self, node):
		if node.name == 'read':
			self.addInstruction('rdv', None, None)
			self.saveLocation(node.params[0].expr)
		if node.name == 'lower':
			sym = self.environment.lookup(node.params[0].expr.idName)
			lowerBound = self.getLowerBoundForMode(sym.mode)
			self.addInstruction('ldc', lowerBound, None)
		if node.name == 'upper':
			sym = self.environment.lookup(node.params[0].expr.idName)
			upperBound = self.getUpperBoundForMode(sym.mode)
			self.addInstruction('ldc', upperBound, None)
		if node.name == 'print':
			self.addComment("print")
			location = node.params[0].expr
			self.handlePrint(location)
			## TRATAR CASO PRINT INTEIRO/CHAR/String

	def handlePrint(self, location):
		self.loadLocation(location, left_side = True)
		if isinstance(location, ast.StringSlice) or isinstance(location, ast.ArraySlice) or isinstance(location, ast.StringElement) or isinstance(location, ast.ArrayElement):
			size = self.environment.countAlocSizeForLocation(location)
			self.addInstruction('lmv', size, None)
			self.addInstruction('prt', size, None)
		else:
			mode = self.environment.lookup(location.idName).mode
			if isinstance(mode, ast.ReferenceMode) or isinstance(mode, ast.DiscreteRangeMode):
				mode = mode.mode
		
			if isinstance(mode, ast.StringMode) or isinstance(mode, ast.ArrayMode):
				size = self.environment.countAlocSizeForMode(mode)
				self.addInstruction('lmv', size, None)
				self.addInstruction('prt', size, None)
			else:
				sym = self.getSymbolInformation(location.idName)
				self.addInstruction('ldv', sym[0], sym[1])
				self.addInstruction('prv', None, None)


	def getLowerBoundForMode(self, node):
		if isinstance(node, ast.DiscreteRangeMode):
			return node.literalRange.lowerBound.val
			
		elif isinstance(node, ast.ReferenceMode):
			return self.getLowerBoundForMode(node.mode)
			
		elif isinstance(node, ast.ArrayMode):
			if len(node.index_mode.index_mode_list) > 1:
				raise Exception("Lower bound of matrix??")
			else:
				return node.index_mode.index_mode_list[0].lowerBound.val
		else:
			raise Exception("Not possible to determine lower bound")

	def getUpperBoundForMode(self, node):
		if isinstance(node, ast.DiscreteRangeMode):
			return node.literalRange.upperBound.val
			
		elif isinstance(node, ast.ReferenceMode):
			return self.getLowerBoundForMode(node.mode)
			
		elif isinstance(node, ast.ArrayMode):
			if len(node.index_mode.index_mode_list) > 1:
				raise Exception("Upper bound of matrix??")
			else:
				return node.index_mode.index_mode_list[0].upperBound.val
		else:
			raise Exception("Not possible to determine upper bound")
