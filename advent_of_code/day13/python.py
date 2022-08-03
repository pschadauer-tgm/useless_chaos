file = [x[:-1] for x in open("input.txt").readlines()]
inp = []
command = []
for x in file:
    if x == "":
        pass
    elif x[0] == "f":
        a, b = x[11:].split("=")
        command.append((a, int(b)))
    else:
        a, b = x.split(",")
        inp.append((int(a),int(b)))
inp = set(inp)

for a, b in command:
    new = []
    for x, y in inp:
        if a == "y":
            if y > b:
                y = b-y+b
        else:
            if x > b:
                x = b-x+b
        new.append((x,y))
    inp = set(new)
for x in range(6):
    for y in range(40):
        if (y,x) in inp:
            print("■", end="")
        else:
            print(" ", end="")
    print()
