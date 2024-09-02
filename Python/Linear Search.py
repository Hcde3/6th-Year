list_len = int(input("How long is your list:\n"))
L = []
for list_els in range(list_len): L.append(input("Input an element\n"))
print(L)
t = input("What is your target value?\n")
for i,u in enumerate(L):
    if u == t:
        print(f"Index: {i}")
        break