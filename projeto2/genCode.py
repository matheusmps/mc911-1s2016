import nodeVisitor
import util.ast as ast
import enviroment as environment

class CodeGenerator(nodeVisitor.NodeVisitor):
	
	def __init__(self):
		self.program = []
		self.environment = None
	
	def printInstructions(self):
		print("\n\n")
		print(" ---- INSTRUCTIONS ----\n")
		print(" ###     Powered by      ###\n ### Fusion Energy Drink ###\n")
		for val in self.program:
			if type(val) is not tuple:
				print(val)
			else:
				print("(", end="")
				for i, value in enumerate(val):
					if value is not None:
						if i == 0:
							print("'%s'" % value, end="")
						else:
							print(", %s" % value, end="")
				print(")")

	def addInstruction(self, opcode, operand1, operand2):
		inst = (opcode, operand1, operand2)
		self.program.append(inst)

	def addComment(self, message):
		self.program.append("\n ### %s ###" % message)

	def calculateSizeAloc(self, node):
		counter = 0
		for key, value in node.symtab.items():
			declNode = value.get("node")
			if isinstance(declNode, ast.Declaration):
				counter = counter + self.environment.countAlocSizeForMode(declNode.mode)
			elif isinstance(declNode, ast.SynDef):
				if declNode.mode is not None:
					counter = counter + self.environment.countAlocSizeForMode(declNode.mode)
				else:
					counter = counter + 1;
			else:
				counter = counter + 1;
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
			
			if isinstance(node, ast.StringSlice) or isinstance(node, ast.ArraySlice) or isinstance(node, ast.StringElement):
				self.loadSliceLocations(node, left_side)
			elif isinstance(node, ast.ArrayElement):
				## TODO
				pass
		
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
		
		if not left_side and isinstance(node, ast.StringElement): 
			self.addInstruction('grc', None, None)

	def saveLocation(self, node):
		if isinstance(node, ast.StringElement) or isinstance(node, ast.StringSlice) or isinstance(node, ast.ArraySlice) or isinstance(node, ast.ArrayElement):
			## FIX
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
		aloc_size = self.calculateSizeAloc(node)
		self.addInstruction('alc', aloc_size, None)
		for statement in node.statements:
			self.visit(statement)
		self.addInstruction('dlc', aloc_size, None)
		self.addInstruction('end', None, None)

	#def visit_DeclStmt(self, node):
	#generic

	def visit_Declaration(self, node):
		for name in node.idList:
			if node.init is not None:
				self.addComment("declaration: %s" % name)
				self.visit(node.init)
				auxNode = ast.Location(name, None)
				self.saveLocation(auxNode)

	### -------------------------------------------------------------- ###

	### MODE ###

	#def visit_Mode(self, node):
	# generic

	#def visit_DiscreteMode(self, node):
	# generic

	#def visit_ReferenceMode(self, node):
	# generic

	#def visit_DiscreteRangeMode(self, node):
	# generic

	#def visit_LiteralRange(self, node):
	# generic

	#def visit_StringMode(self, node):
	# generic

	# def visit_ArrayMode(self, node):
	# como saber quanto de memoria sera alocado
	# se as expressoes sao avaliadas em tempo de execucao

	# def visit_IndexMode(self, node):
	# generic

	### -------------------------------------------------------------- ###

	### MODE / SYN DEFINITION ###

	def visit_ModeDef(self, node):
		## FIX
		pass

	#def visit_NewModeStmt(self, node):
	# generic

	def visit_SynDef(self, node):
		for name in node.idList:
			self.addComment("syn def: %s" % name)
			self.visit(node.expression)
			auxNode = ast.Location(name, None)
			self.saveLocation(auxNode)

	### -------------------------------------------------------------- ###

	### LOCATION ###

	def visit_Location(self, node):
		self.loadLocation(node)

	def visit_ReferencedLocation(self, node):
		self.loadLocation(node)

	def visit_DereferencedLocation(self, node):
		self.loadLocation(node)

	def visit_StringElement(self, node):
		self.loadLocation(node)

	def visit_StringSlice(self, node):
		self.loadLocation(node)

	def visit_ArrayElement(self, node):
		self.loadLocation(node)

	def visit_ArraySlice(self, node):
		self.loadLocation(node)

	### -------------------------------------------------------------- ###

	def visit_Assignment(self, node):
		self.addComment("assignment: %s" % node.location.idName)
		self.loadLocation(node.location, True)
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
		## type was checked during semantic
		opcode = node.operand1.checkType.relOpInst.get(node.operator)
		if opcode is not None:
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
	## TODO

	#def visit_EmptyConst(self, node):
	## TODO

	### -------------------------------------------------------------- ###

	#def visit_ValueArrayElement(self, node):
	## ???

	#def visit_ValueArraySlice(self, node):
	## ???

	### -------------------------------------------------------------- ###

	#def visit_ActionStatement(self, node):
	# generic

	#def visit_Label(self, node):

	def visit_IfAction(self, node):
		self.addComment("if")
		
		self.visit(node.if_expr)
		
		current_label = self.environment.getLabel()
		fi_label = current_label + 1
		
		if node.else_clause is not None:
			## valor da label final (fi)
			fi_label = fi_label + len(node.else_clause)
			
			## jump para a proxima label (caso falso)
			self.addInstruction('jof', current_label + 1, None)
			
			## label de cada statement
			for clause in node.else_clause:
				new_label = self.environment.addLabel()
				clause.label = new_label
			
			## label do FI
			self.environment.addLabel()
			
			## resolvo then (caso true)
			if node.then_clause is not None:
				for statement in node.then_clause:
					self.visit(statement)
					
			## pula para fi
			self.addInstruction('jmp', fi_label, None)
			
			for clause in node.else_clause:
				self.visit(clause)
				self.addInstruction('jmp', fi_label, None)
		else:
			self.addInstruction('jof', fi_label, None)
			if node.then_clause is not None:
				for statement in node.then_clause:
					self.visit(statement)
		
		self.addInstruction('lbl', fi_label, None)

	def visit_ElseIfClause(self, node):
		self.addComment("else if")
		self.addInstruction('lbl', node.label, None)
		self.visit(node.test)
		self.addInstruction('jof', node.label + 1, None)
		
		if node.stmts is not None:
			for statement in node.stmts:
				self.visit(statement)

	def visit_ElseClause(self, node):
		self.addComment("else")
		self.addInstruction('lbl', node.label, None)
		if node.stmts is not None:
			for statement in node.stmts:
				self.visit(statement)

	def visit_DoAction(self, node):
		if node.control is not None:
			
			do_label = self.environment.addLabel()
			od_label = self.environment.addLabel()
			
			if len(node.control) == 1:
				self.handleControl(node, node.control[0], do_label, od_label)
			else:
				controlFor = node.control[0]
				controlWhile = node.control[1]
				
				# init for
				self.initializeCondition(controlFor.iteration)
				
				# DO label
				self.addInstruction('lbl', do_label, None)
				
				## check while expression
				self.visit(controlWhile.bool_expr)
				
				# control jump
				self.addInstruction('jof', od_label, None)
				
				# statements
				if node.stmts is not None:
					for statement in node.stmts:
						self.visit(statement)
				
				# update and test
				self.updateAndTestCondition(controlFor.iteration)
				
				# control jumps
				self.addInstruction('jof', od_label, None)
				self.addInstruction('jmp', do_label, None)
				
				# OD label
				self.addInstruction('lbl', od_label, None)

	def handleControl(self, doActionNode, controlNode, do_label, od_label):
		if isinstance(controlNode, ast.For):
			
			# initialize
			self.initializeCondition(controlNode.iteration)
			
			# DO label
			self.addInstruction('lbl', do_label, None)
			
			# statements
			if doActionNode.stmts is not None:
				for statement in doActionNode.stmts:
					self.visit(statement)
			
			# update and test
			self.updateAndTestCondition(controlNode.iteration)
			
			# control jumps
			self.addInstruction('jof', od_label, None)
			self.addInstruction('jmp', do_label, None)
			
			## OD label
			self.addInstruction('lbl', od_label, None)
		
		else: ## while
			
			## DO label
			self.addInstruction('lbl', do_label, None)
			
			## check expression
			self.visit(controlNode.bool_expr)
			
			# control jump
			self.addInstruction('jof', od_label, None)
			
			# statements
			if doActionNode.stmts is not None:
				for statement in doActionNode.stmts:
					self.visit(statement)
			
			# control jump
			self.addInstruction('jmp', do_label, None)
			
			# OD label
			self.addInstruction('lbl', od_label, None)

	def initializeCondition(self, node):
		if isinstance(node, ast.StepEnumeration):
			auxNode = ast.Assignment(node.counter, "=", node.start_value, None)
			self.visit(auxNode)
		else:
			pass

	def updateAndTestCondition(self, node):
		if isinstance(node, ast.StepEnumeration):
			if node.step_value is None:
				step_value = ast.IntConst(1, None)
			else:
				step_value = node.step_value
			
			if node.down:
				updateExpr = ast.BinaryExpression(node.counter, "-", step_value, None)
				testNode = ast.RelationalExpression(node.counter, ">=", node.end_value, None)
			else:
				updateExpr = ast.BinaryExpression(node.counter, "+", step_value, None)
				testNode = ast.RelationalExpression(node.counter, "<=", node.end_value, None)
			
			## update
			self.addComment("update step enum")
			updateExpr.checkType = environment.IntType
			updateNode = ast.Assignment(node.counter, "=", updateExpr, None)
			self.visit(updateNode)
			
			## test
			self.addComment("test step enum")
			testNode.checkType = environment.IntType
			self.visit(testNode)
			
		else:
			pass


	# def visit_For(self, node):
	# handle in DoAction
	
	#def visit_While(self, node):
	# handle in DoAction

	#def visit_StepEnumeration(self, node):
	# handle in DoAction

	#def visit_RangeEnumeration(self, node):
	# handle in DoAction

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
				self.newError("Lower bound of matrix??")
			else:
				return node.index_mode.index_mode_list[0].lowerBound.val
		else:
			self.newError("Not possible to determine lower bound")

	def getUpperBoundForMode(self, node):
		if isinstance(node, ast.DiscreteRangeMode):
			return node.literalRange.upperBound.val
			
		elif isinstance(node, ast.ReferenceMode):
			return self.getLowerBoundForMode(node.mode)
			
		elif isinstance(node, ast.ArrayMode):
			if len(node.index_mode.index_mode_list) > 1:
				self.newError("Upper bound of matrix??")
			else:
				return node.index_mode.index_mode_list[0].upperBound.val
		else:
			self.newError("Not possible to determine upper bound")
