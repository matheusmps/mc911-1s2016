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
			print("(", end="")
			for value in val:
				if value is not None:
					print("'%s'" % value, end=",")
			print(")")

	def addInstruction(self, opcode, operand1, operand2):
		inst = (opcode, operand1, operand2)
		self.program.append(inst)

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

	def visit_Program(self, node):
		self.environment = node.environment
		node.environment.printStack()
		self.addInstruction('stp', None, None)
		self.addInstruction('alc', self.calculateSizeAloc(node), None)
		for statement in node.statements:
			self.visit(statement)

	#def visit_DeclStmt(self, node):

	def visit_Declaration(self, node):
		for name in node.idList:
			if node.init is not None:
				self.visit(node.init)
				sym = self.getSymbolInformation(name)
				self.addInstruction('stv', sym[0], sym[1])

	### -------------------------------------------------------------- ###

	### MODE ###

	#def visit_Mode(self, node):

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
		sym = self.getSymbolInformation(node.idName)
		self.addInstruction('ldv', sym[0], sym[1])

	def visit_ReferencedLocation(self, node):
		sym = self.getSymbolInformation(node.idName)
		self.addInstruction('ldr', sym[0], sym[1])

	def visit_DereferencedLocation(self, node):
		sym = self.getSymbolInformation(node.idName)
		self.addInstruction('lrv', sym[0], sym[1])

	def visit_StringElement(self, node):
		sym = self.getSymbolInformation(node.idName)
		self.addInstruction('ldr', sym[0], sym[1])
		self.visit(node.start_element)
		self.addInstruction('idx', 1, None)

	#def visit_StringSlice(self, node):

	#def visit_ArrayElement(self, node):

	#def visit_ArraySlice(self, node):

	### -------------------------------------------------------------- ###
	
	def loadLocation(self, node):
		if isinstance(node, ast.StringElement) or isinstance(node, ast.StringSlice) or isinstance(node, ast.ArrayElement) or isinstance(node, ast.ArraySlice):
			self.visit(node)

	def saveLocation(self, node):
		if isinstance(node, ast.StringElement):
			self.addInstruction('smv', 1, None) 
		#elif isinstance(node, ast.StringSlice): 
		#elif isinstance(node, ast.ArrayElement): 
		#elif isinstance(node, ast.ArraySlice):
		else:
			sym = self.getSymbolInformation(node.idName)
			self.addInstruction('stv', sym[0], sym[1])

	def visit_Assignment(self, node):
		self.loadLocation(node.location)
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

