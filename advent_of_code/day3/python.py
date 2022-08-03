file = open("input.txt")
def ftov(arr, mc, digit=0):
    if len(arr) == 1:
        return sum(x << i for i, x in enumerate(reversed(arr[0])))
    value = sum([arr[x][digit] for x in range(len(arr))])
    if mc:
        return ftov(list(filter(lambda x: x[digit] == (value >= len(arr)/2), arr)), mc, digit+1)
    else:
        return ftov(list(filter(lambda x: x[digit] == (value < len(arr)/2), arr)), mc, digit+1)
inp = [list(x)[:-1] for x in file.readlines()]
inp = [[int(y) for y in x] for x in inp]
print("Solution to part 2: ")
print(ftov(inp, True)*ftov(inp, False))
out = [sum([inp[x][y] for x in range(len(inp))]) for y in range(len(inp[0]))]
out = [x > len(inp)/2 for x in out]
epsilon = 0
gamma = 0
for x in out:
    epsilon <<= 1
    gamma <<= 1
    if x:
        epsilon += 1
    else:
        gamma += 1

print("Solution to part 1: ")
print(epsilon * gamma)
