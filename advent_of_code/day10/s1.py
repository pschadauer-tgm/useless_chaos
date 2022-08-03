inp = open("input.txt").readlines()

opening = {
        "(" : (True, 3),
        ")" : (False, 3),
        "[" : (True, 57),
        "]" : (False, 57),
        "{" : (True, 1197),
        "}" : (False, 1197),
        "<" : (True, 25137),
        ">" : (False, 25137)
}
def parser(char, arr, toparse):
    while True:
        if arr[char] == "\n":
            return (-1, char)
        if opening[arr[char]][0]:
            ret, ch = parser(char+1, arr, arr[char])
            if ret == 0:
                char = ch+1
            else:
                return (ret, char)
        elif opening[arr[char]][1] == opening[toparse][1]:
            return (0, char)
        else:
            print("Expected closing for " + toparse + ", but got " + arr[char])
            return (opening[arr[char]][1], char)

result = []
for x in inp:
   num = parser(1, x, x[0])[0]
   if num not in [0,-1]:
       result.append(num)

print(sum(result))
