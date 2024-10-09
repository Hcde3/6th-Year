def listadd(l):
    n = l.pop(0)
    if len(l) > 1:return n + listadd(l)
    else: return n + l[0]

def integersum(i):
    if i>1:return i + integersum(i-1)
    else: return 1

def has_digit(s):
    if s[0].isdigit():return True
    elif len(s) == 1: return False
    else: return has_digit(s[1:])
    
print(listadd([1,2,3,4]))
print(integersum(3))
print(has_digit("gsgsgxg1"))
