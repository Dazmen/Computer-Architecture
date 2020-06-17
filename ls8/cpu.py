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
        # Initialize the last spot in the register to the pointer of the beginning of the stack
        self.reg[7] = 0xf4

        # pc - program counter to track the index/address of instructions in memory
        self.pc = 0

        # stp - STack Pointer, points to a location in the register that contains the current position in the stack
        self.stp = self.reg[7]
        
        # Bool value determining if the CPU is 'on'
        self.running = True

        # Instructions Table
        self.branch_table = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b00000001: self.HLT,
            0b01000101: self.PUSH,
            0b01000110: self.POP
        }
        
    ### MAR = address/index, MRD = value
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MRD, MAR):
        self.ram[MAR] = MRD

    def load(self):
        """Load a program into memory."""
        # Dynamic load method
        file = sys.argv[1]
        address = 0

        with open(file) as f:
            for line in f:
                split_line = line.split(' ')[0].strip("\n")
                # print(split_line)
                if len(split_line) == 8:
                    self.ram[address] = int(split_line, 2)
                    address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
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

    def HLT(self):
        self.running = False

    def PRN(self):
        reg_address = self.ram_read(self.pc + 1)
        value = self.reg[reg_address]
        print(f'PRN -> {value}')

    def LDI(self):
        reg_address = self.ram_read(self.pc+1)
        value = self.ram_read(self.pc+2)
        self.reg[reg_address] = value

    def MUL(self):
        num1 = self.ram_read(self.pc + 1)
        num2 = self.ram_read(self.pc +2 )
        self.alu("MUL", num1, num2)

    def PUSH(self):
        self.stp -= 1
        reg_address = self.ram[self.pc + 1]
        value = self.reg[reg_address]
        self.ram[self.stp] = value

    def POP(self):
        reg_address = self.ram[self.pc + 1]
        value = self.ram[self.stp]
        self.reg[reg_address] = value
        self.stp += 1


    def run(self):
        """Run the CPU."""

        while self.running:
            # ir = instruction register
            ir = self.ram_read(self.pc)

            if ir in self.branch_table:
                self.branch_table[ir]()
                # creates a 'mask' and then shifts off the unneeded binary to get the number of operands
                operands = (ir & 0b11000000) >> 6
                # increment the pc by the number of operands + 1 (for the instruction itself)
                self.pc += operands + 1

            else:
                print(f'Unknown Instruction {ir} as address {self.pc}')
                sys.exit(1)



