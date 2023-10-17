import os
import configparser
import warnings
import pandas as pd
import matplotlib.pyplot as plt 
import geopandas as gpd
from shapely import wkt
from mpl_toolkits.axes_grid1 import make_axes_locatable
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_RESULTS = os.path.join(BASE_PATH, '..', 'results')
DATA_AFRICA = os.path.join(BASE_PATH, '..', 'results', 'SSA')
DATA_VIS = os.path.join(BASE_PATH, '..', 'vis')
path = os.path.join(DATA_RAW, 'countries.csv')


def pop_density(iso3):
    """
    This function plots the population 
    distribution of a country
    """
    map_path = os.path.join(DATA_RESULTS, 'processed', iso3, 'regions', 'regions_1_{}.shp'.format(iso3))
    path = os.path.join(DATA_RESULTS, 'final', iso3, 'population', '{}_population_results.csv'.format(iso3))

    map_df = gpd.read_file(map_path)
    df = pd.read_csv(path)

    df_merged  = map_df.merge(df, left_on = 'GID_1', right_on = 'GID_1')
    gdf = gpd.GeoDataFrame(df_merged)

    gdf.drop(columns = ['geometry_x'], inplace = True)
    gdf.rename(columns = {'geometry_y': 'geometry'}, inplace = True)
    gdf['geometry'] = gdf['geometry'].apply(wkt.loads)
    gdf.set_geometry(col = 'geometry', inplace = True)

    fig, ax = plt.subplots(1, figsize = (10, 10))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('bottom', size = '5%', pad = 0.3)
    gdf.plot(column = 'population', legend = True,
            cax = cax, ax = ax,
            legend_kwds = {'label': 'Population', 'orientation': 'horizontal'})
    ax.set_title('Population Distribution')

    fig_path = os.path.join(DATA_VIS, 'figures', '{}_population.png'.format(iso3))
    plt.savefig(fig_path, dpi = 720)


    return None


def ssa_pop_density():
    """
    This function plots the population 
    distribution of Sub-Saharan Africa
    """
    map_path = os.path.join(DATA_AFRICA, 'shapefile', 'sub_saharan_africa.shp')
    path = os.path.join(DATA_AFRICA, 'SSA_population_results.csv')

    map_df = gpd.read_file(map_path)
    df = pd.read_csv(path)

    df_merged  = map_df.merge(df, left_on = 'GID_1', right_on = 'GID_1')
    gdf = gpd.GeoDataFrame(df_merged)

    gdf.drop(columns = ['geometry_x'], inplace = True)
    gdf.rename(columns = {'geometry_y': 'geometry'}, inplace = True)
    gdf['geometry'] = gdf['geometry'].apply(wkt.loads)
    gdf.set_geometry(col = 'geometry', inplace = True)

    fig, ax = plt.subplots(1, figsize = (10, 10))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('bottom', size = '5%', pad = 0.3)
    gdf.plot(column = 'population', legend = True,
            cax = cax, ax = ax,
            legend_kwds = {'label': 'Population', 'orientation': 'horizontal'})
    ax.set_title('Population Distribution of Sub-Saharan Africa')

    fig_path = os.path.join(DATA_VIS, 'figures', 'SSA_population.png')
    plt.savefig(fig_path, dpi = 720)


    return None

if __name__ == '__main__':

    countries = pd.read_csv(path, encoding = 'latin-1')
    for idx, country in countries.iterrows():

        #if not country['region'] == 'Sub-Saharan Africa' or country['Exclude'] == 1:   
        if not country['iso3'] == 'MWI':
            
            continue 

        #pop_density(countries['iso3'].loc[idx]) 
    ssa_pop_density()           