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
### The CI microcode instruction tells the program counter to, upon the clock cycle during which it is performed, read from the lower 5 bits of the central bus and store that data within itself
### The CO microcode instruction tells the program counter to, during the clock cycle when it is performed, set the data in the lower 5 bits of the central bus to the value within itself
### The CE microcode instruction tells the program counter to, upon the clock cycle during which it is performed, increment its internal value (and halt the HARM8 if the value overflows from the increment)

