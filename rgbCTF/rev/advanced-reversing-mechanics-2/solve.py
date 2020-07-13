import angr
import logging

correct = [b'\n', b'\xfb', b'\xf4', b'\x88', b'\xdd', b'\x9d', b'}', b'_', b'\x9e', b'\xa3', b'\xc6', b'\xba', b'\xf5', b'\x95', b']', b'\x88', b';', b'\xe1', b'1', b'P', b'\xc7', b'\xfa', b'\xf5', b'\x81', b'\x99', b'\xc9', b'|', b'#', b'\xa1', b'\x91', b'\x87', b'\xb5', b'\xb1', b'\x95', b'\xe4']
charset = 'etaoinsrhdlucmfywgpbvkxqjz_0123456789ETAOINSRHDLUCMFYWGPBVKXQJZ{}'

p = angr.Project("./hard.o")
func_addr = p.loader.find_symbol("encryptFlag").rebased_addr
cl = p.factory.callable(func_addr)
flag = "rgbCTF{"

angr.options.FAST_MEMORY = True
angr.options.FAST_REGISTERS = True
logging.disable(logging.WARNING)

for _ in range(35 - len(flag)):
    for c in charset:
        print(flag + " " + c, end='\r')
        cl(flag + c)
        lst = cl.result_state.mem[cl.result_state.regs.r0].char.array(35).resolved

        res = True
        for x, y in zip(correct, lst[:len(flag) + 1]):
            if (x == y).is_false():
                res = False
                break
        if res:
            flag += c
            break
print(flag)