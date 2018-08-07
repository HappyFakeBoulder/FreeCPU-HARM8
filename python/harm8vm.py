import time

#NANDing binary strings
def strNand(str1, str2):
	retStr = ""
	for x in range(0, len(str1)):
		retStr += "0" if str1[x] == "1" and str2[x] == "1" else "1"
	return retStr

#left-pad with 0s until length of 8
def extendLen(string):
	while len(string) <  8:
		string = "0" + string
	return string

#compress into starting with a 1
def compressBin(string):
	while string[0] == "0" and len(string) > 1:
		string = string[1:]
	return string

#VM class
class HARM8():
	#create various variables
	def __init__(self, ioSys, slow):
		self.acc = "00000000"
		self.pc = 0
		self.ram = []
		for x in range(0, 32):
			self.ram.append("00000000")
		#ioSys must be an object that has an input method called inp() and output methods called out() and fout()
		#a class that follows these rules is created later
		self.ioSys = ioSys
		self.carryFlag = False
		self.zeroFlag = False
		self.halted = True
		self.slow = slow

	#execute an instruction
	def execInstruct(self):
		#fetch
		self.instruct = self.ram[self.pc]
		#increment
		self.pc += 1
		if self.pc > 31:
			self.halted = True
		#extended opcodes
		if self.instruct.startswith("000"):
			#00 not here due to it being a NOP
			#in
			if self.instruct[3:5] == "01":
				self.acc = self.ioSys.inp()
			#out
			if self.instruct[3:5] == "10":
				self.ioSys.out(self.acc)
			#hlt
			if self.instruct[3:5] == "11":
				self.halted = True
		#normal-length opcodes
		else:
			self.operand = int(compressBin(self.instruct[3:]), 2)
			#jmp
			if self.instruct[0:3] == "001":
				self.pc = self.operand
			#jz
			elif self.instruct[0:3] == "010":
				if self.zeroFlag:
					self.pc = self.operand
			#jc
			elif self.instruct[0:3] == "011":
				if self.carryFlag:
					self.pc = self.operand
			#lda
			elif self.instruct[0:3] == "100":
				self.acc = self.ram[self.operand]
			#sta
			elif self.instruct[0:3] == "101":
				self.ram[self.operand] = self.acc
			#add
			elif self.instruct[0:3] == "110":
				self.acc = int(compressBin(self.acc), 2) + int(compressBin(self.ram[self.operand]), 2)
				self.carryFlag = self.acc > 255
				self.acc = extendLen(bin(self.acc % 256)[2:])
				self.zeroFlag = self.acc == "00000000"
			#nand
			elif self.instruct[0:3] == "111":
				self.acc = strNand(self.acc, self.ram[self.operand])
				self.zeroFlag = self.acc == "00000000"

	#sets the memory to all 0s
	def clear(self):
		self.ram = []
		for x in range(0, 32):
			self.ram.append("00000000")

	#loads a program into memory
	def loadPrgrm(self, program):
		if type(program) != list:
			raise TypeError("Program passed to loadPrgrm was not a list")
		self.clear()
		for x in range(0, 32 if len(program) > 32 else len(program)):
			for y in program[x]:
				if y not in list("01"):
					raise ValueError("Program passed to loadPrgrm was non-binary")
			if len(program[x]) != 8:
				raise ValueError("Program passed to loadPrgrm had an incorrect word size")
			self.ram[x] = program[x]

	#runs through the program in memory
	def run(self, showMem, showEnd):
		if (type(showMem) != bool) or (type(showEnd) != bool):
			raise TypeError("showMem and/or showEnd passed to run were not a boolean")
		self.halted = False
		while not self.halted:
			self.execInstruct()
			if showMem:
				self.ioSys.out(self.ram)
			time.sleep(0.1 if self.slow else (1 / 52428))
		if showEnd:
			self.ioSys.fout(self.ram)

#this will function as an ioSys
class ConsoleIO():
	def inp(self):
		while True:
			try:
				retVal = input("Input: ")
				if len(retVal != 8):
					raise ValueError
				for x in retVal:
					if x not in list("01"):
						raise ValueError
				return retVal
			except ValueError:
				time.sleep(0.1)
				print("Invalid value.")
				time.sleep(0.15)

	def out(self, arg):
		if type(arg) == str:
			print("Output: " + arg)
		elif type(arg) == list:
			print("Memory:")
			print("\n".join(arg))
		else:
			raise TypeError("arg passed to out was not a string or list")

	def fout(self, arg):
		if type(arg) == list:
			print("\n".join(arg))
		else:
			raise TypeError("arg passed to fout was not a list")

#main
mainIO = ConsoleIO()
mainVM = HARM8(mainIO, False)
prgrmFile = open("prgrm.txt", "r")
mainVM.loadPrgrm(prgrmFile.read().split("\n"))
prgrmFile.close()
mainVM.run(False, True)
