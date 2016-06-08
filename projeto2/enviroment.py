import util.ast as ast

class ExprType(object):

	def __init__(self, typename, default, 
				unaryOpInst=None, binaryOpInst=None, 
				binaryOperators=None, unaryOperators=None,
				relOperators=None, relOpInst=None):

		self.typename = typename
		self.default = default
		self.binaryOperators = binaryOperators or set()
		self.binaryOpInst = binaryOpInst or {}
		self.unaryOperators = unaryOperators or set()
		self.unaryOpInst = unaryOpInst or {}
		self.relOperators = relOperators or set()
		self.relOpInst = relOpInst or {}

	def __repr__(self):
		return "ExprType({})".format(self.typename)

IntType = ExprType("int", int(), 
	binaryOperators={"+", "-", "*", "/", "%"}, 
	binaryOpInst={"+": "add", "-": "sub", "*": "mul", "/": "div", "%" : "mod"},
	unaryOperators={"+", "-"},
	unaryOpInst={"+": "add", "-": "neg"},
	relOperators={"==", "!=", "<", ">", "<=", ">="},
	relOpInst={"==": "equ", "!=": "neq", ">": "grt", "<": "les", ">=": "gre", "<=": "leq"},
)

StringType = ExprType("string", str(), 
	binaryOperators={"+"},
	binaryOpInst={"+": "add"},
	relOperators={"==", "!="},
	relOpInst={"==": "equ", "!=": "neq"},
)

CharType = ExprType("char", str(), 
	binaryOperators={"+"},
	binaryOpInst={"+": "add"},
	relOperators={"==", "!="},
	relOpInst={"==": "equ", "!=": "neq"},
)

BoolType = ExprType("bool", bool(),
	unaryOperators={"!"},
	relOperators={"==", "!=", "&&", "||"},
	relOpInst={"==": "equ", "!=": "neq", "&&": "and", "||": "lor"},
	unaryOpInst={"!": "not"},
)

class SymbolTable(dict):

	def __init__(self, decl=None):
		super().__init__()
		self.decl = decl

	def add(self, name, node, scope_level, offset):
		self[name] = {"node" : node, "scope_level" : scope_level, "offset" : offset}

	def lookup(self, name):
		return self.get(name, None)

	def return_type(self):
		if self.decl:
			return self.decl.procedure_definition.checkType
		return None

class Environment(object):
	def __init__(self):
		self.stack = []
		self.root = SymbolTable()
		self.stack.append(self.root)
		self.offset = []
		self.offset.append(0)
		self.labels = 0
		self.formalParams = -1
		#self.root.update({
		#	"int": IntType,
		#	"char": CharType,
		#	"string": StringType,
		#	"bool": BoolType
		#})

	def getLabel(self):
		return self.labels

	def addLabel(self):
		self.labels = self.labels + 1
		return self.labels

	def getOffset(self):
		return self.offset[-1]

	def incrementOffset(self, val):
		self.offset[-1] = self.offset[-1] + val

	def pushProcedureStack(self, symtab):
		self.stack.append(symtab)

	def push(self, enclosure):
		self.stack.append(SymbolTable(decl=enclosure))
		self.offset.append(0)

	def pop(self):
		self.stack.pop()
		self.offset.pop()
		self.formalParams = -1

	def peek(self):
		return self.stack[-1]

	def scope_level(self):
		return len(self.stack) - 1 

	def add_label(self, name, value):
		value.start_label = self.addLabel()
		value.end_label = self.addLabel()
		self.peek().add(name, value, self.scope_level(), None)

	def add_procedure(self, name, value):
		self.formalParams = -1
		print(self.formalParams)
		self.root.add(name, value, self.scope_level(), None)
		value.start_label = self.addLabel()
		value.end_label = self.addLabel()

	def add_formalParam(self, name, value):
		self.peek().add(name, value, self.scope_level(), self.formalParams)
		if isinstance(value, ast.FormalParameter):
			aloc_size = self.countAlocSizeForMode(value.parameter_specs.mode)
			self.formalParams = self.formalParams - aloc_size

	def add_local(self, name, value):
		self.peek().add(name, value, self.scope_level(), self.getOffset())
		if isinstance(value, ast.Declaration):
			val = self.countAlocSizeForMode(value.mode)
			self.incrementOffset(val)
		else:
			self.incrementOffset(1)

	def countAlocSizeForLocation(self, node):
		if isinstance(node, ast.StringElement):
			return 1
		elif isinstance(node, ast.StringSlice) or isinstance(node, ast.ArraySlice):  
			size = self.calculateLiteralRange(node.literalRange)
			return size
		elif isinstance(node, ast.ArrayElement):
			size = len(node.expressions)
			return size
		else:
			sym = lookup(node.idName)
			mode = sym.mode
			
			if isinstance(mode, ast.ReferenceMode) or isinstance(mode, ast.DiscreteRangeMode):
				mode = mode.mode
				
			if isinstance(mode, ast.StringMode) or isinstance(mode, ast.ArrayMode):
				size = self.countAlocSizeForMode(mode)
				return size
			else:
				return 1

	def countAlocSizeForMode(self, node):
		if isinstance(node, ast.DiscreteRangeMode):
			return self.calculateLiteralRange(node.literalRange)
		
		elif isinstance(node, ast.ReferenceMode):
			return self.countAlocSizeForMode(node.mode)
		
		elif isinstance(node, ast.StringMode):
			return node.length
		
		elif isinstance(node, ast.ArrayMode):
			if node.index_mode.index_mode_list is not None:
				value = 1
				for index_mode in node.index_mode.index_mode_list:
					if isinstance(index_mode, ast.LiteralRange):
						aux = self.calculateLiteralRange(index_mode)
					else:
						aux = self.countAlocSizeForMode(index_mode)
					value = value * aux
				return value
		else:
			return 1

	def calculateLiteralRange(self, node):
		if not isinstance(node.upperBound, ast.IntConst) or not isinstance(node.lowerBound, ast.IntConst):
			raise Exception("Not possible to calculate literal range without constants")
		else:
			return int(node.upperBound.val) - int(node.lowerBound.val) + 1

	def lookup(self, name):
		sym = self.lookupComplete(name)
		if sym is not None:
			return sym.get("node")
		else:
			return None

	def lookupComplete(self, name):
		for scope in reversed(self.stack):
			hit = scope.lookup(name)
			if hit is not None:
				return hit
		return None

	def printStack(self):
		print("\n\n")
		print("---- COMPLETE STACK ----")
		for scope in self.stack:
			self.printItems(scope)
		print("----")
	
	def printItems(self, scope, offset = 0):
		for k, v in scope.items():
			
			lead = ' ' * offset
			node = v.get("node")
			
			print(lead + '%s : %s' % (k, node), end = "")
			print(' - scope_level: %s' % v.get("scope_level"), end = "")
			if v.get("offset") is not None:
				print(' - offset: %s' % v.get("offset"), end = "")
			
			if isinstance(node, ast.ProcedureStmnt) or isinstance(node, ast.Label):
				print(' - start: %s - end: %s' % (node.start_label, node.end_label), end = "")
			print("\n")
			
			if isinstance(node, ast.ProcedureStmnt):
				print("    ---- PROCEDURE STACK ----")
				self.printItems(node.symtab, offset = 4)

	def find(self, name):
		if name in self.stack[-1]:
			return True
		else:
			return False

