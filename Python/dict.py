file = open("book.txt","r")
choice = input("(c) for Characters\n(w) for Words\n")
if choice == "w":
    content = []
    for line in file:
        n_l = line.strip()
        n_l = n_l.split(",")
        n_ll = []
        for ne in n_l: n_ll.extend(ne.split(" "))
        n_lll = []
        for ne in n_ll: n_lll.extend(ne.split("."))
        new_content = [ne.lower() for ne in n_lll]
        content.extend(new_content)
    print(content)
    wordcount = {}
    for word in content:
        try: wordcount[word] = wordcount[word] + 1
        except: wordcount[word] = 1
    print("Words","  "*15,"Count")
    for word,count in wordcount.items():
        print(word,"  "*(20-(len(word))),count)
else:
    charcount = {}
    for line in file:
        line = line.strip()
        for char in line:
            try: charcount[char] = charcount[char] + 1
            except: charcount[char] = 1
    print("Characters","  "*10,"Count")
    for char,count in charcount.items():
        print(char,"  "*(19),count)
    
