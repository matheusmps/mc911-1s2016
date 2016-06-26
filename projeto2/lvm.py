from enviroment import Environment

class LyaVirtualMachine(object):
	
	def __init__(self):
		self.pc = 0
		self.sp = 0
		self.program = []
		self.M = []
		self.D = []
		self.H = []
		self.labelsMap = {}

	def initExecution(self):
		self.pc = 0
		self.sp = 0
		self.program = []
		self.M = [None] * 1000
		self.D = [None] * 100
		self.H = [None] * 100
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

#	NEG: M[sp]= -M[sp]
#	(’neg’)

	def execute_neg(self, instruction):
		self.M[self.sp] = - self.M[self.sp]
		self.pc += 1

#	AND: M[sp-1]=M[sp-1] and M[sp];  sp=sp-1
#	(’and’)

	def execute_and(self, instruction):
		self.M[self.sp-1] = self.M[self.sp-1] and self.M[self.sp]
		self.sp -= 1
		self.pc += 1

#	LOR: M[sp-1]=M[sp-1] or M[sp];  sp=sp-1
#	(’lor’)

	def execute_and(self, instruction):
		self.M[self.sp-1] = self.M[self.sp-1] or self.M[self.sp]
		self.sp -= 1
		self.pc += 1

#	NOT:  M[sp]= not M[sp]
#	(’not’)

	def execute_not(self, instruction):
		self.M[self.sp] = not self.M[self.sp]
		self.pc += 1

#	LES:  M[sp-1]=M[sp-1] < M[sp];  sp=sp-1
#	(’les’)

	def execute_les(self, instruction):
		if self.M[self.sp-1] < self.M[self.sp]:
			 self.M[self.sp-1] = 1
		else:
			self.M[self.sp -1] = 0
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

#	GRT: M[sp-1]=M[sp-1] > M[sp];  sp=sp-1
#	(’grt’)

	def execute_grt(self, instruction):
		if self.M[self.sp-1] > self.M[self.sp] :
			self.M[self.sp-1] = 1
		else:
			self.M[self.sp -1] = 0
		self.sp -= 1
		self.pc += 1
		
#	GRE: M[sp-1]=M[sp-1] >= M[sp];  sp=sp-1
#	(’gre’)

	def execute_gre(self, instruction):
		if self.M[self.sp-1] >= self.M[self.sp] :
			self.M[self.sp-1] = 1
		else:
			self.M[self.sp -1] = 0
		self.sp -= 1
		self.pc += 1

#	EQU: M[sp-1]=M[sp-1] == M[sp];  sp=sp-1
#	(’equ’)

	def execute_equ(self, instruction):
		if self.M[self.sp-1] == self.M[self.sp] :
			self.M[self.sp-1] = 1
		else:
			self.M[self.sp -1] = 0
		self.sp -= 1
		self.pc += 1

#	NEQ: M[sp-1]=M[sp-1] != M[sp];  sp=sp-1
#	(’neq’)

	def execute_neq(self, instruction):
		if self.M[self.sp-1] != self.M[self.sp] :
			self.M[self.sp-1] = 1
		else:
			self.M[self.sp -1] = 0
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

#	CFU:  sp=sp+1; M[sp]=pc+1; pc=p
#	(’cfu’, p)

	def execute_cfu(self, instruction):
		self.sp += 1
		self.M[self.sp] = self.pc+1
		self.pc += self.labelsMap[instruction[1]]


#	ENF: sp=sp+1; M[sp]=D[k]; D[k]=sp+1
#	(’enf’, k)

	def execute_enf(self, instruction):
		self.sp += 1
		self.M[self.sp] = self.D[instruction[1]]
		self.D[instruction[1]] = self.sp + 1
		self.pc += 1

#	RET: D[k]=M[sp]; pc=M[sp-1]; sp=sp-(n+2)
#	(’ret’, k, n)

	def execute_ret(self, instruction):
		self.D[instruction[1]] = self.M[self.sp]
		self.pc = self.M[self.sp-1]
		self.sp -= instruction[2] + 2

#	IDX: M[sp-1]=M[sp-1] + M[sp] * k; sp=sp-1;
#	(’idx’, k)

	def execute_idx(self, instruction):
		self.M[self.sp-1] = self.M[self.sp-1] + self.M[self.sp] * instruction[1]
		self.sp -= 1
		self.pc += 1

#	GRC: M[sp]=M[M[sp]]
#	(’grc’)

	def execute_grc(self, instruction):
		self.M[self.sp] = self.M[ self.M[self.sp] ]
		self.pc += 1

#	LMV: t=M[sp]; M[sp:sp+k]=M[t:t+k]; sp += (k-1)
#	(’lmv’, k)

	def execute_lmv(self, instruction):
		t = self.M[self.sp]
		for i=0 to instruction[1]:
			self.M[self.sp + i] = self.M[t + i]
		self.sp += instruction[1] - 1 
		self.pc += 1

#	SMV: t = M[sp-k]; M[t:t+k] =M[sp-k+1:sp+1]; sp -= (k+1);
#	(’smv’, k)

	def execute_smv(self, instruction):
		t = self.M[self.sp-instruction[1]]
		for i=0 to instruction[1]:
			self.M[t + i] = self.M[self.sp - instruction[1] + 1 +i ]
		self.sp -= instruction[1] + 1
		self.pc += 1

#	SMR: t1 = M[sp-1]; t2 = M[sp]; M[t1:t1+k] = M[t2:t2+k]; sp -= 1;
#	(’smr’, k)

	def execute_smr(self, instruction):
		t1 = self.M[self.sp-1]
		t2 = self.M[self.sp]
		
		for i=0 to instruction[1]:
			self.M[t1 + i] = self.M[t2 + i]
		self.sp -= 1
		self.pc += 1

#	STS: adr=M[sp]; M[adr]=len(H[k]); for c in H[k]: adr=adr+1; M[adr]=c; sp=sp-1
#	(’sts’, k)

	def execute_sts(self, instruction):
		adr = self.M[self.sp]
		self.M[adr] =  len ( self.H[instruction[1] )
		
		for c in self.H[instruction[1]]:
			adr += 1
		
		self.M[adr] = c
		self.sp -= 1
		self.pc += 1

#	RDV: sp=sp+1;  M[sp]=input()
#	(’rdv’)

	def execute_rdv(self, instruction):
		self.sp += 1
		self.M[self.sp] = input()
		self.pc += 1

#	RDS: str=input(); adr=M[sp]; M[adr] = len(str); for k in str: adr=adr+1 M[adr]=k; sp=sp-1;
#	(’rds’)

	def execute_rds(self, instruction):
		str = input() 
		adr = self.M[self.sp]
		self.M[adr] = len (str)
		for k in str:
			adr += 1
			self.M[adr] = k
		self.sp -= 1
		self.pc += 1

#	PRV: print(M[sp]); sp=sp-1
#	(’prv’)

	def execute_prv(self, instruction):
		print(self.M[self.sp])
		self.sp -= 1
		self.pc += 1

#	PRT: print(M[sp-k+1:sp+1]); sp-=(k-1)
#	('prt', k)

	def execute_prt(self, instruction):
		for i=instruction[1] to 0:
			print(self.M[self.sp - i + 1])
		self.sp -= instruction[1] - 1
		self.pc += 1

#	PRC: print(H(i),end="")
#	(’prc’, i)

	def execute_prc(self, instruction):
		print(self.H[instruction[1]], end="")
		self.pc += 1

#	PRS: adr = M[sp]; len = M[adr]; for i in range(0,len): adr = adr + 1 print(M(adr),end=""); sp=sp-1;
#	(’prs’)

	def execute_prs(self, instruction):
		adr = self.M[self.sp]
		b = self.M[adr]
		for i in range(0, b):
			adr += 1
			print(self.M[adr], end="")
		self.sp -= 1
		self.pc += 1

#	LBL:
#	(’lbl’, i)

	def execute_lbl(self, instruction):
		self.pc += 1
		
#	END:
#	(’end’)

	def execute_end(self, instruction):
		pass



