import sys

class NodeAst(object):
	"""
	Base class example for the AST nodes.  Each node is expected to
	define the _fields attribute which lists the names of stored
	attributes.   The __init__() method below takes positional
	arguments and assigns them to the appropriate fields.  Any
	additional arguments specified as keywords are also assigned.
	"""
	__slots__ = ()
	
	attr_names = ()
	
	def children(self):
		""" A sequence of all children that are Nodes"""
		return tuple([])
	
	def show(self, buf=sys.stdout, offset=0, _my_node_name=None):
		
		lead = ' ' * offset
		if _my_node_name is not None:
			buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
		else:
			buf.write(lead + self.__class__.__name__+ ': ')

		if self.attr_names:
			nvlist = [(n, getattr(self,n)) for n in self.attr_names]
			attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
			buf.write(attrstr)

		buf.write('\n')

		for child in self.children():
			buf.write('\n')
			child.show(
				buf,
				offset=offset + 2)

class Program(NodeAst):
	__slots__ = ('statements')
	
	def __init__(self, statements):
		self.statements = statements
	
	def children(self):
		nodelist = []
		for i, child in enumerate(self.statements or []):
			nodelist.append(child)
		return tuple(nodelist)

class DeclStmt(NodeAst):
	__slots__ = ('decls')
	
	def __init__(self, decls):
		self.decls = decls
	
	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(child)
		return tuple(nodelist)
	
class Declaration(NodeAst):
	__slots__ = ('idList', 'mode', 'init')
	
	def __init__(self, idList, mode, init):
		self.idList = idList
		self.mode = mode
		self.init = init
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append(self.mode)
		return tuple(nodelist)
	
	attr_names = ('idList', 'init')
	
class Mode(NodeAst):
	__slots__ = ('modeName')
	
	def __init__(self, modeName):
		self.modeName = modeName
		
	attr_names = ('modeName', )
	
class DiscreteMode(NodeAst):
	__slots__ = ('modeName')
	
	def __init__(self, modeName):
		self.modeName = modeName
		
	attr_names = ('modeName', )
	
class DiscreteRangeMode(NodeAst):
	__slots__ = ('mode', 'literalRange')
	
	def __init__(self, mode, literalRange):
		self.mode = mode
		self.literalRange = literalRange
	
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append(self.mode)
		if self.literalRange is not None: nodelist.append(self.literalRange)
		return tuple(nodelist)
	
class LiteralRange(NodeAst):
	__slots__ = ('lowerBound', 'upperBound')
	
	def __init__(self, lowerBound, upperBound):
		self.lowerBound = lowerBound
		self.upperBound = upperBound
	
	attr_names = ('lowerBound', 'upperBound')