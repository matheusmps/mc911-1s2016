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
			#buf.write('\n')
			child.show(
				buf,
				offset=offset + 2)

class Program(NodeAst):
	__slots__ = ('statements')
	
	def __init__(self, statements):
		self.statements = statements
	
	def children(self):
		nodelist = []
		for child in (self.statements or []): nodelist.append(child)
		return nodelist

class DeclStmt(NodeAst):
	__slots__ = ('decls')
	
	def __init__(self, decls):
		self.decls = decls
	
	def children(self):
		nodelist = []
		for child in (self.decls or []): nodelist.append(child)
		return nodelist

class Declaration(NodeAst):
	__slots__ = ('idList', 'mode', 'init')
	
	def __init__(self, idList, mode, init):
		self.idList = idList
		self.mode = mode
		self.init = init
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append(self.mode)
		if self.init is not None: nodelist.append(self.init)
		return nodelist
	
	attr_names = ('idList',)

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

class ReferenceMode(NodeAst):
	__slots__ = ('mode')
	
	def __init__(self, mode):
		self.mode = mode
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append(self.mode)
		return nodelist

class DiscreteRangeMode(NodeAst):
	__slots__ = ('mode', 'literalRange')
	
	def __init__(self, mode, literalRange):
		self.mode = mode
		self.literalRange = literalRange
	
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append(self.mode)
		if self.literalRange is not None: nodelist.append(self.literalRange)
		return nodelist

class LiteralRange(NodeAst):
	__slots__ = ('lowerBound', 'upperBound')
	
	def __init__(self, lowerBound, upperBound):
		self.lowerBound = lowerBound
		self.upperBound = upperBound
	
	def children(self):
		nodelist = []
		if self.lowerBound is not None: nodelist.append(self.lowerBound)
		if self.upperBound is not None: nodelist.append(self.upperBound)
		return nodelist

class StringMode(NodeAst):
	__slots__ = ('length')
	
	def __init__(self, length):
		self.length = length
		
	attr_names = ('length', )

class IndexMode(NodeAst):
	__slots__ = ('index_mode_list')
	
	def __init__(self, index_mode_list):
		self.index_mode_list = index_mode_list
		
	def children(self):
		nodelist = []
		for child in (self.index_mode_list or []): nodelist.append(child)
		return nodelist

class ArrayMode(NodeAst):
	__slots__ = ('index_mode', 'element_node')
	
	def __init__(self, index_mode, element_node):
		self.index_mode = index_mode
		self.element_node = element_node
		
	def children(self):
		nodelist = []
		if self.index_mode is not None: nodelist.append(self.index_mode)
		if self.element_node is not None: nodelist.append(self.element_node)
		return nodelist

class ModeDef(NodeAst):
	__slots__ = ('idList', 'mode')
	
	def __init__(self, idList, mode):
		self.idList = idList
		self.mode = mode
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append(self.mode)
		return nodelist
	
	attr_names = ('idList',)

class NewModeStmt(NodeAst):
	__slots__ = ('modeList')
	
	def __init__(self, modeList):
		self.modeList = modeList
	
	def children(self):
		nodelist = []
		for child in (self.modeList or []): nodelist.append(child)
		return nodelist

class SynStmt(NodeAst):
	__slots__ = ('synList')
	
	def __init__(self, synList):
		self.synList = synList
	
	def children(self):
		nodelist = []
		for child in (self.synList or []): nodelist.append(child)
		return nodelist

class SynDef(NodeAst):
	__slots__ = ('idList', 'mode', 'expression')
	
	attr_names = ('idList', )
	
	def __init__(self, idList, mode, expression):
		self.idList = idList
		self.mode = mode
		self.expression = expression
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append(self.mode)
		if self.expression is not None: nodelist.append(self.expression)
		return nodelist
		

class IntConst(NodeAst):
	__slots__ = ('val')
	
	attr_names = ('val',)
	
	def __init__(self, val):
		self.val = val

class Location(NodeAst):
	__slots__ = ('idName')
	
	attr_names = ('idName',)
	
	def __init__(self, idName):
		self.idName = idName

class DereferencedLocation(NodeAst):
	__slots__ = ('idName')
	
	attr_names = ('idName',)
	
	def __init__(self, idName):
		self.idName = idName

class StringElement(NodeAst):
	__slots__ = ('idName', 'start_element')
	
	attr_names = ('idName',)
	
	def __init__(self, idName, start_element):
		self.idName = idName
		start_element = start_element
	
	def children(self):
		nodelist = []
		if self.start_element is not None: nodelist.append(self.start_element)
		return nodelist

class StringSlice(NodeAst):
	__slots__ = ('idName', 'left', 'right')
	
	def __init__(self, idName, left, right):
		self.idName = idName
		self.left = left
		self.right = right
	
	def children(self):
		nodelist = []
		if self.left is not None: nodelist.append(self.left)
		if self.right is not None: nodelist.append(self.right)
		return nodelist

class ArrayElement(NodeAst):
	__slots__ = ('array_location', 'expressions')
	
	def __init__(self, array_location, expressions):
		self.array_location = array_location
		self.expressions = expressions
		
	def children(self):
		nodelist = []
		if self.array_location is not None: nodelist.append(self.array_location)
		for child in (self.expressions or []): nodelist.append(child)
		return nodelist

class ArraySlice(NodeAst):
	__slots__ = ('array_location', 'literalRange')
	
	def __init__(self, array_location, literalRange):
		self.array_location = array_location
		self.literalRange = literalRange
		
	def children(self):
		nodelist = []
		if self.array_location is not None: nodelist.append(self.array_location)
		if self.literalRange is not None: nodelist.append(self.literalRange)
		return nodelist

