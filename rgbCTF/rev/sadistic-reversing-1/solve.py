from subprocess import Popen, PIPE

final = [114, 20, 119, 59, 104, 47, 75, 56, 81, 99, 23, 71, 56, 75, 124, 31, 65, 32, 77, 55, 103, 31, 96, 18, 76, 41, 27, 122, 29, 47, 83, 33, 78, 59, 10, 56, 15, 34, 94]

import json
import string

i = 0
cur = ""
while i < len(final):
    for char in string.printable:
        arg = cur + char    
        process = Popen(["./itJX.so",arg], stdout=PIPE)
        output,err = process.communicate()
        out_lst = json.loads(output.decode().replace("\n",""))
        if out_lst[i] == final[i]:
            cur += char
            i += 1
            print(cur)
            break