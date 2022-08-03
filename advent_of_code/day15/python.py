def val(a,b):
    a += b
    if a > 9:
        a -= 9
    return a
inp = [[[val(int(x),i) for z in x] for i, x in enumerate([y[:-1]]*5)] for y in open("input.txt").readlines()]
print(inp[0])
c_best = [[999999999999999999999999999]*len(inp[0]) for _ in range(len(inp[0]))]




def rec_dij(x,y,current,was=[]):
    global inp
    global c_best
    current += inp[x][y]
    # if finished
    if x+1 == len(inp) and y+1 == len(inp[0]):
        return current
    if current >= c_best[x][y]:
        return None
    else:
        c_best[x][y] = current
    out = []
    for a, b in [(1,0),(0,1)]:
        if x+a != -1 and x+a != len(inp) and y+b != -1 and y+b != len(inp[0]):
            r = rec_dij(x+a,y+b, current, was)
            if r != None:
                out.append(r)
    if out == []:
        return None
    else:
        mina = min(out)
        return mina

print(rec_dij(0,0,0,[])-inp[0][0])
