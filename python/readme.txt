To use this system, just write your assembly program in a text file, then use bash and enter 'python3 assembler.py asmb.txt bin.txt',
where asmb.txt is the file that the assembly program is in and bin.txt is the file you want the binary to be saved in. After that,
put in bash 'python3 harm8vm.py -args bin.txt', where bin.txt is the binary file and -args is the boolean arguments you want to use
to control the execution of the program. -s makes the VM run more slowly, -m displays the contents of memory after each instruction
execution, and -e displays the contents of memory once at the end of the program. -sm makes the VM run more slowly and display the
contents of memory after each instruction execution, and -se makes the VM run more slowly and display the contents of memory once at the
end of the program. -sme makes the VM run more slowly, displays the contents of memory after each instruction execution, and displays
the contents of memory once at the end of the program.
