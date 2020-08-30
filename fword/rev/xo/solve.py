#!/usr/bin/python3
from pwn import *

charset = "etaoinsrhdlucmfywgpbvkxqjz_0123456789ETAOINSRHDLUCMFYWGPBVKXQJZ{}!?"
p = remote("xo.fword.wtf", 5554)
flag = ""


while True:
    for c in charset:
        p.sendlineafter(": \n", '`' * len(flag) + c)
        wrong = int(p.recvline().strip())
        print(flag+c)

        if wrong == len(flag):
            flag += c
            break
