import myMathsLibrary
mode = input("1) Area of circle\n2) Perimeter of circle\n3) Area of rectangle\n4) Perimeter of rectangle\n")
if mode == "1": print(myMathsLibrary.circle_area(int(input("Enter a circle diameter:  "))))
if mode == "2": print(myMathsLibrary.circle_per(int(input("Enter a circle diameter:  "))))
if mode == "3": print(myMathsLibrary.rect_area(int(input("Enter a rectangle width:  ")),int(input("Enter a rectangle height:  "))))
if mode == "4": print(myMathsLibrary.rect_per(int(input("Enter a rectangle width:  ")),int(input("Enter a rectangle height:  "))))