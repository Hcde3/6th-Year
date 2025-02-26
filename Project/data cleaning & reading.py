import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("exoplanet-dataset-firebase-adminsdk-shser-d21487840a.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://exoplanet-dataset-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference('/')

def dataclean(value): #removes $,#,[,],/ or . from string and converts floats to scientific notion
    try:
        float(value)
        cleaned = scientific_notation(value,"scientific")
    except:
        cleaned = ""
        for char in value:
            if char in ["$","#","[","]","/"]:
                pass
            elif char == ".":
                cleaned = cleaned + "*"
            else: cleaned = cleaned + char
    return cleaned

def typecheck(d,i):
    valid = True
    if columns[i] in string_type:
        try:
            float(d)
            valid = False
        except: pass
    elif columns[i] in numerical_type:
        try:float(d)
        except:valid = False
    if not d: valid = False
    return valid

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

def SphereAverageDensity(rad,mass):
    volume = math.pi*(4/3)*(rad**3)
    density = mass/volume
    return density

with open("exoplanet dataset.csv","r") as dataset:

    firstline = dataset.readline()
    firstline = firstline.strip()
    columns = firstline.split(",")

    numerical_type = ["sy_snum","sy_pnum","pl_orbsmax","pl_orbper","pl_rade","pl_radj","pl_bmasse","pl_bmassj","pl_dens","pl_orbeccen","pl_insol","pl_eqt","pl_orbincl","ttv_flag","pl_imppar","pl_orblper","st_teff","st_mass","st_lum","st_logg","ra","dec","sy_dist","sy_vmag","sy_kmag","sy_gaiamag","sy_gaiamagerr1","sy_gaiamagerr2"]
    string_type = ["pl_name","hostname","disc_facility","disc_telescope","st_spectype","rastr","decstr","pl_bmassprov"]
    to_be_cleaned = {}
    pl_clean = {}
    stars = {}
    
    for line in dataset:
        
        #___ Data gathering ___#
        line = line.strip()
        planet_data_list = line.split(",")
        pl_dict = {}
        st_dict = {}
        valid = True
        
        for index,data in enumerate(planet_data_list):
            
            #___ Cleaning and fixing ___#
            if not typecheck(data,index): valid = False
            data = dataclean(data)
            
            #___ Assigning data to columns ___#
            if index > 0:pl_dict[columns[index]] = data
            else:pl_name = data
           
        #___ Pure info being stored and impure being noted ___#        
        if valid:
            pl_clean[pl_name] = pl_dict
            
            #___ Star Dict ___#
            c_star = pl_dict["hostname"]
            if not stars.get(c_star): stars[c_star] = {}     
            stars[c_star][pl_name] = pl_dict
        else:
            to_be_cleaned[pl_name] = pl_dict

#___ Finding Missing Values ___#
missingvaluecounts = {}
essentialcolumns = ["pl_bmasse","pl_dens","pl_bmassj","pl_rade","pl_radj","st_mass","sy_dist"]
for impurity_pl, impure_set in to_be_cleaned.items():
    useable = True
    for column in columns[1:]:
        
        #__ Calculating missing densities__#
        if not impure_set["pl_dens"] and (impure_set["pl_bmasse"] and impure_set["pl_rade"]):
            radius_in_cm = scientific_notation(impure_set["pl_rade"],"float")*100*6*10**6
            mass_in_g = scientific_notation(impure_set["pl_bmasse"],"float")*1000*6*10**24
            calculated_density = SphereAverageDensity(radius_in_cm,mass_in_g)
            impure_set["pl_dens"] = scientific_notation(calculated_density,"scientific")    
        
        #__ Measuring missing data __#
        if not impure_set[column]:
            if missingvaluecounts.get(column): missingvaluecounts[column] = missingvaluecounts[column]+1
            else: missingvaluecounts[column] = 1
            if column in essentialcolumns: useable = False
            else: pass
            
    if useable:
        pl_clean[impurity_pl] = impure_set
        c_star = impure_set["hostname"]
        if not stars.get(c_star): stars[c_star] = {}      
        stars[c_star][impurity_pl] = impure_set
        
[print(f"Column {i} is missing {k} values.") for i,k in missingvaluecounts.items()]
#___ Adding to firebase ___#
Celestial_info = {"Star Info": stars, "Planet Info": pl_clean}
ref.set(Celestial_info)


