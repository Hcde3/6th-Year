f = open("Exercise.csv","r")
header = f.readline()
Lines = []

def top20(L,I):
    tp20 = []
    for im in L:
        if im[0] == I: tp20.append(im[3])
    tp20.sort()
    return [sum(tp20[:20])/20,sum(tp20[-20:])/20,sum(tp20)/len(tp20)]

print(f"Duration  Pulse\t MaxPulse Calories\t")
for line in f:
    line = line.strip()
    line = line.split(",")
    if not "" in line:
        line = list(map(float,line))
        Lines.append(line)
        print(f"  {line[0]}\t  {line[1]}\t  {line[2]}\t  {line[3]}\t")

avrgs30 = top20(Lines,30)
print(f"\nAnalytics of 30min Sessions:\nAverage of Top 20: {avrgs30[1]} kcal\nAverage of Bottom 20: {avrgs30[0]} kcal\nOverall Average: {avrgs30[2]} kcal")
avrgs45 = top20(Lines,45)
print(f"\nAnalytics of 45min Sessions:\nAverage of Top 20: {avrgs45[1]} kcal\nAverage of Bottom 20: {avrgs45[0]} kcal\nOverall Average: {avrgs45[2]} kcal")
avrgs60 = top20(Lines,60)
print(f"\nAnalytics of 60min Sessions:\nAverage of Top 20: {avrgs60[1]} kcal\nAverage of Bottom 20: {avrgs60[0]} kcal\nOverall Average: {avrgs60[2]} kcal")
avrgs75 = top20(Lines,75)
print(f"\nAnalytics of 75min Sessions:\nAverage of Top 20: {avrgs75[1]} kcal\nAverage of Bottom 20: {avrgs75[0]} kcal\nOverall Average: {avrgs75[2]} kcal")
avrgs120 = top20(Lines,120)
print(f"\nAnalytics of 120min Sessions:\nAverage of Top 20: {avrgs120[1]} kcal\nAverage of Bottom 20: {avrgs120[0]} kcal\nOverall Average: {avrgs120[2]} kcal")
avrgs180 = top20(Lines,180)
print(f"\nAnalytics of 180min Sessions:\nAverage of Top 20: {avrgs180[1]} kcal\nAverage of Bottom 20: {avrgs180[0]} kcal\nOverall Average: {avrgs180[2]} kcal")
user_duration = int(input("\nInput Duration of Session (mins):   "))
user_calories = int(input("Input Calories Burned (kcal):   "))
print("\nAnalytics of Same Duration:")
if user_duration == 30: print(f"Difference from Top 20 Average: {abs(avrgs30[1]-user_calories)}\nDifference from Bottom 20 Average: {abs(avrgs30[0]-user_calories)}")
if user_duration == 45: print(f"Difference from Top 20 Average: {abs(avrgs45[1]-user_calories)}\nDifference from Bottom 20 Average: {abs(avrgs45[0]-user_calories)}")
if user_duration == 60: print(f"Difference from Top 20 Average: {abs(avrgs60[1]-user_calories)}\nDifference from Bottom 20 Average: {abs(avrgs60[0]-user_calories)}")
if user_duration == 75: print(f"Difference from Top 20 Average: {abs(avrgs75[1]-user_calories)}\nDifference from Bottom 20 Average: {abs(avrgs75[0]-user_calories)}")
if user_duration == 120: print(f"Difference from Top 20 Average: {abs(avrgs120[1]-user_calories)}\nDifference from Bottom 20 Average: {abs(avrgs120[0]-user_calories)}")
if user_duration == 180: print(f"Difference from Top 20 Average: {abs(avrgs180[1]-user_calories)}\nDifference from Bottom 20 Average: {abs(avrgs180[0]-user_calories)}")