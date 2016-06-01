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
	binaryOperators={"+", "-", "*", "/"}, 
	binaryOpInst={"+": "add", "-": "sub", "*": "imul", "/": "idiv"},
	unaryOperators={"+", "-"},
	unaryOpInst={"+": "uadd", "-": "uneg"},
	relOperators={"==", "!=", "<", ">", "<=", ">="},
	relOpInst={"==": "eq", "!=": "neq", ">": "gt", "<": "lt", ">=": "gte", "<=": "lte"},
)

StringType = ExprType("string", str(), 
	binaryOperators={"+"},
	binaryOpInst={"+": "add"},
	relOperators={"==", "!="},
	relOpInst={"==": "eq", "!=": "neq"},
)

CharType = ExprType("char", str(), 
	binaryOperators={"+"},
	binaryOpInst={"+": "add"},
	relOperators={"==", "!="},
	relOpInst={"==": "eq", "!=": "neq"},
)

BoolType = ExprType("bool", bool(),
	unaryOperators={"!"},
	relOperators={"==", "!=", "&&", "||"},
	relOpInst={"==": "eq", "!=": "neq", "&&": "land", "||": "lor"},
	unaryOpInst={"!": "not"},
)

class SymbolTable(dict):

	def __init__(self, decl=None):
		super().__init__()
		self.decl = decl

	def add(self, name, value):
		self[name] = value

	def lookup(self, name):
		return self.get(name, None)

	def return_type(self):
		if self.decl:
			return self.decl.result_spec.mode.modeName
		return None

class Environment(object):
	def __init__(self):
		self.stack = []
		self.root = SymbolTable()
		self.stack.append(self.root)
		self.root.update({
			"int": IntType,
			"char": CharType,
			"string": StringType,
			"bool": BoolType
		})

	def push(self, enclosure):
		self.stack.append(SymbolTable(decl=enclosure))

	def pop(self):
		self.stack.pop()

	def peek(self):
		return self.stack[-1]

	def scope_level(self):
		return len(self.stack)

	def add_local(self, name, value):
		self.peek().add(name, value)

	def add_root(self, name, value):
		self.root.add(name, value)

	def lookup(self, name):
		for scope in reversed(self.stack):
			hit = scope.lookup(name)
			if hit is not None:
				return hit
		return None

	def printStack(self):
		print("\n\n")
		print("---- STACK ----")
		i = 0
		for scope in self.stack:
			print("Stack Scope: %s" % i)
			print("----")
			for k, v in scope.items():
				print('%s : %s' % (k, v))
			i = i + 1

	def find(self, name):
		if name in self.stack[-1]:
			return True
		else:
			return False

