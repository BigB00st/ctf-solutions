from subprocess import Popen, PIPE

final = [117, 148, 123, 5, 54, 9, 61, 234, 45, 4, 2, 40, 88, 111, 65, 65, 46, 23, 114, 110, 102, 148, 136, 123, 30, 5, 214, 231, 225, 255, 239, 138, 211, 208, 250, 232, 178, 187, 171, 242, 255, 30, 39, 19, 64, 17, 40, 29, 13, 27]

import json
import string

arg_min_len = 32

i = 7
cur = list('rgbCTF{-------------------------*----------------}')
find_index = cur.index("*")

while "-" in cur:
    if find_index >= len(cur):
        find_index = 0
    cur[find_index] = "*"
    for char in string.printable:
        arg = "".join(cur).replace("*",char)    
        process = Popen(["./itwk.so",arg], stdout=PIPE)
        output,err = process.communicate()
        out_lst = json.loads(output.decode().replace("\n",""))
        if out_lst[i-7] == final[i-7]:
            cur = list(arg)
            i += 1
            find_index += 1
            print("".join(cur))
            break
