import matplotlib.pyplot as plot
import numpy as np
import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def orderplanets(lst,element):
    try:element_list = [float(x[element]) for x in lst]
    except:return False
    ordered_list = sorted(element_list)
    return ordered_list

#___ Initialising Firebase ___#
cred = credentials.Certificate("exoplanet-dataset-firebase-adminsdk-shser-369d5308fe.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://exoplanet-dataset-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference('/')
firebase_content = ref.get('/users/Planet Info', None)

#___ Making Lists and Dictionaries ___#
planetdict = firebase_content[0]["Planet Info"]
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


#___ Organising Data ___#       
for planet,data in planetdict.items():
    sy_pnum = int(data["sy_pnum"])
    E_mass = data["pl_bmasse"]
    E_radius = data["pl_rade"]
    if data.get("pl_orbper"): orbital_period = data["pl_orbper"]
    else: orbital_period = False
    if E_mass < 2 and E_radius < 2.5: earthlike["Planets"][planet] = data
    elif E_mass < 10 and E_radius < 4: superearth["Planets"][planet] = data
    elif E_mass < 17 and E_radius < 8:megaearth["Planets"][planet] = data
    else:
        if orbital_period:
            if orbital_period < 10: hotjupiter["Planets"][planet] = data
        if not hotjupiter["Planets"].get(planet):
            if E_mass < 125: neptunelike["Planets"][planet] = data
            elif E_mass > 125 and data["pl_bmassj"] < 75:jupiterlike["Planets"][planet] = data
            else: browndwarf["Planets"][planet] = data
                    
#___ Tallying up Telescope Discoveries ___#
    telescope = data["disc_telescope"]
    if telescopecounts.get(telescope): telescopecounts[telescope] = telescopecounts[telescope] + 1
    else: telescopecounts[telescope] = 1

#___ Analysing and Finding Averages ___#
for i,category in enumerate(planet_categories):
    planets = planet_categories[category]["Planets"]
    averages = planet_categories[category]["Averages"]
    for planet,data in planets.items():
        for element,value in data.items():
            if element in numerical_type:
                if value:
                    if averages.get(element):
                        averages[element] = (value+averages[element][0],averages[element][1]+1)
                    else:
                        averages[element] = (value,1)
            if element == "pl_bmasse":list_of_masses[i].append(math.log10(value))
#___ Checking for Habitability ___# assumptions made: Temperature to support water 0-100C and using 60C as an upper limit for temp, Star must live long enough to allow life to form (star mass < 1.5 suns) and must be big enough to allow a viable distance between star and planet (star mass > 0.6 suns a.k.a not a Red Dwarf)            
            if element == "pl_eqt" and value:
                if value > 0+273.15 and value < 60+273.15:
                    try:
                        star_mass = data["st_mass"]
                        if star_mass <= 1.5 and star_mass >= 0.6:
                            habitablecount[category] = habitablecount[category] + 1
                    except:pass
    
    #______ Printing Averages ______#
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

#___ Transferring Data to FireBase ___#
ref = db.reference('/Analytics')
ref.set(Analytics)