savefile = open("Passwords.csv","r")
Users = {}
for line in savefile:
    data = (line.strip()).split(",")
    Users[data[0]] = data[1]
savefile.close()

def passcheck(password):
    valid_length = len(password) >= 8
    up_present = False
    for char in password:
        if char == char.upper():
            try: int(char)
            except: up_present = True
    low_present = False
    for char in password:
        if char == char.lower():
            try: int(char)
            except: low_present = True
    digit_present = False
    for char in password:
        if char.isdigit(): digit_present = True
    special_present = False
    for char in password:
        if char in ["!","£","$","€","&","*","#"]: special_present = True
    return valid_length and up_present and low_present and digit_present and special_present

program_running = True
while program_running:
    mode = input("1) Create new User ID\n2) Change a password\n3) Display all User IDs\n4) Quit\n")
    if mode == "1":
        entering_userid = True
        while entering_userid:
            USERID = input("\nEnter new User ID:  ")
            try:
                if Users[USERID]: print("User ID must be new. Try Again.")
            except:entering_userid = False
        password_valid = False
        while not password_valid:
            print("\nPassword must include:\n   Atleast 8 characters\n   Upper case letters\n   Lower case letters\n   Numbers\n   One special character (!,£,$,€,&,*,#")
            password = input("Enter a password:  ")
            password_valid = passcheck(password)
            if not password_valid: print("Password does not satisfy criteria. Try Again.")
        Users[USERID] = password
    elif mode == "2":
        user_chosen = False
        while not user_chosen:
            USERID = input("\nEnter existing User ID:  ")
            print(Users)
            if Users.get(USERID): user_chosen = True
            else: print("User does not exist. Try Again.")
        password_valid = False
        while not password_valid:
            print("\nPassword must include:\n   Atleast 8 characters\n   Upper case letters\n   Lower case letters\n   Numbers\n   One special character (!,£,$,€,&,*,#")
            password = input("Enter a new password:  ")
            password_valid = passcheck(password)
            if not password_valid: print("Password does not satisfy criteria. Try Again.")
        Users[USERID] = password
    elif mode == "3":
        print("\n")
        for userid in Users: print(userid,": ", Users[userid])
        print("\n")
    elif mode == "4":
        savefile = open("Passwords.csv","w")
        for userdata in Users: savefile.write(f"{userdata},{Users[userdata]}\n")
        savefile.close()
        program_running = False
    else:
        print("Invalid Option. Try Again.\n")
            
