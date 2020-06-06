import angr

func_addr = 0x40056D

p = angr.Project("./maze")
cl = p.factory.callable(func_addr)
cl(2,52,39)
print(cl.result_state.posix.stdout.concretize())
