import sys

class NodeAst(object):
	
	__slots__ = ('coord', 'checkType')
	
	attr_names = ()

	def children(self):
		""" A sequence of all children that are Nodes"""
		return tuple([])

	def show(self, buf=sys.stdout, offset=0, _my_node_name=None, recursive=True):
		
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
		
		if recursive:
			for (child, child_name) in self.children():
				child.show(
					buf,
					offset=offset + 4,
					_my_node_name=child_name,
					recursive=recursive)
		else:
			buf.write("    Nodes:")
			for (child, child_name) in self.children():
				buf.write(" " + child_name + ",")
			buf.write('\n')

class Program(NodeAst):
	__slots__ = ('statements', 'environment', 'symtab')
	
	def __init__(self, statements, coord):
		self.coord = coord
		self.statements = statements
	
	def children(self):
		nodelist = []
		for child in (self.statements or []): nodelist.append((child, "stmt"))
		return nodelist

class DeclStmt(NodeAst):
	__slots__ = ('decls')
	
	def __init__(self, decls, coord):
		self.coord = coord
		self.decls = decls
	
	def children(self):
		nodelist = []
		for child in (self.decls or []): nodelist.append((child, "decls"))
		return nodelist

class Declaration(NodeAst):
	__slots__ = ('idList', 'mode', 'init', 'scope_level', 'offset')
	
	def __init__(self, idList, mode, init, coord):
		self.coord = coord
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
	
	def __init__(self, modeName, coord):
		self.coord = coord
		self.modeName = modeName
		
	attr_names = ('modeName', )

class DiscreteMode(NodeAst):
	__slots__ = ('modeName')
	
	def __init__(self, modeName, coord):
		self.coord = coord
		self.modeName = modeName
		
	attr_names = ('modeName', )

class ReferenceMode(NodeAst):
	__slots__ = ('mode')
	
	def __init__(self, mode, coord):
		self.coord = coord
		self.mode = mode
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		return nodelist

class DiscreteRangeMode(NodeAst):
	__slots__ = ('mode', 'literalRange')
	
	def __init__(self, mode, literalRange, coord):
		self.coord = coord
		self.mode = mode
		self.literalRange = literalRange
	
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		if self.literalRange is not None: nodelist.append((self.literalRange, "range"))
		return nodelist

class LiteralRange(NodeAst):
	__slots__ = ('lowerBound', 'upperBound')
	
	def __init__(self, lowerBound, upperBound, coord):
		self.coord = coord
		self.lowerBound = lowerBound
		self.upperBound = upperBound
	
	def children(self):
		nodelist = []
		if self.lowerBound is not None: nodelist.append((self.lowerBound, "lowerBound"))
		if self.upperBound is not None: nodelist.append((self.upperBound, "upperBound"))
		return nodelist

class StringMode(NodeAst):
	__slots__ = ('length')
	
	def __init__(self, length, coord):
		self.coord = coord
		self.length = length
		
	attr_names = ('length', )

class IndexMode(NodeAst):
	__slots__ = ('index_mode_list')
	
	def __init__(self, index_mode_list, coord):
		self.coord = coord
		self.index_mode_list = index_mode_list
		
	def children(self):
		nodelist = []
		for child in (self.index_mode_list or []): nodelist.append((child, "index_mode_list"))
		return nodelist

class ArrayMode(NodeAst):
	__slots__ = ('index_mode', 'element_node')
	
	def __init__(self, index_mode, element_node, coord):
		self.coord = coord
		self.index_mode = index_mode
		self.element_node = element_node
		
	def children(self):
		nodelist = []
		if self.index_mode is not None: nodelist.append((self.index_mode, "index_mode"))
		if self.element_node is not None: nodelist.append((self.element_node, "element_mode"))
		return nodelist

class ModeDef(NodeAst):
	__slots__ = ('idList', 'mode')
	
	def __init__(self, idList, mode, coord):
		self.coord = coord
		self.idList = idList
		self.mode = mode
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		return nodelist
	
	attr_names = ('idList',)

class NewModeStmt(NodeAst):
	__slots__ = ('modeList')
	
	def __init__(self, modeList, coord):
		self.coord = coord
		self.modeList = modeList
	
	def children(self):
		nodelist = []
		for child in (self.modeList or []): nodelist.append((child, "mode_list"))
		return nodelist

class SynStmt(NodeAst):
	__slots__ = ('synList')
	
	def __init__(self, synList, coord):
		self.coord = coord
		self.synList = synList
	
	def children(self):
		nodelist = []
		for child in (self.synList or []): nodelist.append((child, "syn_list"))
		return nodelist

class SynDef(NodeAst):
	__slots__ = ('idList', 'mode', 'expression')
	
	attr_names = ('idList', )
	
	def __init__(self, idList, mode, expression, coord):
		self.coord = coord
		self.idList = idList
		self.mode = mode
		self.expression = expression
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		if self.expression is not None: nodelist.append((self.expression, "expression"))
		return nodelist
		

class Location(NodeAst):
	__slots__ = ('idName')
	
	attr_names = ('idName',)
	
	def __init__(self, idName, coord):
		self.coord = coord
		self.idName = idName

class ReferencedLocation(NodeAst):
	__slots__ = ('location', 'idName')
	
	def __init__(self, location, coord):
		self.coord = coord
		self.location = location
		
	def children(self):
		nodelist = []
		if self.location is not None: nodelist.append((self.location, "location"))
		return nodelist

class DereferencedLocation(NodeAst):
	__slots__ = ('location', 'idName')
	
	def __init__(self, location, coord):
		self.coord = coord
		self.location = location
		
	def children(self):
		nodelist = []
		if self.location is not None: nodelist.append((self.location, "location"))
		return nodelist

class StringElement(NodeAst):
	__slots__ = ('location', 'start_element', 'idName')
	
	def __init__(self, location, start_element, coord):
		self.coord = coord
		self.location = location
		self.start_element = start_element
	
	def children(self):
		nodelist = []
		if self.location is not None: nodelist.append((self.location, "id"))
		if self.start_element is not None: nodelist.append((self.start_element, "start_element"))
		return nodelist

class StringSlice(NodeAst):
	__slots__ = ('location', 'literalRange', 'idName')
	
	def __init__(self, location, literalRange, coord):
		self.coord = coord
		self.location = location
		self.literalRange = literalRange
	
	def children(self):
		nodelist = []
		if self.location is not None: nodelist.append((self.location, "id"))
		if self.literalRange is not None: nodelist.append((self.literalRange, "range"))
		return nodelist

class ArrayElement(NodeAst):
	__slots__ = ('array_location', 'expressions', 'idName')
	
	def __init__(self, array_location, expressions, coord):
		self.coord = coord
		self.array_location = array_location
		self.expressions = expressions
		
	def children(self):
		nodelist = []
		if self.array_location is not None: nodelist.append((self.array_location, "array_location"))
		for child in (self.expressions or []): nodelist.append((child, "expressions"))
		return nodelist

class ArraySlice(NodeAst):
	__slots__ = ('array_location', 'literalRange', 'idName')
	
	def __init__(self, array_location, literalRange, coord):
		self.coord = coord
		self.array_location = array_location
		self.literalRange = literalRange
		
	def children(self):
		nodelist = []
		if self.array_location is not None: nodelist.append((self.array_location, "array_location"))
		if self.literalRange is not None: nodelist.append((self.literalRange, "range"))
		return nodelist

class Assignment(NodeAst):
	__slots__ = ('location', 'assign_op', 'expression')
	
	def __init__(self, location, assign_op, expression, coord):
		self.coord = coord
		self.location = location
		self.assign_op = assign_op
		self.expression = expression
	
	attr_names = ('assign_op', )
	
	def children(self):
		nodelist = []
		if self.location is not None: nodelist.append((self.location, "location"))
		if self.expression is not None: nodelist.append((self.expression, "expression"))
		return nodelist

class BinaryExpression(NodeAst):
	__slots__ = ('operand1', 'operator', 'operand2')
	
	def __init__(self, operand1, operator, operand2, coord):
		self.coord = coord
		self.operand1 = operand1
		self.operator = operator
		self.operand2 = operand2
	
	attr_names = ('operator',)
	
	def children(self):
		nodelist = []
		if self.operand1 is not None: nodelist.append((self.operand1, "operand1"))
		if self.operand2 is not None: nodelist.append((self.operand2, "operand2"))
		return nodelist

class RelationalExpression(NodeAst):
	__slots__ = ('operand1', 'operator', 'operand2')
	
	def __init__(self, operand1, operator, operand2, coord):
		self.coord = coord
		self.operand1 = operand1
		self.operator = operator
		self.operand2 = operand2
	
	attr_names = ('operator',)
	
	def children(self):
		nodelist = []
		if self.operand1 is not None: nodelist.append((self.operand1, "operand1"))
		if self.operand2 is not None: nodelist.append((self.operand2, "operand2"))
		return nodelist

class UnaryExpression(NodeAst):
	__slots__ = ('operand', 'operator')
	
	def __init__(self, operand, operator, coord):
		self.coord = coord
		self.operand = operand
		self.operator = operator
	
	attr_names = ('operator',)
	
	def children(self):
		nodelist = []
		if self.operand is not None: nodelist.append((self.operand, "operand"))
		return nodelist

class ConditionalExpression(NodeAst):
	__slots__ = ('if_expr', 'then_expr', 'elseif_expr', 'else_expr')
	
	def __init__(self, if_expr, then_expr, elseif_expr, else_expr, coord):
		self.coord = coord
		self.if_expr = if_expr
		self.then_expr = then_expr
		self.elseif_expr = elseif_expr
		self.else_expr = else_expr
	
	def children(self):
		nodelist = []
		if self.if_expr is not None: nodelist.append((self.if_expr, "if"))
		if self.then_expr is not None: nodelist.append((self.then_expr, "then"))
		for child in (self.elseif_expr or []): nodelist.append((child, "elseif"))
		if self.else_expr is not None: nodelist.append((self.else_expr, "else"))
		return nodelist


class IntConst(NodeAst):
	__slots__ = ('val')
	attr_names = ('val',)
	
	def __init__(self, val, coord):
		self.coord = coord
		self.val = val

class CharConst(NodeAst):
	__slots__ = ('val')
	attr_names = ('val',)
	
	def __init__(self, val, coord):
		self.coord = coord
		self.val = val

class Boolean(NodeAst):
	__slots__ = ('val')
	attr_names = ('val',)
	
	def __init__(self, val, coord):
		self.coord = coord
		self.val = val

class StrConst(NodeAst):
	__slots__ = ('val', 'position')
	attr_names = ('val',)
	
	def __init__(self, val, coord):
		self.coord = coord
		self.val = val

class EmptyConst(NodeAst):
	__slots__ = ()
	attr_names = ()

class ValueArrayElement(NodeAst):
	__slots__ = ('primitiveValue', 'expressions')
	
	def __init__(self, primitiveValue, expressions, coord):
		self.coord = coord
		self.primitiveValue = primitiveValue
		self.expressions = expressions
		
	def children(self):
		nodelist = []
		if self.primitiveValue is not None: nodelist.append((self.primitiveValue, "primitiveValue"))
		for child in (self.expressions or []): nodelist.append((child, "expressions"))
		return nodelist

class ValueArraySlice(NodeAst):
	__slots__ = ('primitiveValue', 'literalRange')
	
	def __init__(self, primitiveValue, literalRange, coord):
		self.coord = coord
		self.primitiveValue = primitiveValue
		self.literalRange = literalRange
		
	def children(self):
		nodelist = []
		if self.primitiveValue is not None: nodelist.append((self.primitiveValue, "primitiveValue"))
		if self.literalRange is not None: nodelist.append((self.literalRange, "range"))
		return nodelist

class ActionStatement(NodeAst):
	__slots__ = ('action', 'label')
	
	def __init__(self, action, label, coord):
		self.coord = coord
		self.action = action
		self.label = label
	
	def children(self):
		nodelist = []
		if self.action is not None: nodelist.append((self.action, "action"))
		if self.label is not None: nodelist.append((self.label, "label"))
		return nodelist

class Label(NodeAst):
	__slots__ = ('label', 'start_label', 'end_label')
	
	attr_names = ('label',)
	
	def __init__(self, label, coord):
		self.coord = coord
		self.label = label

class IfAction(NodeAst):
	__slots__ = ('if_expr', 'then_clause', 'else_clause')
	
	def __init__(self, if_expr, then_clause, else_clause, coord):
		self.coord = coord
		self.if_expr = if_expr
		self.then_clause = then_clause
		self.else_clause = else_clause
		
	def children(self):
		nodelist = []
		if self.if_expr is not None: nodelist.append((self.if_expr, "if"))
		for child in (self.then_clause or []): nodelist.append((child, "then"))
		for child in (self.else_clause or []): nodelist.append((child, "else"))
		return nodelist

class ElseIfClause(NodeAst):
	__slots__ = ('test', 'stmts', 'label')

	def __init__(self, test, stmts, coord):
		self.coord = coord
		self.test = test
		self.stmts = stmts

	def children(self):
		nodelist = []
		if self.test is not None: nodelist.append((self.test, "if"))
		for child in (self.stmts or []): nodelist.append((child, "then"))
		return nodelist

class ElseClause(NodeAst):
	__slots__ = ('stmts', 'label')

	def __init__(self, stmts, coord):
		self.coord = coord
		self.stmts = stmts

	def children(self):
		nodelist = []
		for child in (self.stmts or []): nodelist.append((child, "stmts"))
		return nodelist

class DoAction(NodeAst):
	__slots__ = ('control', 'stmts')
	
	def __init__(self, control, stmts, coord):
		self.coord = coord
		self.control = control
		self.stmts = stmts
		
	def children(self):
		nodelist = []
		for child in (self.control or []): nodelist.append((child, "control"))
		for child in (self.stmts or []): nodelist.append((child, "stmts"))
		return nodelist

class For(NodeAst):
	__slots__ = ('iteration')
	
	def __init__(self, iteration, coord):
		self.coord = coord
		self.iteration = iteration 
		
	def children(self):
		nodelist = []
		if self.iteration is not None: nodelist.append((self.iteration, "iteration"))
		return nodelist

class StepEnumeration(NodeAst):
	__slots__ = ('counter', 'start_value', 'step_value', 'end_value', 'down')
	
	attr_names = ('down',)
	
	def __init__(self, counter, start_value, step_value, end_value, down, coord):
		self.coord = coord
		self.counter = counter
		self.start_value = start_value
		self.step_value = step_value
		self.end_value = end_value
		self.down = down
		
	def children(self):
		nodelist = []
		if self.counter is not None: nodelist.append((self.counter, "counter"))
		if self.start_value is not None: nodelist.append((self.start_value, "start_value"))
		if self.step_value is not None: nodelist.append((self.step_value, "step_value"))
		if self.end_value is not None: nodelist.append((self.end_value, "end_value"))
		return nodelist

class RangeEnumeration(NodeAst):
	__slots__ = ('counter', 'expression', 'down')
	
	attr_names = ('down',)
	
	def __init__(self, counter, expression, down, coord):
		self.coord = coord
		self.counter = counter
		self.expression = expression
		self.down = down
		
	def children(self):
		nodelist = []
		if self.counter is not None: nodelist.append((self.counter, "counter"))
		if self.expression is not None: nodelist.append((self.expression, "expression"))
		return nodelist


class While(NodeAst):
	__slots__ = ('bool_expr')
	
	def __init__(self, bool_expr, coord):
		self.coord = coord
		self.bool_expr = bool_expr 
		
	def children(self):
		nodelist = []
		if self.bool_expr is not None: nodelist.append((self.bool_expr, "bool_expr"))
		return nodelist

class ProcedureStmnt(NodeAst):
	__slots__ = ('label', 'procedure_definition', 'scope_level', 'param_list_size', 'symtab', 'start_label', 'end_label')
	
	def __init__(self, label, procedure_definition, coord):
		self.coord = coord
		self.label = label
		self.procedure_definition = procedure_definition
		
	def children(self):
		nodelist = []
		if self.label is not None: nodelist.append((self.label, "label"))
		if self.procedure_definition is not None: nodelist.append((self.procedure_definition, "procedure_definition"))
		return nodelist

class ProcedureDef(NodeAst):
	__slots__ = ('formal_parameter_list', 'result_spec', 'statement_list', 'param_list_size')
	
	def __init__(self, formal_parameter_list, result_spec, statement_list, coord):
		self.coord = coord
		self.formal_parameter_list = formal_parameter_list
		self.result_spec = result_spec
		self.statement_list = statement_list
		
	def children(self):
		nodelist = []
		for child in (self.formal_parameter_list or []): nodelist.append((child, "formal_parameter_list"))
		if self.result_spec is not None: nodelist.append((self.result_spec, "result_spec"))
		for child in (self.statement_list or []): nodelist.append((child, "statement_list"))
		return nodelist
		
class FormalParameter(NodeAst):
	__slots__ = ('idList', 'parameter_specs', 'scope_level', 'offset', 'mode')
	
	def __init__(self, idList, parameter_specs, coord):
		self.coord = coord
		self.idList = idList
		self.parameter_specs = parameter_specs
		
	def children(self):
		nodelist = []
		if self.parameter_specs is not None: nodelist.append((self.parameter_specs, "parameter_specs"))
		return nodelist
		
	attr_names = ('idList',)

class ParameterSpecs(NodeAst):
	__slots__ = ('mode', 'attr')
	
	def __init__(self, mode, attr, coord):
		self.coord = coord
		self.mode = mode
		self.attr = attr
		
	attr_names = ('attr',)
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		return nodelist
	
class ResultSpecs(NodeAst):
	__slots__ = ('mode', 'attr')
	
	def __init__(self, mode, attr, coord):
		self.coord = coord
		self.mode = mode
		self.attr = attr
		
	def children(self):
		nodelist = []
		if self.mode is not None: nodelist.append((self.mode, "mode"))
		return nodelist

	attr_names = ('attr',)

class ProcedureCall(NodeAst):
	__slots__ = ('name', 'params')
	
	def __init__(self, name, params, coord):
		self.coord = coord
		self.name = name
		self.params = params

	attr_names = ('name',)

	def children(self):
		nodelist = []
#		if self.name is not None: nodelist.append((self.name, "name"))
		for child in (self.params or []): nodelist.append((child, "params"))
		return nodelist

class Parameter(NodeAst):
	__slots__ = ('expr', 'call_arg')
	
	def __init__(self, expr, coord):
		self.coord = coord
		self.expr = expr

	def children(self):
		nodelist = []
		if self.expr is not None: nodelist.append((self.expr, "expr"))
		return nodelist


class ExitAction(NodeAst):
	__slots__ = ('label')
	
	def __init__(self, label, coord):
		self.coord = coord
		self.label = label

	def children(self):
		nodelist = []
		if self.label is not None: nodelist.append((self.label, "label"))
		return nodelist


class ReturnAction(NodeAst):
	__slots__ = ('result')
	
	def __init__(self, result, coord):
		self.coord = coord
		self.result = result

	def children(self):
		nodelist = []
		if self.result is not None: nodelist.append((self.result, "result"))
		return nodelist


class ResultAction(NodeAst):
	__slots__ = ('result')
	
	def __init__(self, result, coord):
		self.coord = coord
		self.result = result

	def children(self):
		nodelist = []
		if self.result is not None: nodelist.append((self.result, "result"))
		return nodelist

class BuiltinCall(NodeAst):
	__slots__ = ('name', 'params')
	
	attr_names = ('name', )
	
	def __init__(self, name, params, coord):
		self.coord = coord
		self.name = name
		self.params = params

	def children(self):
		nodelist = []
		for child in (self.params or []): nodelist.append((child, "params"))
		return nodelist
