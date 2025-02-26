import matplotlib.pyplot as plot
import numpy as np
import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def scientific_notation(num,change_to):
    if change_to == "float":
        inputs = num.split("x10^")
        power = int(inputs[1])
        base = int(inputs[0])
        output = base*10**power
        return output
    elif change_to == "scientific":
        num = float(num)
        integer = str(int(round(num,5)*10**5))
        output = integer+"x10^-5"
        return output

def orderplanets(lst,element):
    try:element_list = [scientific_notation(x[element],"float") for x in lst]
    except:return False
    ordered_list = sorted(element_list)
    return ordered_list
    
cred = credentials.Certificate("exoplanet-dataset-firebase-adminsdk-shser-d21487840a.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://exoplanet-dataset-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference('/')

firebase_content = ref.get('/users', None)
planetdict = firebase_content[0]["Planet Info"]
stardict = firebase_content[0]["Star Info"]
averages_8p = {}
averages_7p = {}
averages_6p = {}
averages_5p = {}
averages_4p = {}
averages_3p = {}
averages_2p = {}
averages_1p = {}
pnum_averages = [averages_1p,averages_2p,averages_3p,averages_4p,averages_5p,averages_6p,averages_7p,averages_8p]
earthlike = {"Planets":{},"Averages":{}}
superearth = {"Planets":{},"Averages":{}}
megaearth = {"Planets":{},"Averages":{}}
neptunelike = {"Planets":{},"Averages":{}}
jupiterlike = {"Planets":{},"Averages":{}}
hotjupiter = {"Planets":{},"Averages":{}}
browndwarf = {"Planets":{},"Averages":{}}
outlier_planets = {"Planets":{},"Averages":{}}
planet_categories = {"Earthlike":earthlike,"Super Earth":superearth,"Mega Earth":megaearth,"Neptunelike":neptunelike,"Jupiterlike":jupiterlike,"Hot Jupiter":hotjupiter,"Brown Dwarf":browndwarf}
numerical_type = ["sy_snum","sy_pnum","pl_orbsmax","pl_orbper","pl_rade","pl_radj","pl_bmasse","pl_bmassj","pl_dens","pl_orbeccen","pl_insol","pl_eqt","pl_orbincl","ttv_flag","pl_imppar","pl_orblper","st_teff","st_mass","st_lum","st_logg","ra","dec","sy_dist","sy_vmag","sy_kmag","sy_gaiamag","sy_gaiamagerr1","sy_gaiamagerr2"]

list_of_radii = []
list_of_masses = [[],[],[],[],[],[],[]]
habitablecount = {"Earthlike":0,"Super Earth":0,"Mega Earth":0}
telescopecounts = {}

#___ Planet Mass Ratio Per System Size ___#
dist_data = [[[0,0,0,0,0,0,0,0],0],[[0,0,0,0,0,0,0],0],[[0,0,0,0,0,0],0],[[0,0,0,0,0],0],[[0,0,0,0],0],[[0,0,0],0],[[0,0],0],[[0],0]]
test_list = [[],[],[],[],[],[],[]]
for star,data in stardict.items():
    planets_ordered_by_dist = []
    for planet,pl_data in data.items():planets_ordered_by_dist.append(pl_data)
    planets_ordered_by_dist = orderplanets(planets_ordered_by_dist,"pl_orbsmax")
    if planets_ordered_by_dist:
        planet_no = len(planets_ordered_by_dist)
        for i,pd in enumerate(planets_ordered_by_dist):
            if i == 0:
                baseorbit = pd
                dist_data[8-planet_no][0][0] = dist_data[8-planet_no][0][0] + 1
            else: dist_data[8-planet_no][0][i] = dist_data[8-planet_no][0][i] + pd/baseorbit
        dist_data[8-planet_no][1] = dist_data[8-planet_no][1] + 1
        
dist_averages = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0],[0,0,0,0],[0,0,0],[0,0],[0]]
for sys_num,content in enumerate(dist_data):
    dists = content[0]
    times = content[1]
    if times:
        for i,total_dis in enumerate(dists):
            average = total_dis/times
            dist_averages[sys_num][i] = average
            
print(dist_averages)
for planet,data in planetdict.items():
    sy_pnum = int(scientific_notation(data["sy_pnum"],"float"))
    planet_num_dict = pnum_averages[sy_pnum - 1]
    for element,value in data.items():
        if element == "pl_bmasse":
            E_mass = scientific_notation(value,"float")
            E_radius = scientific_notation(data["pl_rade"],"float")
            #list_of_radii.append(E_radius)
            #list_of_masses.append(E_mass)
            if data.get("pl_orbper"): orbital_period = scientific_notation(data["pl_orbper"],"float")
            else: orbital_period = False
            if E_mass < 2 and E_radius < 2.5: earthlike["Planets"][planet] = data
            elif E_mass < 10 and E_radius < 4: superearth["Planets"][planet] = data
            elif E_mass < 17 and E_radius < 8:megaearth["Planets"][planet] = data
            else:
                if orbital_period:
                    if orbital_period < 10: hotjupiter["Planets"][planet] = data
                if not hotjupiter["Planets"].get(planet):
                    if E_mass < 125: neptunelike["Planets"][planet] = data
                    elif E_mass > 125 and scientific_notation(data["pl_bmassj"],"float") < 75:jupiterlike["Planets"][planet] = data
                    else: browndwarf["Planets"][planet] = data
        if element in numerical_type:
            if value:
                value = scientific_notation(value,"float")
                if planet_num_dict.get(element):
                    planet_num_dict[element] = (value+planet_num_dict[element][0],planet_num_dict[element][1]+1)
                else:
                    planet_num_dict[element] = (value,1)
                    
        #___ Tallying up Telescope Discoveries __#
        if element == "disc_telescope":
            if telescopecounts.get(value): telescopecounts[value] = telescopecounts[value] + 1
            else: telescopecounts[value] = 1
            
for index, sysize_dict in enumerate(pnum_averages):
    planet_no = index + 1
    print(f"\n\n{planet_no} Planets:")
    for element in sysize_dict:
        total = sysize_dict[element][0]
        values = sysize_dict[element][1]
        sysize_dict[element] = total/values
        if element == "sy_pnum": total_pnum = values
        print(f"-----average {element} is {sysize_dict[element]}")
    print(f"Data gathered from {total_pnum} planets across {int(total_pnum/planet_no)} stars.")


for i,category in enumerate(planet_categories):
    planets = planet_categories[category]["Planets"]
    averages = planet_categories[category]["Averages"]
    for planet,data in planets.items():
        for element,value in data.items():
            if element in numerical_type:
                if value:
                    value = scientific_notation(value,"float")
                    if averages.get(element):
                        averages[element] = (value+averages[element][0],averages[element][1]+1)
                    else:
                        averages[element] = (value,1)
            if element == "pl_bmasse":list_of_masses[i].append(math.log10(value))
            #___ Checking for Habitability ___# assumptions made: Temperature to support water 0-100C and using 60C as an upper limit for temp, Star must live long enough to allow life to form (star mass < 1.5 suns) and must be big enough to allow a viable distance between star and planet (star mass > 0.6 suns a.k.a not a Red Dwarf)            
            if element == "pl_eqt" and value:
                if value > 0+273.15 and value < 60+273.15:
                    try:
                        star_mass = scientific_notation(data["st_mass"],"float")
                        if star_mass <= 1.5 and star_mass >= 0.6:
                            habitablecount[category] = habitablecount[category] + 1
                    except:pass
                    
    print(f"\n\n{category} Planets:")
    for element in averages:
        total = averages[element][0]
        values = averages[element][1]
        averages[element] = total/values
        if element == "sy_pnum": total_pnum = values
        if element == "pl_rade": list_of_radii.append(total/values)
        print(f"-----average {element} is {averages[element]}")
    print(f"Data gathered from {total_pnum} planets.")


#______ Graphs and Charts ______#

Analytics = {"Graph_Info":{},"Averages":{"Earthlike":earthlike["Averages"],"Super Earth":superearth["Averages"],"Mega Earth":megaearth["Averages"],"Neptunelike":neptunelike["Averages"],"Jupiterlike":jupiterlike["Averages"],"Hot Jupiter":hotjupiter["Averages"],"Brown Dwarf":browndwarf["Averages"]}} #Creating Analytics Dict

#___ Pie Chart of Habitable Planets or Total Planets___#
cats = []
counts = []
for category,count in habitablecount.items():
        cats.append(category)
        counts.append(count)
fig, ax = plot.subplots()
ax.pie(counts, labels=cats, autopct='%1.1f%%',colors=['blue', 'green', 'brown'])
plot.title('Most Common Types of Habitable Exoplanet')
Analytics["Graph_Info"]["Habitable Planets"] = {}
Analytics["Graph_Info"]["Habitable Planets"]["Categories"] = cats
Analytics["Graph_Info"]["Habitable Planets"]["Counts"] = counts
plot.show()

cats = ["Earthlikes","Super Earths","Mega Earths","Neptunelikes","Jupiterlikes","Hot Jupiters","Brown Dwarfs"]
counts = [len(earthlike["Planets"]),len(superearth["Planets"]),len(megaearth["Planets"]),len(neptunelike["Planets"]),len(jupiterlike["Planets"]),len(hotjupiter["Planets"]),len(browndwarf["Planets"])]
fig, ax = plot.subplots()
ax.pie(counts, labels=cats, autopct='%1.1f%%',colors=['green', 'yellow', 'grey',"blue","orange","red","brown"])
plot.title('Most Common Types of Exoplanet')
Analytics["Graph_Info"]["All Planets"] = {}
Analytics["Graph_Info"]["All Planets"]["Categories"] = cats
Analytics["Graph_Info"]["All Planets"]["Counts"] = counts
plot.show()


#___ Pie Chart of Telescopes Used___#
tels = []
counts = []
othercount = 0
for telescope,count in telescopecounts.items():
    if count > 50:
        #if "*" in telescope:
            
        tels.append(telescope)
        counts.append(count)
    else:
        othercount += 1
tels.append("Other Telescopes")
counts.append(othercount)
fig, ax = plot.subplots()
ax.pie(counts, labels=tels, autopct='%1.1f%%')
plot.title('Most Common Telescopes Used to Discover Exoplanets (In Database)')
plot.show()
Analytics["Graph_Info"]["Telescopes"] = {}
Analytics["Graph_Info"]["Telescopes"]["Names"] = tels
Analytics["Graph_Info"]["Telescopes"]["Counts"] = counts

#___ Boxplot of Planet's Mass by Category___#
plot.boxplot(list_of_masses)
plot.title('Boxplot of Masses in each Category')
plot.xticks([1, 2, 3,4,5,6,7], ["Earthlike","Super Earth","Mega Earth","Neptunelike","Jupiterlike","Hot Jupiter","Brown Dwarf"])
plot.xlabel('Category')
plot.ylabel('Log of Masses')
plot.show()
Analytics["Graph_Info"]["Masses"] = list_of_masses

#__ Bar Chart of Average Radius per Category __#
parameters = input("Choose which categories to view:\n(1) All Categories\n(2) Terrestrials\n(3) Gas Giants\n")
if parameters == "1":plot.bar(list(planet_categories.keys()),list_of_radii,color=['green', 'yellow', 'grey',"blue","orange","red","brown"])
elif parameters == "2":plot.bar(["Earthlike","Super Earth","Mega Earth"],list_of_radii[:3])
else: plot.bar(["Neptunelike","Jupiterlike","Hot Jupiter","Brown Dwarf"],list_of_radii[3:])
plot.title('Average Earth Radii per Planet Type')
plot.xlabel('Planet Types')
plot.ylabel('Average Earth Radii')
plot.show()
Analytics["Graph_Info"]["Radii"] = list_of_radii

#___ Bar Chart of Orbital Radius compared to First ___#
sys_size = int(input("Choose what size solar system to compare orbits of. (1-7)planets:\n"))
plot.bar([1,2,3,4,5,6,7][:sys_size],dist_averages[8-sys_size])
plot.title('Orbital Distance Compared to First')
plot.xlabel('Orbital Position')
plot.ylabel('Orbital Distance / First Orbit')
plot.show()
Analytics["Graph_Info"]["Orbital Radii"] = dist_averages

#___ Transferring Data to FireBase ___#
ref = db.reference('/Analytics')
ref.set(Analytics)