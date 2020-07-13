grid_len = 5000
visited = "A"
hit = "1"
miss = "0"

def mark(y,x ):
    grid[y][x] = visited
    if y < grid_len-1 and grid[y+1][x] == hit:
        mark(y+1, x)
    if y > 0 and grid[y-1][x] == hit:
        mark(y-1,x)
    if x < grid_len-1 and grid[y][x+1] == hit:
        mark(y,x+1)
    if x > 0 and grid[y][x-1] == hit:
        mark(y,x-1)

with open("grid.txt") as f:
    f = f.read()
lines = f.split()
grid = [list(line) for line in lines]
num_islands = 0

for y in range(5000):
    for x in range(5000):
        if grid[y][x] == hit:
            num_islands += 1
            mark(y, x)

print(num_islands)