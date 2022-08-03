inp = open("input.txt").readlines()
pattern = [x.split(" | ")[0] for x in inp]
nums = [x.split(" | ")[1] for x in inp]

from collections import Counter

lut = {}
lut["abcefg"] = 0
lut["cf"] = 1
lut["acdeg"] = 2
lut["acdfg"] = 3
lut["bcdf"] = 4
lut["abdfg"] = 5
lut["abdefg"] = 6
lut["acf"] = 7
lut["abcdefg"] = 8
lut["abcdfg"] = 9

suma = 0

for i, x in enumerate(pattern):
    c = Counter(x.replace(" ",""))
    patterns = pattern[i].split(" ")
    patternone = [x for x in patterns if len(x) == 2][0]
    patternfour = [x for x in patterns if len(x) == 4][0]
    lookup = {}
    for letter, count in c.items():
        if count == 8:
            if letter in patternone:
                lookup[letter] = "c"
            else:
                lookup[letter] = "a"
        if count == 6:
            lookup[letter] = "b"
        if count == 7:
            if letter in patternfour:
                lookup[letter] = "d"
            else:
                lookup[letter] = "g"
        if count == 4:
            lookup[letter] = "e"
        if count == 9:
            lookup[letter] = "f"
    current = 0
    for e in nums[i][:-1].split(" "):
        string = "".join(sorted([lookup[z] for z in e]))
        num = lut[string]
        current *= 10
        current += num
    print(current)
    suma += current
print(suma)
