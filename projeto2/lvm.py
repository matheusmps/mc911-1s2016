from enviroment import Environment

class LyaVirtualMachine(object):
	
	def __init__(self):
		self.pc = 0
		self.sp = 0
		self.program = []
		self.M = []
		self.D = []
		self.labelsMap = {}

	def initExecution(self):
		self.pc = 0
		self.sp = 0
		self.program = []
		self.M = [None] * 1000
		self.D = [None] * 100
		self.labelsMap = {}

	def getCurrentInstruction(self):
		return self.program[self.pc]

	def execute(self, program, labelsMap):
		self.initExecution()
		
		self.program = program
		self.labelsMap = labelsMap
		
		currentInstruction = self.getCurrentInstruction()
		
		while currentInstruction[0] != "end":
			self.executeInstruction(currentInstruction)
			currentInstruction = self.getCurrentInstruction()

	def generic_execute(self, instruction):
		print("Missing execution method for instruction: %s" % instruction[0])

	def executeInstruction(self, instruction):
		method = 'execute_' + instruction[0]
		executor = getattr(self, method, self.generic_execute)
		
		if executor is not None:
			executor(instruction)
		else:
			raise Exception("Missing execution method.")


	def execute_stp(self, instruction):
		self.sp = -1
		self.pc += 1
		self.D[0] = 0

#	LDC: sp=sp+1;  M[sp]=k
#	(’ldc’, k)

	def execute_ldc(self, instruction):
		self.sp += 1
		self.M[self.sp] = instruction[1]
		self.pc += 1


#	LDV: sp=sp+1;  M[sp]=M[D[i]+j]
#	(’ldv’, i, j)

	def execute_ldv(self, instruction):
		self.sp += 1
		self.M[self.sp] = self.M[self.D[ instruction[1] ]+instruction[2]]
		self.pc += 1

#	LDR: sp=sp+1;  M[sp]=D[i]+j
#	(’ldr’, i, j)

	def execute_ldr(self, instruction):
		self.sp += 1
		self.M[self.sp] = self.M[self.D[ instruction[1] ]+instruction[2]]
		self.pc += 1

#	STV: M[D[i]+j]=M[sp];  sp=sp-1
#	(’stv’, i, j)

	def execute_stv(self, instruction):
		self.M[self.D[instruction[1]] + instruction[2]] = self.M[self.sp]
		self.sp -= 1
		self.pc += 1

#	LRV: sp=sp+1;  M[sp]=M[M[D[i]+j]]
#	(’lrv’, i, j)

	def execute_lrv(self, instruction):
		self.sp += 1
		self.M[self.sp] = self.M[self.D[ instruction[1] ]+instruction[2]]

#	SRV:  M[M[D[i]+j]]=M[sp];  sp=sp-1
#	(’srv’, i, j)

	def execute_srv(self, instruction):
		self.M[self.D[ instruction[1] ]+instruction[2]] = self.M[self.sp]
		self.sp -= 1
		self.pc += 1
		

#	ADD: M[sp-1]=M[sp-1] + M[sp];  sp=sp-1
#	(’add’) 

	def execute_add(self, instruction):
		self.M[self.sp-1] = self.M[self.sp-1] + self.M[self.sp]
		self.sp -= 1
		self.pc += 1

#	SUB:  M[sp-1]=M[sp-1] - M[sp];  sp=sp-1
#	 (’sub’)

	def execute_sub(self, instruction):
		self.M[self.sp-1] = self.M[self.sp-1] - self.M[self.sp]
		self.sp -= 1
		self.pc += 1

#	MUL: M[sp-1]=M[sp-1] * M[sp];  sp=sp-1
#	(’mul’)

	def execute_mul(self, instruction):
		self.M[self.sp-1] = self.M[self.sp-1] * self.M[self.sp]
		self.sp -= 1
		self.pc += 1

#	DIV: M[sp-1]=M[sp-1] / M[sp];  sp=sp-1
#	(’div’) 

	def execute_div(self, instruction):
		self.M[self.sp-1] = self.M[self.sp-1] / self.M[self.sp]
		self.sp -= 1
		self.pc += 1

#	MOD:  M[sp-1]=M[sp-1] % M[sp];  sp=sp-1
#	(’mod’)


	def execute_mod(self, instruction):
		self.M[self.sp-1] = self.M[self.sp-1] % self.M[self.sp]
		self.sp -= 1
		self.pc += 1

#	LEQ: M[sp-1]=M[sp-1] <= M[sp];  sp=sp-1
#	(’leq’) 

	def execute_leq(self, instruction):
		if self.M[self.sp-1] <= self.M[self.sp]: 
			self.M[self.sp-1] = 1
		else:
			self.M[self.sp-1] = 0
			
		self.sp -= 1
		self.pc += 1

#	JMP: pc=p
#	(’jmp’, p)

	def execute_jmp(self, instruction):
		self.pc = self.labelsMap[instruction[1]]

#	JOF: if not M[sp]: pc=p    else: pc=pc+1  sp=sp-1
#	(’jof’, p)


	def execute_jof(self, instruction):
		if not self.M[self.sp]:
			self.pc = self.labelsMap[instruction[1]]
		else:
			self.pc += 1
		self.sp -= 1


#	ALC:  sp=sp+n
#	(’alc’, n)

	def execute_alc(self, instruction):
		self.sp += instruction[1]
		self.pc += 1

#	DLC:  sp=sp-n
#	(’dlc’, n)

	def execute_dlc(self, instruction):
		self.sp -= instruction[1]
		self.pc += 1

#	PRV: print(M[sp]); sp=sp-1
#	(’prv’)

	def execute_prv(self, instruction):
		print(self.M[self.sp])
		self.sp -= 1
		self.pc += 1

#	LBL:
#	(’lbl’, i)

	def execute_lbl(self, instruction):
		self.pc += 1
