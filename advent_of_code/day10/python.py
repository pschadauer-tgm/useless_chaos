inp = open("input.txt").readlines()

lut = {
        "(" : (True, 3),
        ")" : (False, 3),
        "[" : (True, 57),
        "]" : (False, 57),
        "{" : (True, 1197),
        "}" : (False, 1197),
        "<" : (True, 25137),
        ">" : (False, 25137)
}

lut2 = {
        "(" : 1,
        "[" : 2,
        "{" : 3,
        "<" : 4
}

def parser(pos, arr):
    toparse = arr[pos]
    while pos+1 < len(arr):
        pos += 1
        if arr[pos] == "\n":
            return (0, pos, lut2[toparse])
        if lut[arr[pos]][0] == True:
            num, rpos, cl = parser(pos, arr)
            if num > 0:
                pos = rpos
            elif cl != None:
                return (0, pos, cl*5 + lut2[toparse])
            else:
                return (num, rpos, None)
        # if closing for current parser
        if lut[arr[pos]][1] == lut[toparse][1]:
            if arr[pos+1] == "\n":
                return (0,pos,0)
            elif lut[arr[pos+1]][0] == True:
                pos += 1
            else:
                return (1, pos+1, None)
        # if wrong closing
        if lut[arr[pos]][0] == False:
            #return (lut[arr[pos]][1], pos, None)
            return (0,pos,None)
        toparse = arr[pos]
    return (-1, pos, None)

output = []
for x in inp:
    out = parser(0, x)
    if out[2] != None:
        output.append(out[2])

print(sorted(output)[len(output)//2])
