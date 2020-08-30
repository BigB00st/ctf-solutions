from pwn import *
from randcrack import RandCrack

rc = RandCrack()

r = remote("twistwislittlestar.fword.wtf", 4445)
#p.interactive()


for i in range(3):
    r.recvuntil("Random Number is : ")
    n = int(r.recvline().strip())
    print(n)
    rc.submit(n)
    

def get_n():
    r.recvuntil("Your Prediction For the next one : ")
    r.sendline("0")
    r.recvuntil("The number was : ")
    n = int(r.recvline().strip())
    print(n)
    return n
    
for i in range(624-3):
    rc.submit(get_n())

for _ in range(20):
    r.sendline(str(rc.predict_getrandbits(32)))

r.interactive()
