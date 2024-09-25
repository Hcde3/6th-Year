file = open("book.txt","r")
answered = False
while not answered:
    answered = True
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
            n_llll = []
            for ne in n_lll: n_llll.extend(ne.split("\t"))
            new_content = [ne.lower() for ne in n_llll]
            content.extend(new_content)
        wordcount = {}
        for word in content:
            if word != "":
                try: wordcount[word] = wordcount[word] + 1
                except: wordcount[word] = 1
        sorted_w = {}
        cn = 0
        while len(wordcount) > len(sorted_w):
            cn += 1
            for w,c in wordcount.items():
                if c == cn: sorted_w[w] = c
            
        print(sorted_w)
        print("Words","  "*14,"Count")
        for word,count in reversed(sorted_w.items()):
            print(word,"  "*(20-(len(word))),count)
    elif choice == "c":
        charcount = {}
        for line in file:
            line = line.strip()
            for char in line:
                try: charcount[char] = charcount[char] + 1
                except: charcount[char] = 1
        print("Characters","  "*10,"Count")
        for char,count in charcount.items():
            print(char,"  "*(19),count)
    else:
        answered = False
        print("\nIncorrect Input. Try again\n")
    
