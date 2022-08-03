def explode_it(nested):
    b, new, _, _ = func(nested)
    return [b,new]

# split it splits every number over 9
def split_it(nested):
    r1, r2 = False, False
    v1, v2 = nested[0], nested[1]
    if isinstance(v1, int):
        if(v1 >= 10):
            ret = v1 //2
            if ret * 2 < v1:
                v1 = [ret, ret+1]
            else:
                v1 = [ret, ret]
            r1 = True
    else:
        r1, v1 = split_it(v1)
    if r1 != True:
        if isinstance(v2, int):
            if(v2 >= 10):
                ret = v2 //2
                if ret * 2 < v2:
                    v2 = [ret, ret+1]
                else:
                    v2 = [ret, ret]
                r2 = True
        else:
            r2, v2 = split_it(v2)
    return (r1 or r2,[v1, v2])


def reduce_it(nested):
    a, b = True, True
    while a or b:
        a = True
        while a:
            a, nested = explode_it(nested)
        b, nested = split_it(nested)
    return nested

def func(nested, depth=0):
    r1, r2 = False, False
    v1, v2 = nested[0], nested[1]
    al, ar = 0, 0
    if depth >= 4 and isinstance(nested, list) and isinstance(v1, int) and isinstance(v2, int):
        return (True, 0, v1, v2)
    else:
        if isinstance(v1, list):
            r1, v1, al, ar = func(v1, depth+1)
        if r1 != True:
            if isinstance(v2, list):
                r2, v2, al, ar = func(v2, depth+1)
        if r1:
            v2 = add_to(v2, ar, isinstance(v2, list))
            ar = 0
        elif r2:
            v1 = add_to(v1, al, not isinstance(v1, list))
            al = 0
    return (r1 or r2, [v1, v2], al, ar)


def add_to(nested, val, left):
    if isinstance(nested, int):
       return nested + val
    else:
        v1, v2 = nested[0], nested[1]
        if left:
            return [add_to(v1, val, left), v2]
        else:
            return [v1, add_to(v2, val, left)]

def magnitude(nested):
    if isinstance(nested, int):
        return nested
    else:
        return 3*magnitude(nested[0]) + 2*magnitude(nested[1])

# dont use this code in production
inp = [eval(x[:-1]) for x in open("input.txt").readlines()]
out = []
cmax = 0
for x in inp:
    for y in inp:
        if x == y:
            continue
        res = magnitude(reduce_it([x,y]))
        if res > cmax:
            print(x,y)
        cmax = max(res, cmax)

print(cmax)
