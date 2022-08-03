fil = open("input.txt").readlines()
fa = fil[0][:-1]
fb = fil[2:]

temp = {}
mapings = {}

for x in fb:
    a, b = x[:-1].split(" -> ")
    temp[a] = 0
    mapings[a] = b

for i in range(len(fa)-1):
    temp[fa[i:i+2]] += 1 


for _ in range(40):
    newt = {}
    for a, b in mapings.items():
        newt[a] = 0
    for e, a in temp.items():
        x = mapings[e]
        newt[e[0]+x] += a
        newt[x+e[1]] += a
    temp = newt

print(sum([a for _,a in temp.items()]))
from collections import Counter
c = Counter()
for a, b in temp.items():
    c.update({a[0]: b})
print(c)
cm = c.most_common()
print(cm[0][1]-cm[-1][1]-1)
