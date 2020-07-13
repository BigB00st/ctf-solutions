import itertools
import copy

n = 12
x = 4

lst = [2**i for i in range(n)]

base_groups = [[] for i in itertools.repeat(None, x)]
base_num = [0 for i in itertools.repeat(None, n)]

def split_to_groups(mask):
    groups = copy.deepcopy(base_groups)
    for i, digit in enumerate(mask):
        groups[digit].append(lst[i])
    
    return [sum(group) for group in groups]

# big endian
def num_base_n(num, base):
    ret = copy.deepcopy(base_num)
    i = 0
    while num > 0:
        mod = num % base
        ret[i] = mod
        num //= base
        i += 1
    return ret

def num_groups(mask):
    return len(set(mask))

final = set()

for i in range(x**n):
    mask = num_base_n(i, x)
    if num_groups(mask) != x:
        continue
    cur = split_to_groups(mask)
    final.add((tuple(sorted(cur))))

print(len(final))