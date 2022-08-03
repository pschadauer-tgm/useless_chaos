file = open("input.txt")
inp = [x.split(" ") for x in file.readlines()]
inp = [(x[0], int(x[1])) for x in inp]

horizontal = 0
depth = 0
aim = 0
for command, amount in inp:
    if command == "forward":
        horizontal += amount
        depth += aim * amount
    elif command == "up":
        aim -= amount
    elif command == "down":
        aim += amount
    else:
        print("Unknown command: " + command)
print(str(horizontal) + "," + str(depth))
print(horizontal * depth)
