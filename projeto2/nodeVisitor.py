from util.enviroment import Environment
from util.expressionTypes import ExprType, IntType, FloatType, StringType, BoolType

class NodeVisitor(object):
	def visit(self,node):
		if node:
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			return visitor(node)
		else:
			return None

	def generic_visit(self,node):
		print("\nVisitor method not found")
		node.show(recursive=False)
		for (child, child_name) in node.children():
			self.visit(child)


def visit_Program(self, node):

def visit_DeclStmt(self, node):

def visit_Declaration(self, node):

def visit_Mode(self, node):

def visit_DiscreteMode(self, node):

def visit_ReferenceMode(self, node):

def visit_DiscreteRangeMode(self, node):

def visit_LiteralRange(self, node):

def visit_StringMode(self, node):

def visit_IndexMode(self, node):

def visit_ArrayMode(self, node):

def visit_ModeDef(self, node):

def visit_NewModeStmt(self, node):

def visit_SynDef(self, node):
		
def visit_IntConst(self, node):

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

def visit_ActionStatement(self, node):

def visit_Label(self, node):

def visit_IfAction(self, node):

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
