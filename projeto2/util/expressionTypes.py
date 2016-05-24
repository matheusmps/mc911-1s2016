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

CharType = ExprType("string", str(), 
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
