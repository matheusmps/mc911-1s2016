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
			buf.write(lead + ' <' + _my_node_name + '>: ' + self.__class__.__name__ + ' => ')
		else:
			buf.write(lead + self.__class__.__name__+ ' => ')

		if self.attr_names:
			nvlist = [(n, getattr(self,n)) for n in self.attr_names]
			attrstr = ', '.join('%s = \'%s\' ' % nv for nv in nvlist)
			buf.write(attrstr)

		buf.write('\n')

		for (child, child_name) in self.children():
			#buf.write('\n')
			child.show(
				buf,
				offset=offset + 2,
				_my_node_name=child_name)

class Program(NodeAst):
	__slots__ = ('statements')
	
	def __init__(self, statements):
		self.statements = statements
	
	def children(self):
		nodelist = []
		for child in (self.statements or []): nodelist.append((child, "stmt"))
		return nodelist

class DeclStmt(NodeAst):
	__slots__ = ('decls')
	
	def __init__(self, decls):
		self.decls = decls
	
	def children(self):
		nodelist = []
		for child in (self.decls or []): nodelist.append((child, "decls"))
		return nodelist

class Declaration(NodeAst):
	__slots__ = ('idList', 'mode', 'init')
	
	def __init__(self, idList, mode, init):
		self.idList = idList
		self.mode = mode
		self.init = init
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		if self.init is not None: nodelist.append((self.init, "initialization"))
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
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		return nodelist

class DiscreteRangeMode(NodeAst):
	__slots__ = ('mode', 'literalRange')
	
	def __init__(self, mode, literalRange):
		self.mode = mode
		self.literalRange = literalRange
	
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		if self.literalRange is not None: nodelist.append((self.literalRange, "range"))
		return nodelist

class LiteralRange(NodeAst):
	__slots__ = ('lowerBound', 'upperBound')
	
	def __init__(self, lowerBound, upperBound):
		self.lowerBound = lowerBound
		self.upperBound = upperBound
	
	def children(self):
		nodelist = []
		if self.lowerBound is not None: nodelist.append((self.lowerBound, "lowerBound"))
		if self.upperBound is not None: nodelist.append((self.upperBound, "upperBound"))
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
		for child in (self.index_mode_list or []): nodelist.append((child, "index_mode_list"))
		return nodelist

class ArrayMode(NodeAst):
	__slots__ = ('index_mode', 'element_node')
	
	def __init__(self, index_mode, element_node):
		self.index_mode = index_mode
		self.element_node = element_node
		
	def children(self):
		nodelist = []
		if self.index_mode is not None: nodelist.append((self.index_mode, "index_mode"))
		if self.element_node is not None: nodelist.append((self.element_node, "element_mode"))
		return nodelist

class ModeDef(NodeAst):
	__slots__ = ('idList', 'mode')
	
	def __init__(self, idList, mode):
		self.idList = idList
		self.mode = mode
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		return nodelist
	
	attr_names = ('idList',)

class NewModeStmt(NodeAst):
	__slots__ = ('modeList')
	
	def __init__(self, modeList):
		self.modeList = modeList
	
	def children(self):
		nodelist = []
		for child in (self.modeList or []): nodelist.append((child, "mode_list"))
		return nodelist

class SynStmt(NodeAst):
	__slots__ = ('synList')
	
	def __init__(self, synList):
		self.synList = synList
	
	def children(self):
		nodelist = []
		for child in (self.synList or []): nodelist.append((child, "syn_list"))
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
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		if self.expression is not None: nodelist.append((self.expression, "expression"))
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

class ReferencedLocation(NodeAst):
	__slots__ = ('location')
	
	def __init__(self, location):
		self.location = location
		
	def children(self):
		nodelist = []
		if self.location is not None: nodelist.append((self.location, "location"))
		return nodelist

class DereferencedLocation(NodeAst):
	__slots__ = ('location')
	
	def __init__(self, location):
		self.location = location
		
	def children(self):
		nodelist = []
		if self.location is not None: nodelist.append((self.location, "location"))
		return nodelist

class StringElement(NodeAst):
	__slots__ = ('idName', 'start_element')
	
	def __init__(self, idName, start_element):
		self.idName = idName
		self.start_element = start_element
	
	def children(self):
		nodelist = []
		if self.idName is not None: nodelist.append((self.idName, "id"))
		if self.start_element is not None: nodelist.append((self.start_element, "start_element"))
		return nodelist

class StringSlice(NodeAst):
	__slots__ = ('idName', 'literalRange')
	
	def __init__(self, idName, literalRange):
		self.idName = idName
		self.literalRange = literalRange
	
	def children(self):
		nodelist = []
		if self.idName is not None: nodelist.append((self.idName, "id"))
		if self.literalRange is not None: nodelist.append((self.literalRange, "range"))
		return nodelist

class ArrayElement(NodeAst):
	__slots__ = ('array_location', 'expressions')
	
	def __init__(self, array_location, expressions):
		self.array_location = array_location
		self.expressions = expressions
		
	def children(self):
		nodelist = []
		if self.array_location is not None: nodelist.append((self.array_location, "array_location"))
		for child in (self.expressions or []): nodelist.append((child, "expressions"))
		return nodelist

class ArraySlice(NodeAst):
	__slots__ = ('array_location', 'literalRange')
	
	def __init__(self, array_location, literalRange):
		self.array_location = array_location
		self.literalRange = literalRange
		
	def children(self):
		nodelist = []
		if self.array_location is not None: nodelist.append((self.array_location, "array_location"))
		if self.literalRange is not None: nodelist.append((self.literalRange, "range"))
		return nodelist

class Assignment(NodeAst):
	__slots__ = ('location', 'assign_op', 'expression')
	
	def __init__(self, location, assign_op, expression):
		self.location = location
		self.assign_op = assign_op
		self.expression = expression
	
	attr_names = ('assign_op', )
	
	def children(self):
		nodelist = []
		if self.location is not None: nodelist.append((self.location, "location"))
		if self.expression is not None: nodelist.append((self.expression, "expression"))
		return nodelist

class Expression(NodeAst):
	__slots__ = ('operand1', 'operator', 'operand2')
	
	def __init__(self, operand1, operator, operand2):
		self.operand1 = operand1
		self.operator = operator
		self.operand2 = operand2
	
	attr_names = ('operator',)
	
	def children(self):
		nodelist = []
		if self.operand1 is not None: nodelist.append((self.operand1, "operand1"))
		if self.operand2 is not None: nodelist.append((self.operand2, "operand2"))
		return nodelist

class ParenthesizedExpression(NodeAst):
	__slots__ = ('expression')
	
	def __init__(self, operand1, operator, operand2):
		self.expression = expression
	
	def children(self):
		nodelist = []
		if self.expression is not None: nodelist.append((self.expression, "expressions"))
		return nodelist


class IntConst(NodeAst):
	__slots__ = ('val')
	attr_names = ('val',)
	
	def __init__(self, val):
		self.val = val

class CharConst(NodeAst):
	__slots__ = ('val')
	attr_names = ('val',)
	
	def __init__(self, val):
		self.val = val

class Boolean(NodeAst):
	__slots__ = ('val')
	attr_names = ('val',)
	
	def __init__(self, val):
		self.val = val

class StrConst(NodeAst):
	__slots__ = ('val')
	attr_names = ('val',)
	
	def __init__(self, val):
		self.val = val

class EmptyConst(NodeAst):
	__slots__ = ()
	attr_names = ()

class ValueArrayElement(NodeAst):
	__slots__ = ('primitiveValue', 'expressions')
	
	def __init__(self, primitiveValue, expressions):
		self.primitiveValue = primitiveValue
		self.expressions = expressions
		
	def children(self):
		nodelist = []
		if self.primitiveValue is not None: nodelist.append((self.primitiveValue, "primitiveValue"))
		for child in (self.expressions or []): nodelist.append((child, "expressions"))
		return nodelist

class ValueArraySlice(NodeAst):
	__slots__ = ('primitiveValue', 'literalRange')
	
	def __init__(self, primitiveValue, literalRange):
		self.primitiveValue = primitiveValue
		self.literalRange = literalRange
		
	def children(self):
		nodelist = []
		if self.primitiveValue is not None: nodelist.append((self.primitiveValue, "primitiveValue"))
		if self.literalRange is not None: nodelist.append((self.literalRange, "range"))
		return nodelist
