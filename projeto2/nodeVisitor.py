import util.expressionTypes as expressionTypes
from util.enviroment import Environment

class NodeVisitor(object):
	def visit(self,node):
		if node:
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			return visitor(node)
		else:
			return None

	def generic_visit(self,node):
		#print("\nVisitor method not found")
		#node.show(recursive=False)
		#print("coord: %s" % node.coord)
		for (child, child_name) in node.children():
			self.visit(child)

	def newError(self, node, message):
		raise Exception("%s : %s", (node.coord, message))

class Visitor(NodeVisitor):
	def __init__(self):
		self.environment = Environment()
		self.typemap = {
			"int": expressionTypes.IntType,
			"char": expressionTypes.CharType,
			"string": expressionTypes.StringType,
			"bool": expressionTypes.BoolType
		}

	def typeCheckUnaryExpression(self, node, op, val):
		if hasattr(val, "checkType"):
			if op not in val.checkType.unaryOperators:
				newError(node, "Unary operator {} not supported".format(op))
			return val.checkType

	def typeCheckBinaryExpression(self, node, op, left, right):
		if hasattr(left, "checkType") and hasattr(right, "checkType"):
			if left.checkType != right.checkType:
				newError(node, "Binary operator {} does not have matching types".format(op))
				return left.checkType
				
			errside = None
			if op not in left.checkType.binaryOperators:
				errside = "LHS"
			if op not in right.checkType.binaryOperators:
				errside = "RHS"
			if errside is not None:
				newError(node, "Binary operator {} not supported on {} of expression".format(op, errside))
		return left.checkType

	def typeCheckRelationalExpression(self, node, op, left, right):
		if hasattr(left, "checkType") and hasattr(right, "checkType"):
			if left.checkType != right.checkType:
				newError(node, "Relational operator {} does not have matching types".format(op))
				return left.checkType
				
			errside = None
			if op not in left.checkType.relOperators:
				errside = "LHS"
			if op not in right.checkType.relOperators:
				errside = "RHS"
			if errside is not None:
				newError(node, "Relational operator {} not supported on {} of expression".format(op, errside))
			return BoolType

	def isInsideFunction(self):
		return self.environment.scope_level() > 1

def visit_Program(self, node):

# nao precisa: generic
def visit_DeclStmt(self, node):

def visit_Declaration(self, node):
	# id_list: array the strings ID's
	# mode: Mode, DiscreteMode, DiscreteRangeMode, LiteralRange, ReferenceMode, StringMode, IndexMode, ArrayMode
	# initialization: expression

### MODE ###

##### TEST #####
def visit_Mode(self, node):
	varType = self.environment.lookup(node.modeName)
	if not isinstance(varType, ExprType):
		newError(node, "%s nao e um tipo valido" % node.modeName)
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
	if node.lowerBound.checkType != expressionTypes.IntType:
		newError(node, "Lower Bound expression nao retorna um inteiro mas um %s" % node.lowerBound.checkType)
	if node.upperBound.checkType != expressionTypes.IntType
		newError(node, "Upper Bound expression nao retorna um inteiro mas um %s" % node.upperBound.checkType)

def visit_StringMode(self, node):
	node.checkType = expressionTypes.StringType

def visit_ArrayMode(self, node):
	self.visit(node.index_mode)
	self.visit(node.element_node)
	node.checkType = node.element_node.checkType

## nao precisa: generic
## somente precisa percorrer a index_mode_list para cada mode
## index_mode_list pode ser um DiscreteMode ou um LiteralRange
# def visit_IndexMode(self, node):

### --- ###

### MODE / SYN DEFINITION ###

def visit_ModeDef(self, node):

def visit_NewModeStmt(self, node):

def visit_SynDef(self, node):

### LOCATION ###

def visit_Location(self, node):

def visit_ReferencedLocation(self, node):

def visit_DereferencedLocation(self, node):

def visit_StringElement(self, node):

def visit_StringSlice(self, node):

def visit_ArrayElement(self, node):

def visit_ArraySlice(self, node):

def visit_Assignment(self, node):

def visit_Expression(self, node):

def visit_ParenthesizedExpression(self, node):

def visit_ConditionalExpression(self, node):

def visit_IntConst(self, node):

def visit_CharConst(self, node):

def visit_Boolean(self, node):

def visit_StrConst(self, node):

def visit_EmptyConst(self, node):

def visit_ValueArrayElement(self, node):

def visit_ValueArraySlice(self, node):

### --- ###

def visit_ActionStatement(self, node):

def visit_Label(self, node):

def visit_IfAction(self, node):
	if not self.inside_function():
		newError(node, "Nao e possivel user IF fora do corpo de uma funcao")
		return
	self.visit(node.if_expr)
	if node.expr.checkType != BoolType:
		newError(node, "Expressao do IF deve retornar um boolean")
	self.visit(node.then_clause)
	if node.else_clause is not None:
		self.visit(node.else_clause)

def visit_ElseIfClause(self, node):

def visit_ElseClause(self, node):

def visit_DoAction(self, node):

def visit_For(self, node):

def visit_StepEnumeration(self, node):

def visit_RangeEnumeration(self, node):

def visit_While(self, node):

def visit_ProcedureStmnt(self, node):

def visit_ProcedureDef(self, node):

def visit_FormalParameter(self, node):

def visit_ParameterSpecs(self, node):

def visit_ResultSpecs(self, node):

def visit_ProcedureCall(self, node):

def visit_Parameter(self, node):

def visit_ExitAction(self, node):

def visit_ReturnAction(self, node):

def visit_ResultAction(self, node):

def visit_BuiltinCall(self, node):
