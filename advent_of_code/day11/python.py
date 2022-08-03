inp = [[int(y) for y in list(x[:-1])] for x in open("input.txt").readlines()]

flashes = 0
current = 0

def increment(x,y):
    global flashes
    global current
    if x < 0 or x >= len(inp) or y < 0 or y >= len(inp[0]):
        return
    if inp[x][y] > 9:
        return
    inp[x][y] += 1
    if inp[x][y] > 9:
        flashes += 1
        current += 1
        increment(x+1,y)
        increment(x-1,y)
        increment(x,y+1)
        increment(x,y-1)
        increment(x+1,y+1)
        increment(x+1,y-1)
        increment(x-1,y+1)
        increment(x-1,y-1)

for z in range(1,1000):
    for x in range(len(inp)):
        for y in range(len(inp[0])):
            increment(x,y)
    if current == len(inp) * len(inp[0]):
        print(z)
        break
    current = 0
    for x in range(len(inp)):
        for y in range(len(inp[0])):
            if inp[x][y] > 9:
                inp[x][y] = 0
                print("\033[95m", end="")
            print(str(inp[x][y]) + "\033[0m", end="")
        print()
    print()


print(flashes)
