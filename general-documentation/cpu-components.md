# Components of the HARM8 CPU:

## Clock
### It runs at 262,144hz/262.14khz/0.26mhz
### Each instruction execution/machine cycle is 5 ticks, so the CPU runs at approximately 52428 IPS/52.42 KIPS
### No microcode instructions associated with this component

## Accumulator
### Stores 8 bits of data
### Represented by "Acc" in the mathematical descriptions of the actions of each instruction
### The AI microcode instruction tells the accumulator to, upon the clock cycle during which it is performed, read from the central bus and store that data within itself
### The AO microcode instruction tells the accumulator to, during the clock cycle when it is performed, set the data in the central bus to the value within itself
### It is wired to constantly output to the first input of the ALU

## B Register
### Stores 8 bits of data
### Not shown in the mathematical description of the actions of each instruction
### The BI microcode instruction tells the B register to, upon the clock cycle during which it is performed, read from the central bus and store that data within itself
### It is wired to constantly output to the second input of the ALU

## Program Counter
### Stores 5 bits of data
### Represented by "PC" in the mathematical descriptions of the actions of each instruction
### The CIA microcode instruction tells the program counter to, upon the clock cycle during which it is performed, read from the lower 5 bits of the central bus and store that data within itself
### The CO microcode instruction tells the program counter to, during the clock cycle when it is performed, set the data in the lower 5 bits of the central bus to the value within itself
### The CE microcode instruction tells the program counter to, upon the clock cycle during which it is performed, increment its internal value (and triggers the [HLT microcode instruction](https://github.com/HappyFakeBoulder/FreeCPU-HARM8/blob/master/general-documentation/cpu-components.md#the-hlt-microcode-instruction-activates-the-halting-system) if the value overflows from the increment)
### The CIZ microcode instruction tells the program counter to, upon the clock cycle during which it is performed, read from the lower 5 bits of the central bus and store that data within itself, but only if the zero flag is set to 1
### The CIC microcode instruction tells the program counter to, upon the clock cycle during which it is performed, read from the lower 5 bits of the central bus and store that data within itself, but only if the carry flag is set to 1

## Address Register
### Stores 5 bits of data
### Not shown in the mathematical description of the actions of each instruction
### It is wired to constantly output to the address port of the RAM
### The MAI microcode instruction tells the address register to, upon the clock cycle during which it is performed, read from the lower 5 bits of the central bus and store that data within itself

## Instruction Register
### Stores 8 bits of data
### Not shown in the mathematical description of the actions of each instruction
### It is wired to constantly output its *upper* five bits to the opcode input of the control logic
### The IRI microcode instruction tells the instruction register to, upon the clock cycle during which it is performed, read from the data output of the RAM and store that data within itself
### The IRO microcode instruction tells the instruction register to, during the clock cycle when it is performed, set the data in the lower 5 bits of the central bus to the lower five bits of the value within itself

## RAM
### Stores 32 words of data
### As each word is 8 bits, it stores 32 bytes
### Represented by "M" in the mathematical descriptions of the actions of each instruction
### Has a 5-bit address input port, which is wired to constantly input from the value output on the address register
### Has an 8-bit dual-directional data port
### It is used to store both data and program
### The MDI microcode instruction tells the RAM to, upon the clock cycle during which it is performed, read from the central bus and store that data within the spot within itself that is currently addressed
### The MDO microcode instruction tells the RAM to, during the clock cycle when it is performed, set the data in the central bus to the value in the spot within itself that is currently addressed

## Input port
### Transfers 8 bits of data, plus 1 bit of output to notify the user when input is wanted and 1 bit of input for the user to say when they are finished
### Represented by "input" in the mathematical descriptions of the actions of each instruction
### Connected to the input wait circuit, so as to delay the clock until the user enables the extra input bit to signify finishing whenever input is required
### The IO microcode instruction tells the input port to notify the user that input is desired, then use the input wait circuit to disable other function until user finishes input, and then set the data in the central bus to the data the user had input

## Input wait circuit
### Connected to the clock, so as to stop the clock when it creates a delay until the delay is finished
### Delays in this are created when the input port is told to get input with the IO microcode instruction
### No microcode instructions associated with this component

## Output register/port
### Stores 8 bits of data
### Represented by "output" in the mathematical descriptions of the actions of each instruction
### Constantly outputs that data to the output port
### The OI microcode instruction tells the output register to, upon the clock cycle during which it is performed, read from the central bus and store that data within itself

## ALU
### Processes on 8 bits of data, with two inputs and one output
### The first input is connected to the accumulator; the second input is connected to the B register
### Connected to the flag registers
### Has two operations; only outputs the result of one of them at a time (default is addition, the other is bitwise NAND)
### The ΣO (sum out) microcode instruction tells the ALU to, during the clock cycle during which it is performed, set the data in the central bus to the output from itself; it also sets the zero flag, and the carry flag if it is doing addition
### The ALU microcode instruction tells the ALU to, during the clock cycle during which it is performed, switch its calculation mode to bitwise NAND instead of addition

## Flag Registers
### Two 1-bit registers - zero flag and carry flag
### Connected to the ALU, set during the ΣO microcode instruction
### Zero flag is set if the ALU's output is equal to 00000000
### Carry flag is set if the ALU's processing mode is addition and the addition resulted in a carry-out; it is only updated when the ALU's processing mode is addition
### Flags are used in conditional jumps
### No microcode instructions associated with this component

## Central Data Bus
### 8 bits wide
### Almost all other components are connected to it in some way, so as to transfer data between them
### No microcode instructions (directly) associated with this component

## Reset system
### Sets all registers to all zeros when activated, and starts up the clock if it was not already
### No microcode instructions associated with this component

## Halting system
### The clock will be stopped until the reset signal is sent when this is activated
### The HLT microcode instruction activates the halting system

## Control logic
### Primarily consists of a ROM, with 18-bit words and 5-bit addressing (32 words)
### The upper five bits of the instruction register are connected to the ROM's address port
### 

# This listing is not complete. More will be added soon.
