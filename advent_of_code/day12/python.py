inp = [x[:-1].split("-") for x in open("input.txt").readlines()]

counter = 0

class Node:
    def __init__(self, name):
        self.name = name
        self.cons = {}
    def add(self, node):
        self.cons[node.name] = node
        if self.name not in node.cons:
            node.add(self)
    def s_end(self, was={}, stri="", already = 0):
        global counter
        stri += self.name + " "
        if self.name == "end":
            counter += 1
            print(stri)
            return
        was2 = was.copy()
        if self.name.islower():
            if self.name not in was2:
                was2[self.name] = 0
            if self.name in ["start","end"]:
                was2[self.name] += 2
            else:
                was2[self.name] += 1
                if was2[self.name] == 2:
                    already = 1
        for n, e in self.cons.items():
            if n not in was2:
                e.s_end(was2, stri, already)
            elif was2[n] < (2-already):
                e.s_end(was2, stri, already)



nodes = {}

for a,b in inp:
    if a not in nodes:
        nodes[a] = Node(a)
    if b not in nodes:
        nodes[b] = Node(b)
    nodes[a].add(nodes[b])

nodes["start"].s_end()
print(counter)
