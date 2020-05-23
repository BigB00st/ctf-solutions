from pwn import *

r = remote("challs.m0lecon.it",10000)
for i in range(10):
	r.recvuntil("N = ")
	N = r.recvline().replace("\n","")
	a,b = int(N)-1,1
	print a,b
	r.sendline(str(a) + " " + str(b))
r.interactive()
r.close()

