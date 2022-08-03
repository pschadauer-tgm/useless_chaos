# input:
# target area: x=20..30, y=-10..-5
#xmin = 20
#xmax = 30
#ymin = -10
#ymax = -5

# target area: x=281..311, y=-74..-54
xmin = 281
xmax = 311
ymin = -74
ymax = -54

#get possible x components
x = []
got = False
counter = 0
while True:
    current = sum(list(range(counter+1)))
    if xmin < current and current < xmax:
        x.append(counter)
        got = True
    else:
        if got:
            break
    counter += 1

print(x)

def inbound(x,y):
    #y -= 1
    cx = 0
    cy = 0
    high = 0
    while cx < xmax+1 and cy+1 > ymin:
        cx += x
        cy += y
        high = max(high, cy)
        if xmin <= cx <= xmax and ymin <= cy <= ymax:
            #print(high)
            return True
        if x < 0:
            x += 1
        elif x > 0:
            x -= 1

        y -= 1
    return False

y = -1
amount = 0

for change in range(x[0], xmax+2):
    for counter in range(-abs(ymin), abs(ymin)+1):
        current = inbound(change, counter)
        if current:
            amount += 1
            y = max(y,counter)

print(amount)
