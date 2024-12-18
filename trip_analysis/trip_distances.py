import networkx as nx
import pandas as pd
import geopandas as gpd
import config as cfg
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utils import get_district_names, get_income_data, add_quantiles, plot_distances, build_distance_count

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
    all_viajes = pd.read_csv(cfg.VIAJES_DATA / 'viajes_weekend_0322.csv', thousands='.',decimal=',')  # Subtracting trips in Madrid districts during weekend
    data_name = 'Weekend'
else:
    raise ValueError('No time of study has been set')

income = gpd.read_file(cfg.ROOT_PATH / 'segregation_indices/data/processed/geometries_and_income.geojson') # income data

filtered_df = all_viajes.loc[(all_viajes['actividad_origen'] == 'casa')] # home origin trips

distance_counts = build_distance_count(filtered_df) # adding 'distancia' to the analysis
distance_counts = get_district_names(distance_counts)
distance_counts = get_income_data(distance_counts, income, 'Gini Index', 'Median income per consumption unit')
distance_counts = add_quantiles(distance_counts, 'Median income per consumption unit', n_quantiles=4)
distance_counts = add_quantiles(distance_counts, 'Gini Index', n_quantiles=4)

low_median_income = distance_counts[distance_counts['income decile origin Median income per consumption unit'].isin([0])]
high_median_income = distance_counts[distance_counts['income decile origin Median income per consumption unit'].isin([3])]
low_median_income['Income Group'] = 'Low Income'
high_median_income['Income Group'] = 'High Income'

low_gini = distance_counts[distance_counts['income decile origin Gini Index'].isin([0])]
high_gini = distance_counts[distance_counts['income decile origin Gini Index'].isin([3])]
low_gini['Gini Group'] = 'Low Gini'
high_gini['Gini Group'] = 'High Gini'

fig = plot_distances(low_median_income, high_median_income, 'Median Income')
fig.savefig(cfg.FIGURES_PATH / 'median_distances.png', dpi=300)

fig = plot_distances(low_gini, high_gini, 'Gini Index')
fig.savefig(cfg.FIGURES_PATH / 'gini_distances.png', dpi=300)