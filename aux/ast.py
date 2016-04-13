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

        #if showcoord:
        #    buf.write(' (at %s)' % self.coord)
		buf.write('\n')

		for (child_name, child) in self.children():
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
		for i, child in enumerate(self.statements or []):
			nodelist.append(("statement[%d]" % i, child))
		return tuple(nodelist)

class DeclStmt(NodeAst):
	__slots__ = ('decls')
	
	def __init__(self, decls):
		self.decls = decls
	
	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)
	
class Declaration(NodeAst):
	__slots__ = ('idList', 'mode', 'init')
	
	def __init__(self, idList, mode, init):
		self.idList = idList
		self.mode = mode
		self.init = init
	
	attr_names = ('idList', 'mode', 'init')
