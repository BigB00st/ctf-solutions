import angr

value = 0x265D1D22 + 1

p = angr.Project("./a.out")
func_addr = p.loader.find_symbol("win").rebased_addr
cl = p.factory.callable(func_addr)
cl(value)
print(cl.result_state.posix.stdout.concretize())