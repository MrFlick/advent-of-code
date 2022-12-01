
registers = {
    "w": ('val', 0),
    "x": ('val', 0),
    "y": ('val', 0),
    "z": ('val', 0)
}

def is_val(expr):
    return(expr[0] == 'val')

def is_zero(expr):
    return(is_val(expr) and expr[1] == 0)

def is_one(expr):
    return(is_val(expr) and expr[1] == 1)

def is_input(expr):
    return(expr[0] == 'input')

with open("2021-Day24.txt",  encoding="utf-8") as f:
    input_index = 0
    for line in f:
        parts = line.strip().split(" ")
        cmd = parts[0]

        #for k, v in registers.items():
        #    print(f"{k}: {v}")
        #pass
        #print(line)
        if cmd == "inp":
            registers[parts[1]] = ('input', input_index)
            input_index += 1
            continue

        r1 = parts[1]
        r2 = parts[2]
        rv1 = registers[r1]
        if r2.isnumeric() or r2[0]=="-":
            rv2 = ('val', int(r2))
        else:
            rv2 = registers[r2]

        if cmd == "add":
            if is_zero(rv2):
                continue #Noop
            if is_zero(rv1):
                registers[r1] = rv2
                continue
            if is_val(rv1) and is_val(rv2):
                registers[r1] = ('val', rv1[1] + rv2[1])
                continue
        if cmd == "mul":
            if is_one(rv2):
                continue #Noop
            if is_one(rv1):
                registers[r1] = rv2
                continue
            if is_zero(rv1) or is_zero(rv2):
                registers[r1] = ('val', 0)
                continue
            if is_val(rv1) and is_val(rv2):
                registers[r1] = ('val', rv1[1] * rv2[1])
                continue
        if cmd == "div":
            if is_one(rv2):
                continue #Noop
            if is_val(rv1) and is_val(rv2):
                registers[r1] = ('val', int(rv1[1] / rv2[1]))
                continue
        if cmd == "mod":
            if is_zero(rv1):
                continue #Noop
            if is_val(rv1) and is_val(rv2):
                registers[r1] = ('val', rv1[1] % rv2[1])
                continue
        if cmd == "eql":
            if is_val(rv1) and is_val(rv2):
                if rv1[1] == rv2[1]:
                    registers[r1] = ('val', 1)
                else:
                    registers[r1] = ('val', 0)
                continue
            if is_input(rv1) and is_val(rv2):
                if rv2[1] <= 0 or rv2[1] >= 10:
                    registers[r1] = ('val', 0)
                    continue
            if is_val(rv1) and is_input(rv2):
                if rv1[1] <= 0 or rv1[1] >= 10:
                    registers[r1] = ('val', 0)
                    continue

        registers[r1] = (cmd, rv1, rv2)

print(registers["z"])
