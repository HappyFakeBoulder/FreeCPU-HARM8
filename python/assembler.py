import sys

#left-pad with 0s until length of 8
def extendLen(string):
	while len(string) <  8:
		string = "0" + string
	return string

#left-pad with 0s until length of 5
def extLen(string):
	while len(string) <  5:
		string = "0" + string
	return string

#my way of exiting the program
class _(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)

# when there's an error in the assembly code
def AssemblyError(lineNum, lineContent, errorName, errorDesc):
	input("Line " + str(lineNum + 1) + ":\n" + lineContent + "\n" + errorName + ": " + errorDesc + "\nPress enter to continue")
	# exits the program
	raise _

# the main assembler class
class Assembler():
	def __init__(self):
		self.codeStr = ""
		self.codeList = []
		self.currentLineStr = ""
		self.currentLineList = []
		self.lineNum = -1
		self.variables = {}
		self.compiledResult = ""
		self.counter = 0

	def assembleLine(self, mode):
		# mode is a boolean, determining whether to scan for variable declarations (False) or for instructions (True)
		if self.currentLineStr[0].isalpha():
			if True:
				self.currentLineList = self.currentLineStr.split(" ")
				# snip statement
				if self.currentLineList[0] == "snip":
					# checking for correct number of arguments
					if len(self.currentLineList) != 2:
						AssemblyError(self.lineNum, self.currentLineStr, "ArgumentError", "Invalid number of parameters for snip statement")
					# when the user does it right
					if self.currentLineList[1].isnumeric():
						for x in range(0, int(self.currentLineList[1])):
							if mode:
								if len(self.compiledResult) > 0:
									self.compiledResult += "\n"
								self.compiledResult += "00000000"
							self.counter += 1
					# when the argument is not a number
					else:
						AssemblyError(self.lineNum, self.currentLineStr, "TypeError", "Parameter to snip statement is not numeric")
				# dat statement
				elif self.currentLineList[0] == "dat":
					# checking for correct number of arguments
					if len(self.currentLineList) != 2:
						AssemblyError(self.lineNum, self.currentLineStr, "ArgumentError", "Invalid number of parameters for dat statement")
					# when the user does it right
					if self.currentLineList[1].isnumeric():
						if mode:
							if len(self.compiledResult) > 0:
								self.compiledResult += "\n"
							self.compiledResult += extendLen(bin(int(self.currentLineList[1]))[2:])
						self.counter += 1
					# when the argument is not a number
					else:
						AssemblyError(self.lineNum, self.currentLineStr, "TypeError", "Parameter to dat statement is not numeric")
				# normal-length opcodes
				elif self.currentLineList[0] in "jmp jz jc lda sta add nand".split(" "):
					# checking for correct number of arguments
					if len(self.currentLineList) != 2:
						AssemblyError(self.lineNum, self.currentLineStr, "ArgumentError", "Invalid number of parameters for " + self.currentLineList[0] + " statement")
					# when the user does it right - with a number
					if self.currentLineList[1].isnumeric():
						self.temp = {"jmp":"001", "jz":"010", "jc":"011", "lda":"100", "sta":"101", "add":"110", "nand":"111"}
						if mode:
							if len(self.compiledResult) > 0:
								self.compiledResult += "\n"
							self.compiledResult += self.temp[self.currentLineList[0]] + extLen(bin(int(self.currentLineList[1]))[2:])
						self.counter += 1
					# when the user does it right - with a variable
					elif self.currentLineList[1][0] == "$":
						try:
							self.temp = {"jmp":"001", "jz":"010", "jc":"011", "lda":"100", "sta":"101", "add":"110", "nand":"111"}
							if mode:
								if len(self.compiledResult) > 0:
									self.compiledResult += "\n"
								self.compiledResult += self.temp[self.currentLineList[0]] + self.variables[self.currentLineList[1][1:]]
							self.counter += 1
						# when the user tries to reference an undefined variable
						except KeyError:
							AssemblyError(self.lineNum, self.currentLineStr, "NameError", "Variable '" + self.currentLineList[1] + "' is not defined")
					# when the argument is invalid
					else:
						AssemblyError(self.lineNum, self.currentLineStr, "TypeError", "Parameter to " + self.currentLineList[0] + " statement is not numeric or a variable")
				# extended opcodes
				elif self.currentLineList[0] in "nop in out hlt".split(" "):
					# checking for correct number of arguments
					if len(self.currentLineList) != 1:
						AssemblyError(self.lineNum, self.currentLineStr, "ArgumentError", "Invalid number of parameters for " + self.currentLineList[0] + " statement")
					# when the user does it right
					self.temp = {"nop":"00000", "in":"00001", "out":"00010", "hlt":"00011"}
					if mode:
						if len(self.compiledResult) > 0:
							self.compiledResult += "\n"
						self.compiledResult += self.temp[self.currentLineList[0]] + "000"
					self.counter += 1
				# not a valid statement
				else:
					AssemblyError(self.lineNum, self.currentLineStr, "FunctionError", "'" + self.currentLineList[0] + "' statement is not defined")

		elif self.currentLineStr[0] == "$":
			if mode == False:
				# check for valid var name
				self.currentLineList = self.currentLineStr.split(" ")
				if self.currentLineList[0][1] not in list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"):
					AssemblyError(self.lineNum, self.currentLineStr, "SyntaxError", "Invalid variable name")
				for x in self.currentLineList[0][2:]:
					if x not in list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"):
						AssemblyError(self.lineNum, self.currentLineStr, "SyntaxError", "Invalid variable name")
				# when it's a number to assign to it
				if self.currentLineList[2].isnumeric():
					self.variables[self.currentLineList[0][1:]] = extLen(bin(int(self.currentLineList[2]))[2:])
				# when it's __line__
				elif self.currentLineList[2] == "__line__":
					self.variables[self.currentLineList[0][1:]] = extLen(bin(int(self.counter))[2:])
				# when it's not a valid thing
				else:
					AssemblyError(self.lineNum, self.currentLineStr, "TypeError", "Parameter to assignment statement is not numeric or a variable")

		elif self.currentLineStr[0] == "#":
			if mode == True:
				pass

		else:
			AssemblyError(self.lineNum, self.currentLineStr, "SyntaxError", "Invalid starting character in line")

	def reset(self):
		self.codeStr = ""
		self.codeList = []
		self.lineNum = -1
		self.variables = {}
		self.compiledResult = ""
		self.counter = 0

	def loadPrgrm(self, program):
		self.codeStr = program
		self.codeList = program.split("\n")

	def assemble(self):
		# variable run-through
		for line in range(0, len(self.codeList)):
			self.lineNum = line
			self.currentLineStr = self.codeList[self.lineNum].strip()
			self.assembleLine(False)
		# binary run-through
		for line in range(0, len(self.codeList)):
			self.lineNum = line
			self.currentLineStr = self.codeList[self.lineNum].strip()
			self.assembleLine(True)

#main
# check for valid arg number
if ((len(sys.argv) - 1) % 2 != 0) or (len(sys.argv) < 2):
	print("Usage: python3 assembler.py asmbFile1.txt binFile1.txt asmbFile2.txt binFile2.txt ...")
	raise TypeError
# gathering file names
parity = 0
fileList = []
temp = []
for x in sys.argv[1:]:
	temp.append(x)
	if parity:
		fileList.append(temp)
		temp = []
	parity = 1 - parity
mainAssembler = Assembler()
for x in fileList:
	mainAssembler.reset()
	readFile = open(x[0], "r")
	mainAssembler.loadPrgrm(readFile.read())
	readFile.close()
	mainAssembler.assemble()
	writeFile = open(x[1], "w")
	writeFile.write(mainAssembler.compiledResult)
	writeFile.close()
