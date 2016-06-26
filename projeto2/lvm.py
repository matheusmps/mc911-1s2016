
class LyaVirtualMachine(object):
	
	def __init__(self, program):
		self.pc = 0
		self.sp = 0
		self.program = program
		
		self.M = []
		self.D = []

	def execute(self):
		for instruction in self.program:
			if type(instruction) is tuple:
				inst = instruction[0]
				print(inst)
				print("")
