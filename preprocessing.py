#all combined data processing

import geopandas as gpd
import pandas as pd
import numpy as np
import re

#-----------------------------------------------------------------------------#

def dataprocess():

    df = pd.read_csv("data/education_province.csv", sep=';')
    df.columns = df.columns.map(lambda x: re.sub("\s+\(PV\)\s*", "", x))
    df = df.loc[[3,4,5,6,7,8,10,11,17,18], ~df.columns.isin(['Nederland', 'Niet in te delen'])]
    df.set_index("Regio's", inplace=True)
    df.index.name = "Education level"
    df.rename({"Vmbo theoretische-gemengde leerweg 3-4": "Vmbo TL 3-4",
               "Vmbo basis-kaderberoeps 3-4": "Vmbo basis-kader 3-4",
               "Hoger beroepsonderwijs": "Hbo",
               "Wetenschappelijk onderwijs": "Wo"
              }, axis=0, inplace=True)
    df.columns.name = "Province"
    for col in df.columns:
        df[col] = df[col].astype('int')
    
    return df

#-----------------------------------------------------------------------------#

def dataprocess_jw():
    
    ### Importing data.
    ## CSV import via pandas.
    df_jw = pd.read_csv('data/cbs_data.csv', sep=';')
    
    ## Re-name variables.
    df_jw.columns = ['ID', 'Sex', "Age", "Education type", "Migration background", "Region", "Year", "Frequency"]
    ## Re-name variable categories.
    # Sex.
    df_jw["Sex"] = df_jw["Sex"].replace({3000: 'Male', 4000: 'Female'})
    # Education type.
    df_jw["Education type"] = df_jw["Education type"].replace({"T001345": 'Secondary education', 
                                                               "A041687": 'Secondary vocational education',
                                                               "A025294": 'Higher vocational education',
                                                               "A025297": 'Academic education'})
    # Migration backgroud.
    df_jw["Migration background"] = df_jw["Migration background"].replace({1012600: 'Dutch',
                                                                           2012655: "Non-dutch western",
                                                                           2012657: "Non-dutch non-western",
                                                                           2012605: 'Non-dutch'})
    # Year.
    df_jw["Year"] = df_jw["Year"].replace({"2005SJ00": '2005/\'06', "2006SJ00": '2006/\'07', "2007SJ00": '2007/\'08',
                                           "2008SJ00": '2008/\'09', "2009SJ00": '2009/\'10', "2010SJ00": '2010/\'11',
                                           "2011SJ00": '2011/\'12', "2012SJ00": '2012/\'13', "2013SJ00": '2013/\'14',
                                           "2014SJ00": '2014/\'15', "2015SJ00": '2015/\'16', "2016SJ00": '2016/\'17',
                                           "2017SJ00": '2017/\'18', "2018SJ00": '2018/\'19', "2019SJ00": '2019/\'20'})
    ## Drop redundant columns.
    columns = ['Age', 'Region']
    df_jw = df_jw.drop(columns, axis = 1)
    ## Remove invalid values in "Frequency" variable. 
    df_jw = df_jw[df_jw.Frequency != '       .']
    ## Convert "Frequency' variable to numeric.
    df_jw["Frequency"] = df_jw['Frequency'].astype(str).astype(int)
    ## Calculate within-group proportions grouped by "Sex" and "Migration background" respectively.
    df_jw["Proportion"] = df_jw.Frequency / df_jw.groupby(["Sex", "Year"])["Frequency"].transform("sum")
    df_jw["Proportion "] = df_jw.Frequency / df_jw.groupby(["Migration background", "Year"])["Frequency"].transform("sum")
    ## Print the resulting dataframe.
    
    return df_jw

#-----------------------------------------------------------------------------#

def dataprocess_gdf_prov():
    
    df_e = pd.read_csv("data/edu_category.csv",sep=';')
    
    #dropping "Nederland" and "Niet in te delen" columns
    df_e = df_e.drop(columns=['The Netherlands', 'Cannot be classified (PV)'])
    
    #removing needless education level classifiers
    df_e = df_e.drop([0,1,8,11,12,13,14,15])
    
    #renaming provinces column to match the geodataframe naming (not very elegant)
    renaming_dict = {'Groningen (PV)': 'Groningen', 'Fryslân (PV)': 'Friesland',
                     'Drenthe (PV)': 'Drenthe','Overijssel (PV)': 'Overijssel',
                     'Flevoland (PV)': 'Flevoland','Gelderland (PV)': 'Gelderland',
                     'Utrecht (PV)': 'Utrecht','North Holland (PV)': 'Noord-Holland',
                     'South Holland (PV)': 'Zuid-Holland','Zeeland (PV)': 'Zeeland',
                     'North Brabant (PV)': 'Noord-Brabant','Limburg (PV)': 'Limburg'}
    
    df_e.rename(columns=renaming_dict, inplace=True)
    
    #reforming the index column
    df_e.rename(columns = {'Regions':'Education level'}, inplace = True)
    df_e = df_e.set_index('Education level')
    
    #transposing the dataframe to make it compatible with the geodataframe
    df_e = df_e.T
    
    #removing Vavo because it contributes with negligible percentage per province
    #(later addition - only realized this after cleaning data)
    df_e = df_e.drop(columns=['Vavo'])
    
    #reseting the indexation for merging
    df_e.reset_index(level=0, inplace=True)
    df_e.rename(columns = {'index':'Province'}, inplace = True)
    
    #adding a column with the total number of students in the province
    df_e["Student total"] = df_e.sum(axis=1)
    
    pd.set_option('precision', 10)
    
    #conversion to percentages
    for column in df_e.columns[1:]:
        temp = (df_e[column]/df_e["Student total"])*100
        df_e[column] = temp
        #print(temp)
    
    #remove the total percentual column
    df_e = df_e.drop(columns=['Student total'])
    
    #path of the geodata
    geo_path = "data/provinciegrenzen/Provinciegrenzen_2019.shp"
    
    #geodataframe merging
    gdf_prov = gpd.read_file(geo_path)
    gdf_prov = pd.merge(gdf_prov,df_e,left_on='Provincien',right_on='Province',how='left')
    
    return gdf_prov

#-----------------------------------------------------------------------------#

def process_population():
    #Dutch population file. 
    #Is the reachest region also the one with the high educational students?
    pop_data =pd.read_csv("data/dutch_population.csv", sep = "\t")
    
    #For the income I want to have the averge household income of the province
    inc_data = pop_data.groupby(by = pop_data["province"], as_index = False).mean()
    inc_data = inc_data[["province", "avg_household_income_2012"]]
    inc_data.columns = ["province", "income"]
    
    #Let's make a discrete distrubution of the income to make more clear the outcome of the map. 
    inc_data["income_dis"] = np.digitize(inc_data["income"], bins = [31500, 33000, 34500, 36000, 37500, 39000])
    
    #Add at the original dataframe the colum with the descrete income value
    inc_data["income_dis"] = inc_data["income_dis"].replace({0: ".       < 31.5K", \
                                                             1: "..      31.5 - 33.0K",\
                                                             2: "...     33.0K - 34.5K",\
                                                             3: "....    34.5K - 36.0K",\
                                                             4: ".....   36.0K - 37.5K",\
                                                             5: "......  37.5 - 39.0K",\
                                                             6: "....... > 39K"})
    
        
    #For the population I want to have the total number of citizen in each province by summing the population of each municipality
    den_data = pop_data.groupby(by = pop_data["province"], as_index = False).sum()
    den_data = den_data[["province", "population", "surface_km2"]]
    den_data["population_density"] = round(den_data["population"] / den_data["surface_km2"], 2 )
    
    den_data["population_density_dis"] = np.digitize(den_data["population_density"], bins = [150, 300, 450, 600, 750, 1000])
    
    #Add at the original dataframe the colum with the descrete income value
    den_data["population_density_dis"] = den_data["population_density_dis"].replace({0: ".       <150",\
                                                                             1: "..      150 - 300",\
                                                                             2: "...     300 - 450",\
                                                                             3: "....    450 - 600",\
                                                                             4: ".....   600 - 750",\
                                                                             5: "......  750 - 1000",\
                                                                             6: "....... >1000"})
    
    #GEOMAP data
    shapefile = "data/provinciegrenzen/Provinciegrenzen_2019.shp"
    #Read shapefile using Geopandas
    geo_data = gpd.read_file(shapefile)[["Provincien", "geometry"]]
    #Rename columns.
    geo_data.columns = ['province', 'geometry']
    geo_data['province']=geo_data['province'].replace({'Fryslân': 'Friesland'})
    
    
    #MERGE the two data sets to plot the income and population in the map 
    
    plot_data = den_data.merge(inc_data)
    merged_data = geo_data.merge(plot_data)
    
    return merged_data