class NodeVisitor(object):
	"""
	Class for visiting nodes of the parse tree.  This is modeled after
	a similar class in the standard library ast.NodeVisitor.  For each
	node, the visit(node) method calls a method visit_NodeName(node)
	which should be implemented in subclasses.  The generic_visit() method
	is called for all nodes where there is no matching visit_NodeName()
	method.
	Here is a example of a visitor that examines binary operators:
	class VisitOps(NodeVisitor):
		visit_Binop(self,node):
			print("Binary operator", node.op)
			self.visit(node.left)
			self.visit(node.right)
		visit_Unaryop(self,node):
			print("Unary operator", node.op)
			self.visit(node.expr)
	tree = parse(txt)
	VisitOps().visit(tree)
	"""

	def visit(self,node):
		"""
		Execute a method of the form visit_NodeName(node) where
		NodeName is the name of the class of a particular node.
		"""
		if node:
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			return visitor(node)
		else:
			return None

	def generic_visit(self,node):
		"""
		Method executed if no applicable visit_ method can be found.
		This examines the node to see if it has _fields, is a list,
		or can be further traversed.
		"""
		print("\nVisitor method not found")
		node.show()
		for (child, child_name) in node.children():
			self.visit(child)
