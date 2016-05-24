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
