class Coord(object):
    __slots__ = ('file', 'line', 'column', '__weakref__')

    def __init__(self, file, line, column=None):
        self.file = file
        self.line = line
        self.column = column

    def __str__(self):
        str = "%s:%s" % (self.file, self.line)
        if self.column: str += ":%s" % self.column
        return str


class ParseError(Exception): pass


class PLYParser(object):
	def _coord(self, lineno, column=None):
		return Coord(file = self.lexer.filename, 
			line = lineno, 
			column=column)

	def _parse_error(self, coord, msg):
		raise ParseError("%s: %s" % (msg, repr(coord)))
