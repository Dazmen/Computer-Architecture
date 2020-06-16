"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Memory with 256 bytes (RAM)
        self.ram = [0] * 256
        
        # Register, general purpose memory
        self.reg = [0] * 8

        # pc - program counter to track the index/address of instructions in memory
        self.pc = 0
        
        # Bool value determining if the CPU is 'on'
        self.running = True
        
    ### MAR = address/index, MRD = value
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MRD, MAR):
        self.ram[MAR] = MRD

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        instructions = {
            'LDI': 0b10000010, # Load value into register
            'PRN': 0b01000111, # Print the value
            'HLT': 0b00000001 # Halts the program
        }

        while self.running:
            # ir = instruction register
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == instructions['HLT']:
                self.running = False
            elif ir == instructions['PRN']:
                # the next line is the address in the register to print
                reg_address = operand_a
                value = self.reg[reg_address]
                print(value)
                # increment by 2 since there were two lines of instruction
                self.pc += 2
            elif ir == instructions['LDI']:
                #The current IR is an instruction
                #operand_a is IR + 1, which is the memory location
                #operand_b is the IR + 2 which is the value
                reg_address = operand_a
                value = operand_b
                self.reg[reg_address] = value

                # Increment pc by 3 since the instructions read 3 lines of instruction
                self.pc += 3
            else:
                print(f'Unknown Instruction {ir} as address {self.pc}')
                sys.exit(1)



