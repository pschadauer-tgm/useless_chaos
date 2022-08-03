import math
inp = [[int(y) for y in x[:-1]] for x in open("input.txt").readlines()]

def get(x,y):
    if x >= len(inp) or x < 0 or y >= len(inp[0]) or y < 0:
        return 9
    else:
        return inp[x][y]

def basin(x,y,was=[]):
    was.append((x,y))
    result = 1
    if get(x+1,y) != 9 and (x+1,y) not in was:
        o, w = basin(x+1,y, was)
        was = w
        result += o
    if get(x-1,y) != 9 and (x-1,y) not in was:
        o, w = basin(x-1,y, was)
        was = w
        result += o
    if get(x,y+1) != 9 and (x,y+1) not in was:
        o, w = basin(x,y+1, was)
        was = w
        result += o
    if get(x,y-1) != 9 and (x,y-1) not in was:
        o, w = basin(x,y-1, was)
        was = w
        result += o
    return (result, was)

nums = []

for x in range(len(inp)):
    for y in range(len(inp[x])):
        if get(x+1,y) > get(x,y) and get(x-1,y) > get(x,y) and get(x, y+1) > get(x,y) and get(x,y-1) > get(x,y):
            nums.append(basin(x,y)[0])

print(nums)
print(math.prod(sorted(nums)[-3:]))
