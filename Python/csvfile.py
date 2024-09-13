f = open("Exercise.csv","r")
header = f.readline()
Lines = []

def top20(L,I):
    tp20 = []
    for im in L:
        if im[0] == I: tp20.append(im[3])
    tp20.sort()
    return [sum(tp20[:20])/20,sum(tp20[-20:])/20,sum(tp20)/len(tp20)]

print(f"Duration    Pulse     MaxPulse  Calories\t")
for line in f:
    line = line.strip()
    line = line.split(",")
    if not "" in line:
        line = list(map(float,line))
        Lines.append(line)
        print(f"  {line[0]}\t  {line[1]}\t  {line[2]}\t  {line[3]}\t")

types = [15,20,25,30,45,60,75,80,90,120,150,160,180,210,270,300]
avrgof4560 = []
otheravrg = []
for session_type in types:
    avrg = top20(Lines,session_type)
    if session_type in [45,60]:
        print(f"\nAnalytics of {session_type}min Sessions:\nAverage of Top 20: {avrg[1]} kcal\nAverage of Bottom 20: {avrg[0]} kcal\nOverall Average: {avrg[2]} kcal")
        avrg.append(session_type)
        avrgof4560.append(avrg)
        otheravrg.append(avrg)
    else:
        print(f"\n{session_type}min Session Average: {avrg[2]} kcal")
        avrg.append(session_type)
        otheravrg.append(avrg)
for fs in avrgof4560:
    for avrgs in otheravrg:
        print(f"\nThere is a {((fs[2]-avrgs[2])/((fs[2]+avrgs[2])/2))*100}% difference between the overall average of {fs[3]}min and {avrgs[3]}min sessions")
        print(f"There is a {((fs[1]-avrgs[1])/((fs[1]+avrgs[1])/2))*100}% difference between the top 20 average of {fs[3]}min and {avrgs[3]}min sessions")
        print(f"There is a {((fs[0]-avrgs[0])/((fs[0]+avrgs[0])/2))*100}% difference between the bottom 20 average of {fs[3]}min and {avrgs[3]}min sessions")

answering = True
print(f"\nSession Types: {types}")
while answering:
    user_duration = int(input("Input Session Type (mins):   "))
    user_calories = int(input("Input Calories Burned (kcal):   "))
    if user_duration in types: answering = False
    else: print("Not a possible session length, try again.")

print(f"\nAnalytics of {user_duration}min Sessions:")
avrg = top20(Lines,user_duration)
print(f"Difference from Top 20 Average: {abs(avrg[1]-user_calories)}\nDifference from Bottom 20 Average: {abs(avrg[0]-user_calories)}")

