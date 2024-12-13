import networkx as nx
import pandas as pd
import geopandas as gpd
import config as cfg
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils import build_trip_count, get_district_names, normalize_by_pop, get_income_data, add_quantiles, get_share_trips

sns.set(font_scale=1.2) 

if cfg.type_of_study == 'month':
    all_viajes = pd.read_csv(cfg.VIAJES_DATA / 'all_viajes_month_0322.csv', thousands='.',decimal=',')  # Subtracting trips in Madrid districts during March 2022
    data_name = 'March 2022'
elif cfg.type_of_study == 'week':
    all_viajes = pd.read_csv(cfg.VIAJES_DATA / 'viajes_week_0322.csv', thousands='.',decimal=',')  # Subtracting trips in Madrid districts during a 'normal' week
    data_name = 'Normal Week'
elif cfg.type_of_study == 'two_weeks':
    all_viajes = pd.read_csv(cfg.VIAJES_DATA / 'viajes_two_weeks_0322.csv', thousands='.',decimal=',')  # Subtracting trips in Madrid districts during 2 weeks
    data_name = 'Two Weeks'
elif cfg.type_of_study == 'weekend':
    all_viajes = pd.read_csv(cfg.VIAJES_DATA / 'viajes_weekend_0322.csv', thousands='.',decimal=',')  # Subtracting trips in Madrid districts during 2 weeks
    data_name = 'Weekend'
else:
    raise ValueError('No time of study has been set')

income = gpd.read_file(cfg.ROOT_PATH / 'segregation_indices/data/processed/geometries_and_income.geojson') # income data

filtered_df = all_viajes.loc[(all_viajes['actividad_origen'] == 'casa')] # home origin trips

district_counts = filtered_df.groupby('origen')['viajes'].sum().reset_index(name='total_viajes') # FIXED
district_counts.columns = ['ID', 'Population']

trip_counts = build_trip_count(filtered_df)
trip_counts = get_district_names(trip_counts)
trip_counts = normalize_by_pop(trip_counts, district_counts)
if cfg.SAVE_DFS:
    trip_counts.to_csv(f'outputs/{cfg.type_of_study}_normalized_trip_count.csv', index=False) # saving trip counts

trip_counts = get_income_data(trip_counts, income, 'Gini Index', 'Median income per consumption unit')
trip_counts = add_quantiles(trip_counts, 'Median income per consumption unit', n_quantiles=4)
trip_counts = add_quantiles(trip_counts, 'Gini Index', n_quantiles=4)

low_to_high_median = trip_counts[(trip_counts['income decile origin Median income per consumption unit'].isin([0])) & 
                                      (trip_counts['income decile destination Median income per consumption unit'].isin([3]))]

high_to_low_median = trip_counts[(trip_counts['income decile origin Median income per consumption unit'].isin([3])) & 
                                      (trip_counts['income decile destination Median income per consumption unit'].isin([0]))]

low_to_low_median = trip_counts[(trip_counts['income decile origin Median income per consumption unit'].isin([0])) &
                                (trip_counts['income decile destination Median income per consumption unit'].isin([0]))]

high_to_high_median = trip_counts[(trip_counts['income decile origin Median income per consumption unit'].isin([3])) & 
                                trip_counts['income decile destination Median income per consumption unit'].isin([3])]

low_to_high_gini = trip_counts[(trip_counts['income decile origin Gini Index'].isin([0])) & 
                                      (trip_counts['income decile destination Gini Index'].isin([3]))]

high_to_low_gini = trip_counts[(trip_counts['income decile origin Gini Index'].isin([3])) & 
                                      (trip_counts['income decile destination Gini Index'].isin([0]))]

low_to_low_gini = trip_counts[(trip_counts['income decile origin Gini Index'].isin([0])) &
                              (trip_counts['income decile destination Gini Index'].isin([0]))]


high_to_high_gini = trip_counts[(trip_counts['income decile origin Gini Index'].isin([3])) & 
                                (trip_counts['income decile destination Gini Index'].isin([3]))]

h_l = get_share_trips(trip_counts, low_to_high_median)
l_h = get_share_trips(trip_counts, high_to_low_median)
l_l = get_share_trips(trip_counts, low_to_low_median)
h_h = get_share_trips(trip_counts, high_to_high_median)

h_l = get_share_trips(trip_counts, low_to_high_gini)
l_h = get_share_trips(trip_counts, high_to_low_gini)
l_l = get_share_trips(trip_counts, low_to_low_gini)
h_h = get_share_trips(trip_counts, high_to_high_gini)
