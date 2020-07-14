#!/usr/bin/env python
# coding: utf-8

# In[1]:


#data comes from the Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/categories/30154) 
#and the Utah Open Data Catalog (https://opendata.utah.gov/Social-Services/Average-Price-3-Bedroom-Homes-By-County-In-Utah-19/5icz-nmjb)

#import necessary packages
import pandas as pd
import numpy as np
import glob


# In[2]:


#read in housing data
housing = pd.read_csv("10-year_Change_in_Average_3_Bedroom_Home_Prices_in_Utah_Counties.csv")

#transpose house cost table (counties as columns)
housing = housing.transpose()


# In[3]:


#reset the index, name the columns based on the cities, drop irrelevant info
housing = housing.reset_index()
housing.columns = housing.iloc[0]
housing = housing.drop([0, 230])


# In[4]:


#convert Month column to datetime
housing["Month"] = pd.to_datetime(housing["Month"], format = "%Y-%m")


# In[5]:


#append "_houseprice" to each column name
housing.columns = [str(col) + '_houseprice' for col in housing.columns]
housing.rename(columns={'Month_houseprice':'Month', "Salt Lake_houseprice":"SaltLake_houseprice"}, inplace=True)


# In[6]:


#set the "Month" column as the index of the housing df
housing.set_index("Month", inplace = True)


# In[7]:


#create separate dfs for each county
Davis_housing = pd.DataFrame(housing["Davis_houseprice"]).rename({"Davis_houseprice":"houseprice"}, axis = 1)
SaltLake_housing = pd.DataFrame(housing["SaltLake_houseprice"]).rename({"SaltLake_houseprice":"houseprice"}, axis = 1)
Tooele_housing = pd.DataFrame(housing["Tooele_houseprice"]).rename({"Tooele_houseprice":"houseprice"}, axis = 1)
Utah_housing = pd.DataFrame(housing["Utah_houseprice"]).rename({"Utah_houseprice":"houseprice"}, axis = 1)
Wasatch_housing = pd.DataFrame(housing["Wasatch_houseprice"]).rename({"Wasatch_houseprice":"houseprice"}, axis = 1)
Washington_housing = pd.DataFrame(housing["Washington_houseprice"]).rename({"Washington_houseprice":"houseprice"}, axis = 1)
Weber_housing = pd.DataFrame(housing["Weber_houseprice"]).rename({"Weber_houseprice":"houseprice"}, axis = 1)


# In[8]:


#use glob to get list of all MHI CSVs
MHI_list = glob.glob("*MHI.csv")


# In[9]:


#read in MHI data
DavisMHI = pd.read_csv('DavisCountyMHI.csv', names = ["Month", "MHI"], header = 0)
SaltLakeMHI = pd.read_csv('SaltLakeCountyMHI.csv', names = ["Month", "MHI"], header = 0)
TooeleMHI = pd.read_csv('TooeleCountyMHI.csv', names = ["Month", "MHI"], header = 0)
UtahMHI = pd.read_csv('UtahCountyMHI.csv', names = ["Month", "MHI"], header = 0)
WasatchMHI = pd.read_csv('WasatchCountyMHI.csv', names = ["Month", "MHI"], header = 0)
WashingtonMHI = pd.read_csv('WashingtonCountyMHI.csv', names = ["Month", "MHI"], header = 0)
WeberMHI = pd.read_csv('WeberCountyMHI.csv', names = ["Month", "MHI"], header = 0)


# In[10]:


#create a list of the MHI and housing dfs
MHI_dfs = [DavisMHI, SaltLakeMHI, TooeleMHI, UtahMHI, WasatchMHI, WashingtonMHI, WeberMHI]
housing_dfs = [Davis_housing, SaltLake_housing, Tooele_housing, Utah_housing, Wasatch_housing, Washington_housing, Weber_housing]


# In[11]:


#Convert Month col to datetime, set that col as index, and replace "." with NaN
for df in MHI_dfs:
    df["Month"] = pd.to_datetime(df["Month"])
    df.set_index("Month", inplace = True)
    df.replace(".", np.nan, inplace = True)


# In[12]:


#convert MHI col to numeric
for df in MHI_dfs:
    df.iloc[:,0] = pd.to_numeric(df.iloc[:,0], errors = 'coerce')


# In[13]:


#resample to monthly using month start offset rule ("MS")
DavisMHI = DavisMHI.resample("MS").asfreq()
SaltLakeMHI = SaltLakeMHI.resample("MS").asfreq()
TooeleMHI = TooeleMHI.resample("MS").asfreq()
UtahMHI = UtahMHI.resample("MS").asfreq()
WasatchMHI = WasatchMHI.resample("MS").asfreq()
WashingtonMHI = WashingtonMHI.resample("MS").asfreq()
WeberMHI = WeberMHI.resample("MS").asfreq()


# In[14]:


#intepolate county-level MHI data to get monthly MHI estimates. make sure columns have appropriate names
DavisMHI.interpolate(inplace = True)
SaltLakeMHI.interpolate(inplace = True)
TooeleMHI.interpolate(inplace = True)
UtahMHI.interpolate(inplace = True)
WasatchMHI.interpolate(inplace = True)
WashingtonMHI.interpolate(inplace = True)
WeberMHI.interpolate(inplace = True)


# In[15]:


#to make the data tidy, create a column "county" for each df, and populate it with the county
DavisMHI["county"] = "Davis"
SaltLakeMHI["county"] = "Salt Lake"
TooeleMHI["county"] = "Tooele"
UtahMHI["county"] = "Utah"
WasatchMHI["county"] = "Wasatch"
WashingtonMHI["county"] = "Washington"
WeberMHI["county"] = "Weber"


# In[16]:


#outer merge the housing and MHI csv on dt index
Davis_merge = DavisMHI.merge(Davis_housing, how = "inner", left_index = True, right_index = True)
SaltLake_merge = SaltLakeMHI.merge(SaltLake_housing, how = "inner", left_index = True, right_index = True)
Tooele_merge = TooeleMHI.merge(Tooele_housing, how = "inner", left_index = True, right_index = True)
Utah_merge = UtahMHI.merge(Utah_housing, how = "inner", left_index = True, right_index = True)
Wasatch_merge = WasatchMHI.merge(Wasatch_housing, how = "inner", left_index = True, right_index = True)
Washington_merge = WashingtonMHI.merge(Washington_housing, how = "inner", left_index = True, right_index = True)
Weber_merge = WeberMHI.merge(Weber_housing, how = "inner", left_index = True, right_index = True)


# In[17]:


#vertically concatenate all merge dfs
merge_dfs = [Davis_merge, SaltLake_merge, Tooele_merge, Utah_merge, Wasatch_merge, Washington_merge, Weber_merge]
MHI_housing_merge = pd.concat(merge_dfs, axis = 0)
MHI_housing_merge = MHI_housing_merge[["county", "houseprice", "MHI"]]


# In[18]:


MHI_housing_merge['housing_MHI_ratio'] = MHI_housing_merge['houseprice'] / MHI_housing_merge['MHI']


# In[19]:


#export full merged df to csv for further analysis in R
MHI_housing_merge.to_csv("housing_MHI_merge.csv")


# In[20]:


MHI_housing_merge


# In[21]:


#make an attempt to pivot or melt the df so that column headers are stored in the column "metric"
MHI_housing_melt = pd.melt(MHI_housing_merge.reset_index(), value_vars = ["houseprice", "MHI", "housing_MHI_ratio"], id_vars = ["Month", "county"]).set_index("Month")
MHI_housing_melt


# In[22]:


MHI_housing_melt.to_csv("housing_MHI_melt.csv")


# In[ ]:




