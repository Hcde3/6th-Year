import math
def circle_area(d):
    r = d/2
    return f"Area of circle with diameter {d}m is {round(math.pi*(r**2),2)}m2"

def circle_per(d):
    r = d/2
    return f"Perimeter of circle with diameter {d}m is {round(math.pi*r*2,2)}m"

def rect_area(w,h):
    return f"Area of rectangle is {w*h}m2"

def rect_per(w,h):
    return f"Perimeter of rectangle is {(h*2)+(w*2)}m"
