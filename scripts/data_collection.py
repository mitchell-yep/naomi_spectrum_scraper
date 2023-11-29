# Importing Python Modules To Help Run the Below Code
import requests
import ssl
from requests.adapters import HTTPAdapter
import json
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from google.colab import files
import itertools

# -----------------------------------------

## Generating API Inputs ##
# ie: https://naomi2023.azurewebsites.net/api/v1/areas?params

# Country codes
countries = ['AGO', 'BDI', 'BEN', 'BFA', 'BWA', 'CAF', 'CMR', 'COD', 'COG', 'CIV',
    'ETH', 'GAB', 'GHA', 'GIN', 'GMB', 'GNB', 'KEN', 'LBR', 'LSO','MWI', 'MLI',
    'MOZ', 'NAM', 'NER', 'RWA', 'SEN', 'SLE', 'SWZ', 'TCD', 'TGO', 'UGA',
    'ZMB', 'ZWE','GNQ','HIT', 'STP', 'TZA', 'ZAF']

names = ['Angola', 'Burundi', 'Benin', 'Burkina Faso', 'Botswana', 'Central African Republic',
'Cameroon', 'Democratic Republic of the Congo', 'Republic of the Congo', "Ivory Coast (Côte d'Ivoire)",
'Ethiopia', 'Gabon', 'Ghana', 'Guinea', 'The Gambia', 'Guinea-Bissau', 'Kenya', 'Liberia', 'Lesotho','Malawi', 'Mali',
'Mozambique', 'Namibia', 'Niger', 'Rwanda', 'Senegal', 'Sierra Leone', 'Eswatini', 'Chad',
'Togo', 'Uganda', 'Zambia', 'Zimbabwe', 'Equatorial Guinea', 'Haiti', 'Sao Tome and Principe', 'Tanzania', 'South Africa']


country_conversion = pd.DataFrame({'country':countries, 'country_name':names})

# Available indicators - Missing all  ANC indicators (No estimates for many countries)
indicator = ['population', 'prevalence', 'plhiv', 'art_coverage',
             'art_current_residents', 'art_current', 'untreated_plhiv_num',
             'aware_plhiv_prop', 'unaware_plhiv_num', 'aware_plhiv_num',
             'plhiv_attend','untreated_plhiv_attend', 'aware_plhiv_attend',
             'unaware_plhiv_attend', 'incidence', 'infections']

# Age Groups
ageGroup = ['Y015_049', 'Y015_064', 'Y015_999', 'Y050_999', 'Y000_999',
            'Y000_064', 'Y000_014', 'Y015_024', 'Y025_034', 'Y035_049',
            'Y050_064', 'Y065_999', 'Y010_019', 'Y025_049', 'Y000_004',
            'Y005_009', 'Y010_014']

# Periods
period = ['2022-4', '2023-3', '2024-3','2025-3']

# Sex
sex = ['both', 'male', 'female']

# Area Level - 3 is the preferred area level
areaLevel = ['0', '1', '2', '3', '4']

countries_param = "&country=".join(countries)

indicator_index = [i for i in range(len(indicator)) if indicator[i] in enter_indicator]
sex_index = [i for i in range(len(sex)) if sex[i] in enter_sex]
age_index = [i for i in range(len(ageGroup)) if ageGroup[i] in enter_age]
period_index = [i for i in range(len(period)) if period[i] in enter_period]

unique_combinations = []

for i in indicator_index:
    for j in age_index:
        for x in period_index:
            for y in sex_index:
                unique_combinations.append((indicator[i], ageGroup[j], period[x], sex[y]))

#print(country_conversion)

# Creating our URL For Areas Endpoint
AREAS_URL = (f'https://naomi2023.azurewebsites.net/api/v1/areas?'
            f'country={countries_param}&'
            f'indicator={unique_combinations[0][0]}&'
            f'ageGroup={unique_combinations[0][1]}&'
            f'period={unique_combinations[0][2]}&'
            f'sex={unique_combinations[0][3]}&'
            f'areaLevel={areaLevel[3]}')

url_list = []
for i in range(len(unique_combinations)):
  unique_url = (f'https://naomi2023.azurewebsites.net/api/v1/areas?'
              f'country={countries_param}&'
              f'indicator={unique_combinations[i][0]}&'
              f'ageGroup={unique_combinations[i][1]}&'
              f'period={unique_combinations[i][2]}&'
              f'sex={unique_combinations[i][3]}&'
              f'areaLevel={areaLevel[3]}')
  url_list.append(unique_url)

# Verifying it looks ok
print("our generated URL")
print(AREAS_URL)
print("vs example link from site")
print("https://naomi2023.azurewebsites.net/api/v1/areas?country=AGO&country=BEN&indicator=art_coverage&ageGroup=Y015_049&period=2022-4&sex=both&areaLevel=1")
print(url_list)

naomi_dfs = []


for z in range(len(url_list)):
  response = requests.get(url_list[z])
  data = response.json()
# If you'd like to see the raw data, uncomment the below line
#print(json.dumps(data))
#Filter our 1st level Area and Sub Areas
  temp = []
  nosub = []
  for string in data:
    if "subareas" in string:
      temp.append(string)
    else: nosub.append(string)
# Bring 1st subarea up a level
  subareas = []

  for i in range(len(temp)):
    for j in range(len(temp[i]['subareas'])):
      subareas.append((temp[i]['subareas'][j]))
#print(len(subareas))
#print(data)
# Parse out 2nd subareas
  psub = []
  parea =[]
  ssubarea = []
  for string in subareas:
    if "subareas" in string:
      psub.append(string)
    else: parea.append(string)
# Bring 2nd sublevel up
  for i in range(len(psub)):
    for j in range(len(psub[i]['subareas'])):
      ssubarea.append((psub[i]['subareas'][j]))
# Parse out 3nd subareas
  dsub = []
  darea =[]
  ddsubarea = []
  for string in ssubarea:
    if "subareas" in string:
      dsub.append(string)
    else: darea.append(string)
# Bring 3rd sublevel up
  for i in range(len(dsub)):
    for j in range(len(dsub[i]['subareas'])):
      ddsubarea.append((dsub[i]['subareas'][j]))

# Joining all the different levels
  countrydf = pd.DataFrame(temp).drop(columns = ['subareas'])
  nosubdf = pd.DataFrame(nosub)
  subdf = pd.DataFrame(subareas).drop(columns = ['subareas'])

  psubdf = pd.DataFrame(parea)
  psub_par_df = pd.DataFrame(ssubarea).drop(columns = ['subareas'])

  tsubdf = pd.DataFrame(darea)
  tsub_par_df = pd.DataFrame(ddsubarea)

# Don't include for level 3, 2, 1.
#May need to include for level 4 and additional levels for higher
#dsub_par_df = pd.DataFrame(dsub).drop(columns = ['subareas'])
  list(countrydf.columns)
  list(nosubdf.columns)
  list(subdf.columns)
  list(psubdf.columns)
  list(psub_par_df.columns)
  list(tsubdf.columns)
  list(tsub_par_df.columns)
#list(dsub_par_df.columns)
# List to store all DataFrames


  all_df= pd.concat([countrydf, nosubdf, subdf, psubdf, psub_par_df,
                     tsubdf, tsub_par_df], ignore_index = True)
  all_df.drop_duplicates(keep = 'first')
#Add geographical region code
  all_df['geo_region'] = all_df['areaLevel']
  all_df['geo_region'] = np.where(all_df['geo_region'] == 0,
                                  'OU',all_df['geo_region'])
  all_df['geo_region'] = np.where(all_df['geo_region'] == '1',
                                  'SNU',all_df['geo_region'])
  all_df['geo_region'] = np.where(all_df['geo_region'] == '2',
                                  'SSNU',all_df['geo_region'])
  all_df['geo_region'] = np.where(all_df['geo_region'] == '3',
                                  'PSNU',all_df['geo_region'])

#Reference table
  geocodes = all_df[['code','parentCode', 'areaLevel','geo_region', 'name']]

  snucodes = geocodes[geocodes.geo_region == 'SNU'].rename(columns ={
      'name':'SNUname',
      'geo_region':'Parent_region',
      'code':'SNUcode'})

  ssnucodes = geocodes[geocodes.geo_region == 'SSNU'].rename(columns ={
      'name':'SSNUname',
       'parentCode':'SNUcode',
      'code':'parentCode'})

  all_df = pd.merge(all_df, ssnucodes[['SNUcode','SSNUname', 'parentCode']],
                    on='parentCode', how = 'left')
  all_df['SSNUcode'] = np.where(all_df['geo_region'] == 'PSNU',
                                all_df['SNUcode'],
                                all_df['parentCode'])


  all_df = pd.merge(all_df, snucodes[['SNUcode','SNUname']], on = 'SNUcode', how = 'left')

  data = {'indicator':{unique_combinations[0][0]},
              'ageGroup':{unique_combinations[0][1]},
              'period':{unique_combinations[0][2]},
              'sex':{unique_combinations[0][3]},
              'areaLevel':{areaLevel[3]}}

  # initializing list of lists
  indicator = [unique_combinations[z][0]]
  agegroup = [unique_combinations[z][1]]
  period = [unique_combinations[z][2]]
  sex = [unique_combinations[z][3]]


  # declaring magnitude of repetition
  K = len(all_df.index)

  # using itertools.chain.from_iterable()
  # + itertools.repeat() repeat elements K times
  indicator_list = list(itertools.chain.from_iterable(itertools.repeat(i, K)
                      for i in indicator))
  agegroup_list = list(itertools.chain.from_iterable(itertools.repeat(i, K)
                      for i in agegroup))
  period_list = list(itertools.chain.from_iterable(itertools.repeat(i, K)
                      for i in period))
  sex_list = list(itertools.chain.from_iterable(itertools.repeat(i, K)
                      for i in sex))

  all_df['indicator'] = indicator_list
  all_df['age_group'] = agegroup_list
  all_df['period'] = period_list
  all_df['sex'] = sex_list
  all_df['country'] = all_df['code'].str.slice(0,3)
  all_df = pd.merge(all_df, country_conversion, on = 'country', how = 'left', validate = 'm:1' )
  naomi_dfs.append(all_df)

df = pd.concat(naomi_dfs)
df.to_csv('all_data.csv', index = False )
files.download('all_data.csv')