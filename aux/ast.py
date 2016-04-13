import sys

class NodeAst(object):
	"""
	Base class example for the AST nodes.  Each node is expected to
	define the _fields attribute which lists the names of stored
	attributes.   The __init__() method below takes positional
	arguments and assigns them to the appropriate fields.  Any
	additional arguments specified as keywords are also assigned.
	"""
	
	_fields = []
	
	def __init__(self,*args,**kwargs):
		assert len(args) == len(self._fields)
		for name,value in zip(self._fields,args):
			setattr(self,name,value)
		# Assign additional keyword arguments if supplied
		for name,value in kwargs.items():
			setattr(self,name,value)
			
	def children(self):
		""" A sequence of all children that are Nodes"""
		pass
	
	def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
		""" Pretty print the Node and all its attributes and
			children (recursively) to a buffer.
			buf:
				Open IO buffer into which the Node is printed.
			offset:
				Initial offset (amount of leading spaces)
			attrnames:
				True if you want to see the attribute names in
				name=value pairs. False to only see the values.
			nodenames:
				True if you want to see the actual node names
				within their parents.
			showcoord:
				Do you want the coordinates of each Node to be
				displayed.
		"""
		lead = ' ' * offset
		if nodenames and _my_node_name is not None:
			buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
		else:
			buf.write(lead + self.__class__.__name__+ ': ')

		if self.fields:
			if attrnames:
				nvlist = [(n, getattr(self,n)) for n in self.fields]
				attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
			else:
				vlist = [getattr(self, n) for n in self.fields]
				attrstr = ', '.join('%s' % v for v in vlist)
			buf.write(attrstr)

		if showcoord:
			buf.write(' (at %s)' % self.coord)
		buf.write('\n')

		for (child_name, child) in self.children():
			child.show(
				buf,
				offset=offset + 2,
				attrnames=attrnames,
				nodenames=nodenames,
				showcoord=showcoord,
				_my_node_name=child_name)

class Program(NodeAst):
	_fields = ['statements']
	
class Delaration(NodeAst):
	_fields = ['type']

class 

 
