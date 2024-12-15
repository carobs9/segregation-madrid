import pickle
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from utils import check_in_weights, check_out_weights
import config as cfg

if cfg.type_of_study == 'month':
    file_name = 'all_viajes_month_0322.csv'
elif cfg.type_of_study == 'week':
    file_name = 'viajes_week_0322.csv'  #TODO: CORRECT IF NEEDED
elif cfg.type_of_study == 'two_weeks':
    file_name = 'viajes_two_weeks_0322.csv'  #TODO: CORRECT IF NEEDED
elif cfg.type_of_study == 'weekend':
    file_name = 'viajes_weekend_0322.csv'  #TODO: CORRECT IF NEEDED
else:
    file_name = 'default_file.csv'  # FIXME: Fallback option if neither is True

# load graph object from file
G = pickle.load(open(cfg.ROOT_PATH / f'network/graphs/{file_name}.pickle', 'rb')) # TAKING THE NETWORK WITH NORMALIZED WEIGHTS , FIXED
income = gpd.read_file(cfg.ROOT_PATH / 'segregation_indices/data/processed/geometries_and_income.geojson')
gdf = gpd.read_file(cfg.ZONIFICACION_DATA / 'distritos/madrid_gdf.geojson')
distritos = pd.read_csv(cfg.ZONIFICACION_DATA / 'distritos/PROCESSED_nombres_distritos.csv')

in_weights = check_in_weights(G)
out_weights = check_out_weights(G)

in_weights_df = pd.DataFrame(list(in_weights.items()), columns=['District', 'Total In-weight'])
out_weights_df = pd.DataFrame(list(out_weights.items()), columns=['District', 'Total Out-weight'])

gdf['ID'] = gdf['ID'].astype('int64')
distritos['ID'] = distritos['ID'].astype('int64')

distritos_and_gdf = pd.merge(distritos, gdf, on='ID', how='inner') # merging the income and geography data into one gdf
distritos_and_gdf = gpd.GeoDataFrame(distritos_and_gdf, geometry='geometry')
distritos_and_gdf.rename(columns={'name_2': 'District'}, inplace=True)

# turning in-weights into gdf
in_weights_gdf = pd.merge(in_weights_df, distritos_and_gdf, on='District', how='inner') 
in_weights_gdf = gpd.GeoDataFrame(in_weights_gdf, geometry='geometry')

# turning out-weights into gdf
out_weights_gdf = pd.merge(out_weights_df, distritos_and_gdf, on='District', how='inner')
out_weights_gdf = gpd.GeoDataFrame(out_weights_gdf, geometry='geometry')

vmin = min(in_weights_gdf['Total In-weight'].min(), out_weights_gdf['Total Out-weight'].min())
vmax = max(in_weights_gdf['Total In-weight'].max(), out_weights_gdf['Total Out-weight'].max())

# Plot In-Weights
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Create side-by-side plots

# In-Weight plot
in_weights_gdf.plot(
    column='Total In-weight',  # Column containing the LISA values
    cmap='RdPu',               # Use the RdPu colormap
    legend=True,               # Show legend
    ax=axes[0],                # Axis to plot on (left)
    vmin=vmin,                 # Set common minimum value for scale
    vmax=vmax                  # Set common maximum value for scale
)
axes[0].set_title('In-Weight Distribution')  # Title for In-Weight
axes[0].set_axis_off()  # Remove axis labels

# Save the In-Weight figure if required
if cfg.SAVE_FIGURES:
    plt.savefig(cfg.FIGURES_PATH / f'{cfg.type_of_study}_in_weight_distribution.png', dpi=300, bbox_inches='tight')

# Out-Weight plot
out_weights_gdf.plot(
    column='Total Out-weight',  # Column containing the LISA values
    cmap='RdPu',               # Use the same colormap for consistency
    legend=True,               # Show legend
    ax=axes[1],                # Axis to plot on (right)
    vmin=vmin,                 # Set common minimum value for scale
    vmax=vmax                  # Set common maximum value for scale
)
axes[1].set_title('Out-Weight Distribution')  # Title for Out-Weight
axes[1].set_axis_off()  # Remove axis labels

# Adjust layout to avoid overlapping legends
plt.tight_layout()

# Save the Out-Weight figure if required
if cfg.SAVE_FIGURES:
    plt.savefig(cfg.FIGURES_PATH / f'{cfg.type_of_study}_weight_distribution.png', dpi=300, bbox_inches='tight')

# Show the combined figure
plt.show()
