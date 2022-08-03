inp = open("input.txt").readlines()[0].split(",")
inp = sorted([int(x) for x in inp])
print(sum(inp)/len(inp))

current = 0
minfuel = 9999999999999999999

for e in inp:
    cost = sum([sum(range(abs(y - e)+1)) for y in inp])
    if cost < minfuel:
        current = e
        minfuel = cost

print(current)
print(minfuel)
