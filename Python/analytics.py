def simplesort(l):
    NL = []
    for x in range(len(l)):
        sml = False
        smlindex = 0
        for index,smlfind in enumerate(l):
            if not sml: sml = smlfind
            if smlfind < sml:
                smlindex = index
                sml = smlfind
        NL.append(sml)
        del l[smlindex]
    return NL

def mean(l):
    total = 0
    for x in l: total += x
    return total/len(l)

def median(l):
    l = simplesort(l)
    lngth = len(l)
    if not lngth%2: return (l[int(lngth/2)]-1,l[int(lngth/2)])
    else: return l[round(lngth/2)-1]
    
def mode(l):
    nums = []
    for el in l:
        present = False
        for i,x in enumerate(nums):
            if el == x[0]:
                nums[i] = (x[0],x[1]+1)
                present = True
        if not present: nums.append((el,1))
    mod = nums[0]
    for n in nums:
        if mod[1] < n[1]: mod = n
    return mod

def frequency(l):
    nums = []
    for el in l:
        present = False
        for i,x in enumerate(nums):
            if el == x[0]:
                nums[i] = (x[0],x[1]+1)
                present = True
        if not present: nums.append((el,1))
    return nums

def top5(l): return simplesort(l)[-5:]
def bot5(l): return simplesort(l)[:5]
    



TestSet = [1,6,2,8,2,7,12,43,77,11,975,333,11,-55,11,-62,-10,43,20]
list_len = input("(type ts for TestSet)\nHow long is your list?:\n")
if list_len == "ts":
    print(TestSet)
    L = TestSet
else:
    L = []
    for list_els in range(int(list_len)): L.append(int(input("Input a number:\n")))
    print(L)
choice = input("Choose a procedure:\n(1)Mean\n(2)Median\n(3)Mode\n(4)Frequency\n(5)Largest 5\n(6)Lowest 5\n")
if choice == "1": print(f"Mean of List: {mean(L)}")
if choice == "2": print(f"Median(s) of List: {median(L)}")
if choice == "3": print(f"Mode of List: {mode(L)[0]} appears {mode(L)[1]} times")
if choice == "4": print(f"Frequency of Numbers in List: {frequency(L)}")
if choice == "5": print(f"Largest 5 in List: {top5(L)}")
if choice == "6": print(f"Lowest 5 in List: {bot5(L)}")



