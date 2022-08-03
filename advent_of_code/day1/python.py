file = open("input.txt")
inp = [int(x) for x in file.readlines()]
# For part 2
inp = [sum(inp[0+i:3+i]) for i in range(0, len(inp)-2)]
out = 0
for i in range(1, len(inp)):
    if inp[i] > inp[i-1]:
        out += 1
print(out)
