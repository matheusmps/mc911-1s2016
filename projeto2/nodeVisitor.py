import util.enviroment as environment
import util.ast as ast 

class NodeVisitor(object):
	def visit(self,node):
		if node:
			print("")
			node.show(recursive=False)
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			return visitor(node)
		else:
			return None

	def generic_visit(self,node):
		print("Visitor method not found")
		#node.show(recursive=False)
		#print("coord: %s" % node.coord)
		for (child, child_name) in node.children():
			self.visit(child)

	def newError(self, node, message):
		raise Exception(message)

class Visitor(NodeVisitor):
	def __init__(self):
		self.environment = environment.Environment()
		self.typemap = {
			"int": environment.IntType,
			"char": environment.CharType,
			"string": environment.StringType,
			"bool": environment.BoolType
		}

	def typeCheckUnaryExpression(self, node, op, val):
		if hasattr(val, "checkType"):
			if op not in val.checkType.unaryOperators:
				self.newError(node, "Unary operator {} not supported".format(op))
			return val.checkType

	def typeCheckBinaryExpression(self, node, op, left, right):
		if hasattr(left, "checkType") and hasattr(right, "checkType"):
			if left.checkType != right.checkType:
				self.newError(node, "Binary operator {} does not have matching types".format(op))
				return left.checkType
				
			errside = None
			if op not in left.checkType.binaryOperators:
				errside = "LHS"
			if op not in right.checkType.binaryOperators:
				errside = "RHS"
			if errside is not None:
				self.newError(node, "Binary operator {} not supported on {} of expression".format(op, errside))
		return left.checkType

	def typeCheckRelationalExpression(self, node, op, left, right):
		if hasattr(left, "checkType") and hasattr(right, "checkType"):
			if left.checkType != right.checkType:
				self.newError(node, "Relational operator {} does not have matching types".format(op))
				return left.checkType
				
			errside = None
			if op not in left.checkType.relOperators:
				errside = "LHS"
			if op not in right.checkType.relOperators:
				errside = "RHS"
			if errside is not None:
				self.newError(node, "Relational operator {} not supported on {} of expression".format(op, errside))
			return environment.BoolType

	def isInsideFunction(self):
		return self.environment.scope_level() > 1

	def checkIdIsUsed(self, idName):
		if self.environment.lookup(idName) is not None:
			self.newError(None, "Variavel '{}' ja declarada".format(idName))
			return

	def checkLocation(self,node):
		symbol = self.environment.lookup(node.idName)
		if not symbol:
			self.newError(node, "name '{}' not found".format(node.idName))
			return
		node.checkType = symbol.checkType

	def visit_Program(self, node):
		node.environment = self.environment
		node.symtab = self.environment.peek()
		for statement in node.statements:
			self.visit(statement)
			if isinstance(statement, ast.Assignment):
				self.environment.add_local(statement.location.idName, statement.expression)

	#def visit_DeclStmt(self, node):
	# nao precisa: generic

	def visit_Declaration(self, node):
		for idName in node.idList:
			self.checkIdIsUsed(idName)
			self.environment.add_local(idName, node)
			
			self.visit(node.mode)
			if hasattr(node.mode, "checkType"):
				node.checkType = node.mode.checkType

			self.visit(node.init)
			
			if node.init is not None:
				if (node.checkType != node.init.checkType):
					self.newError(node, "Cannot assign {} to {}".format(node.init.checkType, node.checkType))
					return
				
			# TODO
			#if node.init is None:
			#	default = node.check_type.default
			#	node.init = Literal(default)
			#	node.expr.checkType = node.checkType
			
			node.scopeLevel = self.environment.scope_level()

	### -------------------------------------------------------------- ###

	### MODE ###

	def visit_Mode(self, node):
		varType = self.environment.lookup(node.modeName)
		if not isinstance(varType, environment.ExprType):
			self.newError(node, "%s nao e um tipo valido" % node.modeName)
			return
		node.checkType = varType

	def visit_DiscreteMode(self, node):
		self.visit_Mode(node)

	def visit_ReferenceMode(self, node):
		self.visit(node.mode)
		node.checkType = node.mode.checkType

	def visit_DiscreteRangeMode(self, node):
		self.visit(node.mode)
		node.checkType = node.mode.checkType
		self.visit(node.literalRange)

	def visit_LiteralRange(self, node):
		self.visit(node.lowerBound)
		self.visit(node.upperBound)
		if node.lowerBound.checkType != environment.IntType:
			self.newError(node, "Lower Bound expression nao retorna um inteiro mas um %s" % node.lowerBound.checkType)
			return
		if node.upperBound.checkType != environment.IntType:
			self.newError(node, "Upper Bound expression nao retorna um inteiro mas um %s" % node.upperBound.checkType)
			return 

	def visit_StringMode(self, node):
		node.checkType = environment.StringType

	def visit_ArrayMode(self, node):
		self.visit(node.index_mode)
		self.visit(node.element_node)
		node.checkType = node.element_node.checkType

	## nao precisa: generic
	## somente precisa percorrer a index_mode_list para cada mode
	## index_mode_list pode ser um DiscreteMode ou um LiteralRange
	# def visit_IndexMode(self, node):

	### -------------------------------------------------------------- ###

	### MODE / SYN DEFINITION ###

	##### TEST #####

	def visit_ModeDef(self, node):
		for idName in node.idList:
			self.checkIdIsUsed(idName)
			self.environment.add_local(idName, node)
		self.visit(node.mode)
		node.checkType = node.mode.checkType

	#def visit_NewModeStmt(self, node):
	# generic

	def visit_SynDef(self, node):
		self.visit_ModeDef(node)
		if node.mode is None:
			self.visit(node.expression)
			node.mode = node.expression.checkType
		else:
			if node.checkType != node.expression.checkType:
				self.newError(node, "Cannot assign {} to {}".format(node.expression.checkType, node.checkType))

	### -------------------------------------------------------------- ###

	### LOCATION ###

	def visit_Location(self, node):
		self.checkLocation(node)

	def visit_ReferencedLocation(self, node):
		self.visit(node.location)
		node.idName = node.location.idName

	def visit_DereferencedLocation(self, node):
		self.visit(node.location)
		node.idName = node.location.idName

	def visit_StringElement(self, node):
		self.checkLocation(node)
		self.visit(node.start_element)
		if node.start_element.checkType != environment.IntType:
			self.newError(node, "Start element from String Element does not return an int but a %s" % node.start_element.checkType)

	def visit_StringSlice(self, node):
		self.checkLocation(node)
		self.visit(node.literalRange)

	def visit_ArrayElement(self, node):
		self.visit(node.array_location)
		for expression in node.expressions:
			self.visit(expression)

	def visit_ArraySlice(self, node):
		self.visit(node.array_location)
		self.visit(node.literalRange)

	### -------------------------------------------------------------- ###

	def visit_Assignment(self, node):
		symbol = self.environment.lookup(node.location.idName)
		if not symbol:
			self.newError(node, "name '{}' not defined".format(node.location.idName))
		
		self.visit(node.expression)
		
		#if isinstance(symbol, ast.Declaration):
		#	if hasattr(symbol, "checkType") and hasattr(node.expression, "checkType"):
		#		if symbol.checkType != node.expression.checkType:
		#			self.newError(node, "Cannot assign {} to {}".format(node.expression.checkType, symbol.checkType))
		#			return
					
		if hasattr(node.location, "checkType") and hasattr(node.expression, "checkType"):
			if node.location.checkType != node.expression.checkType:
				self.newError(node, "Cannot assign {} to {}".format(node.expression.checkType, node.location.checkType))

	#def visit_Expression(self, node):
	# generic

	def visit_UnaryExpression(self,node):
		self.visit(node.operand)
		checkType = self.typeCheckUnaryExpression(node, node.operator, node.operand)
		node.checkType = checkType

	def visit_BinaryExpression(self,node):
		self.visit(node.operand1)
		self.visit(node.operand2)
		checkType = self.typeCheckBinaryExpression(node, node.operator, node.operand1, node.operand2)
		node.checkType = checkType

	def visit_RelationalExpression(self,node):
		self.visit(node.operand1)
		self.visit(node.operand2)
		checkType = self.typeCheckRelationalExpression(node, node.operator, node.operand1, node.operand2)
		node.checkType = checkType

	def visit_ConditionalExpression(self, node):
		self.visit(node.if_expr)
		if node.if_expr.checkType != environment.BoolType:
			self.newError(node, "Expressao do IF deve retornar um boolean")
			return
		self.visit(node.then_expr)
		for clause in node.elseif_expr:
			self.visit(clause)
		self.visit(node.else_expr)

	### -------------------------------------------------------------- ###

	def visit_IntConst(self, node):
		node.checkType = environment.IntType

	def visit_CharConst(self, node):
		node.checkType = environment.CharType

	def visit_Boolean(self, node):
		node.checkType = environment.BoolType

	def visit_StrConst(self, node):
		node.checkType = environment.StringType

	#def visit_EmptyConst(self, node):
	#####@@@### Tipo empty?

	### -------------------------------------------------------------- ###

	#def visit_ValueArrayElement(self, node):

	#def visit_ValueArraySlice(self, node):

	### -------------------------------------------------------------- ###

	#def visit_ActionStatement(self, node):
	# generic

	#def visit_Label(self, node):
	# generic

	def visit_IfAction(self, node):
		self.visit(node.if_expr)
		if node.if_expr.checkType != environment.BoolType:
			self.newError(node, "Expressao do IF deve retornar um boolean")
			return
		
		for clause in node.then_clause:
			self.visit(clause)
		if node.else_clause is not None:
			for clause in node.else_clause:
				self.visit(clause)

	def visit_ElseIfClause(self, node):
		self.visit(node.test)
		if node.test.checkType != environment.BoolType:
			self.newError(node, "Expressao do ElseIF deve retornar um boolean")
			return
		for statement in node.stmts:
			self.visit(statement)

	#def visit_ElseClause(self, node):
	# não precisa, generic

	def visit_DoAction(self, node):
		for ctrl in node.control:
			self.visit(ctrl)
		#if node.control.checkType != environment.BoolType:
		#	self.newError(node, "Expressao do ElseIF deve retornar um boolean")
		#	return
		for statement in node.stmts:
			self.visit(statement)

	#def visit_For(self, node):
	# generic visit

	def visit_StepEnumeration(self, node):
		self.visit(node.counter)
		
		self.visit(node.start_value)
		if node.start_value.checkType != environment.IntType:
			self.newError(node, "Start value from FOR must be a int not a %s" % node.start_value.checkType)
			return
		
		self.visit(node.step_value)
		if node.step_value is not None:
			if node.step_value.checkType != environment.IntType:
				self.newError(node, "Step value from FOR must be a int not a %s" % node.start_value.checkType)
				return
		
		self.visit(node.end_value)
		if node.end_value.checkType != environment.IntType:
			self.newError(node, "End value from FOR must be a int not a %s" % node.start_value.checkType)
			return

	def visit_RangeEnumeration(self, node):
		self.visit(node.counter)
		self.visit(node.expression)
		if node.counter.checkType != node.expression.checkType:
			self.newError(node, "Cannot assign {} to {}".format(node.expression.checkType, node.counter.checkType))

	def visit_While(self, node):
		self.visit(node.bool_expr)
		if node.bool_expr.checkType != environment.BoolType:
			self.newError(node, "Expressao nao eh booleana")
			return

	def visit_ProcedureStmnt(self, node):
		node.scope_level = self.environment.scope_level()
		if node.scope_level > 1:
			self.newError(node, "Nested functions not implemented")
			return
		self.environment.push(node)
		if self.environment.lookup(node.label.label) is not None:
			self.newError(node, "Attempted to redefine func '{}', not allowed".format(node.label.label))
			return
		
		self.environment.add_root(node.label.label, node)
		self.visit(node.procedure_definition)
		node.param_list_size = node.procedure_definition.param_list_size
		
		if hasattr(node.procedure_definition, "checkType"):
			node.checkType = node.procedure_definition.checkType
			
		self.environment.pop()

	def visit_ProcedureDef(self, node):
		node.param_list_size = 0
		for parameter in node.formal_parameter_list:
			node.param_list_size +=  len(parameter.idList)
			self.visit(parameter)
		
		if node.result_spec is not None:
			self.visit(node.result_spec)
			node.checkType = node.result_spec.checkType
		
		for statement in node.statement_list:
			self.visit(statement)

	def visit_FormalParameter(self, node):
		self.visit(node.parameter_specs)
		node.checkType = node.parameter_specs.checkType
		
		for idName in node.idList:
			self.environment.add_local(idName, node)
			node.scope_level = self.environment.scope_level()

	def visit_ParameterSpecs(self, node):
		self.visit(node.mode)
		node.checkType = node.mode.checkType

	def visit_ResultSpecs(self, node):
		self.visit(node.mode)
		node.checkType = node.mode.checkType

	def visit_ProcedureCall(self, node):
		sym = self.environment.lookup(node.name)
		if not sym:
			self.environment.printStack()
			self.newError(node, "Function name '{}' not found".format(node.name))
			return
		if not isinstance(sym, ast.ProcedureStmnt):
			self.newError(node, "Tried to call non-function '{}'".format(node.name))
			return
		if sym.param_list_size != len(node.params):
			self.newError(node, "Number of arguments for call to function '{}' do not match function parameter declaration".format(node.name))
		
		for p in node.params:
			self.visit(p)
		
		argerrors = False
		for arg, parm in zip(node.params, sym.procedure_definition.formal_parameter_list):
			print(arg.checkType)
			print(parm.checkType)
			if arg.checkType != parm.checkType:
				newError(node, "Argument type '{}' does not match parameter type '{}' in function call to '{}'".format(arg.checkType, parm.checkType, node.name))
				argerrors = True
			if argerrors:
				return
			arg.call_arg = parm

	def visit_Parameter(self, node):
		self.visit(node.expr)
		node.checkType = node.expr.checkType

	def visit_ExitAction(self, node):
		sym = self.environment.lookup(node.label.label)
		if not sym:
			self.newError(node, "Funcao '{}' nao encontrada".format(node.label.label))
			return

	def visit_ReturnAction(self, node):
		self.visit(node.result)
		if self.environment.peek().return_type() != node.expr.check_type:
			self.newError(node, "Tipo de retorno da funcao eh diferente do esperado")

	#def visit_ResultAction(self, node):
	# generic
	
	#def visit_BuiltinCall(self, node):
	# generic
