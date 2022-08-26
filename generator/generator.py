import json
import sys

class ISA:
    instructions = []

class InstructionClass:
    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.format = []
        self.instructions = []
    def reprJSON(self):
        return self.__dict__

class Instruction:
    def __init__(self, opcode, name, short, description):
        self.opcode = opcode
        self.name = name
        self.short = short
        self.description = description
    def reprJSON(self):
        return self.__dict__

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

isa = []

with open(sys.argv[1], 'r') as f:
    ic = InstructionClass('', '')
    for line in f.readlines():
        # header line
        if line[0] == '#':
            headerLine = line[2:-1]
            className = ''.join(headerLine.split(' ')[:-1])
            className = className.lower().replace(' ', '')
            ic = InstructionClass(className, line[2:-1])
            isa.append(ic)
        elif line[0] == '\n':
            continue
        else:
            instructionLine = line.split('\t')
            # print(instructionLine)
            inst = Instruction(instructionLine[0], instructionLine[1], instructionLine[2].split('.')[0], instructionLine[2][:-1])
            ic.instructions.append(inst)

with open('out.json', 'w') as f:
    outObj = { 'isa': isa}
    f.write(json.dumps(outObj, indent=4, cls=ComplexEncoder))