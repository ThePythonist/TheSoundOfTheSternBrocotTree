#!/usr/bin/python3.8

class List:
    def __init__(self, x, n):
        self.x = x
        self.n = n
    
    def get(self, k):
        if k == 0:
            return []
        return [self.x] + self.n().get(k-1)

def nop(x):
    return x

def tuple_to_fraction(x):
    return f"{x[0]}/{x[1]}"

class Tree:
    def __init__(self, x, l, r):
        self.x = x
        self.l = l
        self.r = r
    
    def listify(self):
        return Tree([self.x], lambda: self.l().listify(), lambda: self.r().listify())
    
    @staticmethod
    def merge(a, b):
        return Tree(
            a.x+b.x,
            lambda: Tree.merge(a.l(), a.r()),
            lambda: Tree.merge(b.l(), b.r())
        )
    
    def bfs(self):
        def aux(left, right):
            merged = Tree.merge(left, right)
            return List(merged.x, lambda: aux(merged.l(), merged.r()))
        return List([self.x], lambda: aux(self.l().listify(), self.r().listify()))
    
    def draw(self, depth, spacing=1, transformation=nop):
        rows = self.bfs().get(depth)
        maxLength = 1
        for y in rows:
            for x, c in enumerate(y):
                y[x] = (n := transformation(c))
                if (newLength:=len(str(n))) > maxLength:
                    maxLength = newLength
        rowStrings = []
        rowWidth = (maxLength+spacing)*2**(len(rows)-1)
        for i, row in enumerate(rows):
            width = (maxLength+spacing)*2**(len(rows)-1-i)
            if i > 0:
                for j in range(width//2):
                    ax = ("/" + (" "*j*2) + "\\").center(2*width)
                    rowStrings.append(ax * (rowWidth//len(ax)))
            elts = list(str(x).center(width) for x in row)
            rowStrings.append("".join(elts))
        output = "\n".join(rowStrings)
        print(output)
        return output
    
    def find(self, k):
        if k == 1:
            return self.x
        return (self.r if k%2 else self.l)().find(k//2)
    
    def traverse(self, start=1):
        return List(self.find(start), lambda: self.traverse(start=start+1))


def mediant(a, b):
    return tuple(x+b[i] for i, x in enumerate(a))

def stern_brocot_tree(x, l, r):
    return Tree(
        x,
        lambda: stern_brocot_tree(mediant(l, x), l, x),
        lambda: stern_brocot_tree(mediant(x, r), x, r)
    )

