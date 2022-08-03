file = open("input.txt")
inp = [x for x in file.readlines()]
inpnum = [int(x) for x in inp[0].split(",")]
inpbin = []
current = []
for i in inp[2:]:
    if i != "\n":
        current.append([int(x) for x in i[:-1].strip().replace("  ", " ").split(" ")])
    if len(current) == 5:
        inpbin.append(current)
        current = []
from functools import reduce
from operator import add

def calculate():
    for i in range(1,len(inpnum)):
        setnum = set(inpnum[:i+1])

        for bingo in list(inpbin):
            for row in range(len(bingo)):
                if set([x[row] for x in bingo]).issubset(setnum) or set(bingo[row]).issubset(setnum):
                    print(bingo)
                    inpbin.remove(bingo)
                    if len(inpbin) == 0:
                        print(bingo)
                        nwm = inpnum[i]
                        sumrest = sum([x for x in reduce(add, bingo) if x not in setnum])
                        return (nwm, sumrest)
                    break

print(calculate())
print(inpbin)
