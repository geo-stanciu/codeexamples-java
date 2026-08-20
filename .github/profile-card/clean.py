import sys
lines = sys.stdin.read().split("\n")
W = max(len(l) for l in lines)
g = [list(l.ljust(W)) for l in lines]
H = len(g)
for _ in range(2):
    drop = []
    for y in range(H):
        for x in range(W):
            if g[y][x] == " ":
                continue
            n = sum(1 for dy in (-1,0,1) for dx in (-1,0,1)
                    if (dy or dx) and 0 <= y+dy < H and 0 <= x+dx < W and g[y+dy][x+dx] != " ")
            if n < 3:
                drop.append((y, x))
    for y, x in drop:
        g[y][x] = " "
print("\n".join("".join(r).rstrip() for r in g))
