def firstlet(s): return s[0]
print(list(map(firstlet,["apple","banana","cherry"])))
def upperify(s): return s.upper()
print(list(map(upperify,["apple","banana","cherry"])))
def whitespace(s): return s.strip()
print(list(map(whitespace,["  hello  ","  world  "," python "])))
def C_to_F(c): return (c*9/5)+32
print(list(map(C_to_F,[0,20,37,100])))
