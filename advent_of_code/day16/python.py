hex = {
        "0" : [0,0,0,0],
        "1" : [0,0,0,1],
        "2" : [0,0,1,0],
        "3" : [0,0,1,1],
        "4" : [0,1,0,0],
        "5" : [0,1,0,1],
        "6" : [0,1,1,0],
        "7" : [0,1,1,1],
        "8" : [1,0,0,0],
        "9" : [1,0,0,1],
        "A" : [1,0,1,0],
        "B" : [1,0,1,1],
        "C" : [1,1,0,0],
        "D" : [1,1,0,1],
        "E" : [1,1,1,0],
        "F" : [1,1,1,1],
}

import math
funcs = {
        0 : sum,
        1 : math.prod,
        2 : min,
        3 : max,
        5 : (lambda arr: 1 if arr[0]  > arr[1] else 0),
        6 : (lambda arr: 1 if arr[0]  < arr[1] else 0),
        7 : (lambda arr: 1 if arr[0] == arr[1] else 0),
}

inp = []
for x in open("input.txt").readlines()[0][:-1]:
    inp += hex[x]

def value(arr):
    out = 0
    for x in arr:
        out <<= 1
        out += x
    return out

def read_value(arr, start):
    num = arr[start+1:start+5]
    if arr[start] == 1:
        ret = read_value(arr, start+5)
        return (num + ret[0], ret[1])
    else:
        return (num, start+5)

def read_packet(arr, start, i=0):
    version = value(arr[start:start+3])
    typeid = value(arr[start+3:start+6])
    print("*"*i,"Version", version, "Type", typeid)
    val = None
    end = 0
    if typeid == 4:
        ret = read_value(arr,start+6)
        val = value(ret[0])
        print("*"*i, "Number", val)
        end = ret[1]
    else:
        if arr[start+6] == 1:
            val = []
            amount = value(arr[start+7:start+18])
            print("*"*i, "Amount packets:", amount)
            start = start+18
            for _ in range(amount):
                ret = read_packet(arr, start, i+1)
                start = ret[3]
                val.append(ret[2])
            end = start
        else:
            val = []
            amount = value(arr[start+7:start+22]) + start + 22
            print("*"*i, "Till bits:", amount)
            start += 22
            while start+1 < amount:
                ret = read_packet(arr, start, i+1)
                start = ret[3]
                val.append(ret[2])
            end = start
        val = funcs[typeid](val)
    return (version, typeid, val, end)

print(inp)
print(read_packet(inp,0))
