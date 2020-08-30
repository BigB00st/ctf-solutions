from pwn import *

r = remote("repeat.fword.wtf", 4545)

r.sendlineafter("Your Option :", "1")
r.recvuntil("The Message is : ")
num = r.recvline().strip().decode()

groups = [num[i:i+5] for i in range(0, len(num), 5)]
hexstr = hex(int(''.join(['1' if x.count('1') > x.count('0') else '0' for x in groups]), 2))
print(bytearray.fromhex(hexstr[2:]).decode())