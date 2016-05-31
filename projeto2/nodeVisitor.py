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
		raise Exception("%s : %s" % (node.coord, message))

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
			return BoolType

	def isInsideFunction(self):
		return self.environment.scope_level() > 1

	def visit_Program(self, node):
		node.environment = self.environment
		node.symtab = self.environment.peek()
		for statement in node.statements:
			self.visit(statement)
			if isinstance(statement, ast.Assignment):
				self.environment.add_local(statement.location.idName, statement.expression)

	# nao precisa: generic
	#def visit_DeclStmt(self, node):

	def visit_Declaration(self, node):
		# id_list: array the strings ID's
		# mode: Mode, DiscreteMode, DiscreteRangeMode, LiteralRange, ReferenceMode, StringMode, IndexMode, ArrayMode
		# initialization: expression
		
		for idName in node.idList:
			if self.environment.lookup(idName) is not None:
				self.newError(node, "Variavel {} ja declarada")
				return
			self.environment.add_local(idName, node)
			self.visit(node.mode)

			if hasattr(node.mode, "checkType"):
				node.checkType = node.mode.checkType

			self.visit(node.init)
			#if node.init is None:
			#	default = node.check_type.default
			#	node.init = Literal(default)
			#	node.expr.checkType = node.checkType
			node.scopeLevel = self.environment.scope_level()

	### -------------------------------------------------------------- ###

	### MODE ###

	##### TEST #####
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
		if node.upperBound.checkType != environment.IntType:
			self.newError(node, "Upper Bound expression nao retorna um inteiro mas um %s" % node.upperBound.checkType)

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

	#def visit_ModeDef(self, node):

	#def visit_NewModeStmt(self, node):

	#def visit_SynDef(self, node):

	### -------------------------------------------------------------- ###

	### LOCATION ###

	#def visit_Location(self, node):

	#def visit_ReferencedLocation(self, node):

	#def visit_DereferencedLocation(self, node):

	#def visit_StringElement(self, node):

	#def visit_StringSlice(self, node):

	#def visit_ArrayElement(self, node):

	#def visit_ArraySlice(self, node):

	### -------------------------------------------------------------- ###

	def visit_Assignment(self, node):

		# 1. Make sure the location of the assignment is defined
		sym = self.environment.lookup(node.location.idName)
		if not sym:
			self.newError(node, "name '{}' not defined".format(node.location.idName))
			
		# 2. Check that assignment is allowed
		self.visit(node.expression)
		
		if isinstance(sym, ast.Declaration):
			# empty var declaration, so check against the declared type name
			if hasattr(sym, "checkType") and hasattr(node.expression, "checkType"):
				if sym.checkType != node.expression.checkType:
					self.newError(node, "Cannot assign {} to {}".format(node.expression.checkType, sym.checkType))
					return
		
		#if isinstance(sym, ConstDeclaration):
		#	newError(node.lineno, "Cannot assign to constant {}".format(sym.name))
		#	return
		
		# 3. Check that the types match
		if hasattr(node.location, "checkType") and hasattr(node.expression, "checkType"):
			if node.location.checkType != node.expression.checkType:
				self.newError(node, "Cannot assign {} to {}".format(node.expression.checkType, node.location.checkType))

	# generic
	#def visit_Expression(self, node):

	#def visit_ParenthesizedExpression(self, node):

	#def visit_ConditionalExpression(self, node):

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

	# generic
	#def visit_ActionStatement(self, node):

	# generic
	#def visit_Label(self, node):

	def visit_IfAction(self, node):
		self.visit(node.if_expr)
		if node.expr.checkType != BoolType:
			self.newError(node, "Expressao do IF deve retornar um boolean")
		self.visit(node.then_clause)
		if node.else_clause is not None:
			self.visit(node.else_clause)

	#def visit_ElseIfClause(self, node):

	#def visit_ElseClause(self, node):

	#def visit_DoAction(self, node):

	#def visit_For(self, node):

	#def visit_StepEnumeration(self, node):

	#def visit_RangeEnumeration(self, node):

	def visit_While(self, node):
		if node.expr.check_type != BoolType:
			self.newError(node, "Expressao nao eh booleana")
			return
		self.visit(node.bool_expr)

	#def visit_ProcedureStmnt(self, node):

	#def visit_ProcedureDef(self, node):

	#def visit_FormalParameter(self, node):

	#def visit_ParameterSpecs(self, node):

	#def visit_ResultSpecs(self, node):

	#def visit_ProcedureCall(self, node):

	#def visit_Parameter(self, node):

	#def visit_ExitAction(self, node):

	def visit_ReturnAction(self, node):
		self.visit(node.result)
		if self.environment.peek().return_type() != node.expr.check_type:
			self.newError(node, "Tipo de retorno da funcao eh diferente do esperado")

	#def visit_ResultAction(self, node):

	#def visit_BuiltinCall(self, node):
