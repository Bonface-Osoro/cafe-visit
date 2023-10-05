import configparser
import os
import warnings
import pandas as pd
from cafevisit.preprocessing import ProcessCountry, ProcessRegions, ProcessPopulation
from cafevisit.geodcoder import geocoding
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


path = os.path.join(DATA_RAW, 'countries.csv')
pop_tif_loc = os.path.join(DATA_RAW, 'WorldPop', 'ppp_2020_1km_Aggregated.tif')

countries = pd.read_csv(path, encoding = 'latin-1')

for idx, country in countries.iterrows():
        
    if not country['iso3'] == 'RWA':
        
        continue 

    country = ProcessCountry(path, countries['iso3'].loc[idx])
    country.process_country_shapes()

    regions = ProcessRegions(countries['iso3'].loc[idx], countries['lowest'].loc[idx])
    regions.process_regions()
    regions.process_sub_region_boundaries()

    populations = ProcessPopulation(path, countries['iso3'].loc[idx], countries['lowest'].loc[idx], pop_tif_loc)
    populations.process_national_population()
    populations.process_population_tif()

    #geocoding(countries['iso3'].loc[idx])