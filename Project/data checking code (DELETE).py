import pandas as pd #when calling pandas can use pd
df = pd.read_csv('exoplanet dataset.csv') #df = dataframe, encoding= tells the computer what format the file is in

#print(df.columns) prints the names of every column in a list
 
df.columns = df.columns.str.upper() #converts all data to strings and all upper case for simplicity, no mixtures (.lower() can be used too
 
# df = df.rename(columns={'oldname1': 'newname1' , 'oldname2': 'newname2'}) how to set new names per column
df = df.rename(columns={"DURATION": "TIME"})
 
pd.set_option('display.max_columns', None)
print(df.isnull()) #isnull() will return a table showing true or false value for each point, True means value is missing
 
print(df.isnull().any()) # shows what columns have missing values (true still meaning a value is missing)
 
print(df.isnull().sum()) # shows how many missing values in each column
 
 
print(df.isnull().sum().sum()) # shows how many missing values in the entire dataframe
 
#df = df.fillna(0) # replaces all missing values with 0
 
#new_values = {"TIME": 100, "FACENUMBER_IN_POSTER": -999} 
#df=df.fillna(value=new_values) #adds new values to existing non existing values
 
mean_of_time = df["TIME"].mean() #gets the mean average of values                - Can also get .median(), .std() [standard deviation], .min() [minimum], .max() [max], .mode()
df["TIME"]=df.TIME.fillna(mean_of_time) #Replace all NaN values in the TIME column with the mean average
 
 
df.dropna(inplace=True) #both do the same thing, drop all rows that have missing values
#df = df.dropna()       #the latter creates a new dataframe, former makes the changes in place