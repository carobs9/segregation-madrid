import config as cfg
import geopandas as gpd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as mticker

sns.set(font_scale=1.2) 

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

merged = gpd.read_file(cfg.ROOT_PATH / 'segregation_indices/data/geometries_and_income.geojson') # merging processed done at 'preprocessing'
distritos = pd.read_csv(cfg.ZONIFICACION_DATA / 'distritos/PROCESSED_nombres_distritos.csv')

all_viajes = pd.read_csv(cfg.MOBILITY_DATA / f'VIAJES/{file_name}', thousands='.', decimal=',') #df of interest
filtered_viajes = all_viajes.loc[(all_viajes['actividad_origen'] == 'casa')]
population = pd.read_csv(cfg.ROOT_PATH / 'data_overview/raw/poblacion_distritos_enero_21.csv', sep=';') # SOURCE: https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Estadistica/?vgnextfmt=default&vgnextchannel=8156e39873674210VgnVCM1000000b205a0aRCRD

population = population.drop(columns=['Total.1'])
population.columns = ['ID', 'Population']
distritos['ID'] = distritos['ID'].astype(str)
population['ID'] = population['ID'].astype(str)
distritos_and_pop = pd.merge(distritos, population, left_index=True, right_index=True)
distritos_and_pop = distritos_and_pop.drop(columns=['ID_y'])
distritos_and_pop = distritos_and_pop.rename(columns={'ID_x': 'ID'})

morans = pd.read_csv(cfg.ROOT_PATH / 'segregation_indices/outputs/global_morans_i_df.csv')

normalized_trip_counts = pd.read_csv(cfg.ROOT_PATH / f'trip_analysis/outputs/{cfg.type_of_study}_normalized_trip_count.csv')

origin_trips = filtered_viajes.groupby('origen')['viajes'].sum().reset_index(name='total_viajes') 

# PLOTTING INCOME QUANTILES -----------------------------------------------------------------------------------------------

f, axs = plt.subplots(nrows=2, ncols=3, figsize=(14, 14))
# Make the axes accessible with single indexing
axs = axs.flatten()
# Start a loop over all the variables of interest
for i, col in enumerate(cfg.INCOME_VARS_OF_INTEREST):
    # select the axis where the map will go
    ax = axs[i]
    # Plot the map
    merged.plot(
        column=col,
        ax=ax,
        scheme="Quantiles",
        k=5, # n quantiles
        legend=True,
        legend_kwds={"loc": "lower left"},
        linewidth=0,
        cmap="RdPu",
    )
    # Remove axis clutter
    ax.set_axis_off()
    # Set the axis title to the name of variable being plotted
    ax.set_title(col)

f.show()
if cfg.SAVE_FIGURES:
    f.savefig(cfg.FIGURES_PATH / 'income_quantiles.png', dpi=300, bbox_inches='tight')


# GINI INDEX --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

fig, ax = plt.subplots(1, figsize=(6, 6))
merged.plot(
        column='Gini Index',  # Column containing the LISA values
        cmap='RdPu',        # Use the RdPu colormap
        legend=True,            # Show legend
        ax=ax                   # Axis to plot on
    )
    
    # Set the title with global statistics
ax.set_title('Gini Index Distribution'
    )

    # Remove axis labels
ax.set_axis_off()
fig.show()
if cfg.SAVE_FIGURES:
        plt.savefig(cfg.FIGURES_PATH / f'gini_index_distribution.png', dpi=300, bbox_inches='tight')

# MEDIAN INCOME DISTRIBUTION ----------------------------------------------------------------------------------------------------------------------------------------

fig, ax = plt.subplots(1, figsize=(6, 6))
merged.plot(
        column='Median income per consumption unit',  # Column containing the LISA values
        cmap='RdPu',        # Use the RdPu colormap
        legend=True,            # Show legend
        ax=ax                   # Axis to plot on
    )
    
    # Set the title with global statistics
ax.set_title('Median Income per Consumption Unit Distribution'
    )

    # Remove axis labels
ax.set_axis_off()
fig.show()

# CITY OF MADRID -----------------------------------------------------------------------------------------------------------------------------------------

merged['ID'] = merged['ID'].astype(str)
gdf_with_names = merged.merge(distritos[['ID', 'name_2']], on='ID')
gdf_with_names = gdf_with_names[['ID', 'geometry', 'name_2']]
gdf_with_names['ID'] = gdf_with_names['ID'].astype(str).str[-2:]
# gdf_with_names = gdf_with_names.to_crs(epsg=3857)

ax = gdf_with_names.plot(figsize=(20,15), color="purple", alpha=0.15)
merged.boundary.plot(color="#DA70D6", ax=ax)

ctx.add_basemap(ax,
               # crs=gdf_with_names.crs.to_string(),
               source=ctx.providers.Esri.WorldGrayCanvas
              )

bounds = gdf_with_names.total_bounds
ax.set_xlim(bounds[0], bounds[2])  # Set x-axis (longitude)
ax.set_ylim(bounds[1], bounds[3])  # Set y-axis (latitude)

texts = []

# Add district names as annotations
for x, y, label in zip(gdf_with_names.geometry.centroid.x, 
                       gdf_with_names.geometry.centroid.y, 
                       gdf_with_names['ID']):
    texts.append(ax.text(x, y, label, fontsize=16, ha='center', color='black'))  # Change color of text to red

from matplotlib.lines import Line2D

legend_elements = [Line2D([0], [0], marker='o', color='w', label=f"{num}: {name}",
                          markerfacecolor='lightgray', markersize=12)
                   for num, name in zip(gdf_with_names['ID'], gdf_with_names['name_2'])]

ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.98),  # Adjust position inside plot
          title='Legend', fontsize=17, title_fontsize=19, frameon=True)  # Larger font sizes and frame

# Remove axes
ax.set_axis_off()
ax.set_title('Districts of Madrid', fontsize=20)
plt.axis('equal')

if cfg.SAVE_FIGURES:
    plt.savefig(cfg.FIGURES_PATH / 'districts_of_madrid.png', dpi=300, bbox_inches='tight')


# DISTRICTS AND POPULATION --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if cfg.SAVE_DATASETS:
    distritos_and_pop.to_csv(cfg.DATASETS_PATH / 'districts_and_population.csv', index=False)

# GINI INDEX DATAFRAME --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

merged['ID'] = merged['ID'].astype(str)
distritos_and_pop['ID'] = distritos_and_pop['ID'].astype(str)
gini_and_districts = pd.merge(merged[['ID', 'Gini Index']], distritos_and_pop[['ID', 'name_2']], on='ID')

# Select the 'name_2' and 'Gini Index' columns
gini_and_districts = gini_and_districts[['name_2', 'Gini Index']]

gini_and_districts = gini_and_districts.rename(columns={'name_2': 'District'})

if cfg.SAVE_DATASETS:
    gini_and_districts.to_csv(cfg.DATASETS_PATH / 'districts_and_gini.csv', index=False)

# GLOBAL MORANS I ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
morans_filtered = morans[morans['Variable'] != 'Gini Index']

variables = morans_filtered['Variable']  # The income variables
morans_I = morans_filtered['Global Morans I']  # The Global Moran's I values
p_values = morans_filtered['P-value']  # The p-values

colors = ['purple' if p < 0.05 else 'black' for p in p_values]

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(morans_I, variables, color=colors, s=100,  marker='s')  # s sets the size of the dots

# Set labels and title
plt.xlabel('Global Moran\'s I', fontsize=12)
plt.title('Global Moran\'s I for Income Variables and Significance Levels', fontsize=14)
plt.xticks(fontsize=12)

# Customizing the y-axis labels (income variables)
plt.yticks(range(len(variables)), variables, fontsize=12)

if cfg.SAVE_FIGURES:
    plt.savefig(cfg.FIGURES_PATH / 'global_morans_significance.png', dpi=300, bbox_inches='tight')

# INCOME DATA --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

income_stats = merged.describe()
income_stats_big = income_stats.drop(columns=['Gini Index'])
income_stats_small = income_stats[['Gini Index']]
income_stats_big = income_stats_big.round(3)
income_stats_small = income_stats_small.round(3)

if cfg.SAVE_DATASETS:
    income_stats_big.to_csv(cfg.DATASETS_PATH / 'income_stats.csv', index=True)
    income_stats_small.to_csv(cfg.DATASETS_PATH / 'gini_stats.csv', index=True)

income_stats_big = income_stats_big.drop(index='count')
income_stats_big = income_stats_big.reset_index().rename(columns={'index': 'Statistic'})
income_stats_big = income_stats_big.melt(id_vars='Statistic', var_name='Income Category', value_name='Value')

income_stats_small = income_stats_small.drop(index='count')
income_stats_small = income_stats_small.reset_index().rename(columns={'index': 'Statistic'})

plt.figure(figsize=(12, 8))

sns.boxplot(x='Income Category', y='Value', data=income_stats_big, palette='Set3')

plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)  # Increase the font size of y-tick labels
plt.title('Distribution of Income Statistics', fontsize=16)  # Increase the font size of the title
plt.xlabel('Income Category', fontsize=15)  # Increase font size for x-axis label
plt.ylabel('Value', fontsize=15)  # Increase font size for y-axis label
plt.tight_layout()

if cfg.SAVE_FIGURES:
    plt.savefig(cfg.FIGURES_PATH / 'income_statistics_boxplot.png', dpi=300, bbox_inches='tight')

# TRIP COUNTS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# normalized
plt.figure(figsize=(10, 6))
sns.histplot(normalized_trip_counts['normalized_trip_count'], bins=50, kde=True, color='blue', alpha=0.7)
ax = plt.gca()  # Get the current axis
ax.xaxis.set_major_locator(MaxNLocator(nbins=10))

formatter = mticker.ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)

plt.title('Distribution of Normalised Trip Counts')
plt.xlabel('Normalised Trip Count')
plt.ylabel('Density')
plt.tight_layout()
plt.savefig(f'{cfg.FIGURES_PATH}/{cfg.type_of_study}_normalized_trip_count_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# unnormalized
plt.figure(figsize=(10, 6))
sns.histplot(normalized_trip_counts['trip_count'], bins=50, kde=True, color='blue', alpha=0.7)

ax = plt.gca()  # Get the current axis

# Set axis formatter to remove scientific notation
formatter = mticker.ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)

ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)

# Set a reasonable number of x-axis bins
ax.xaxis.set_major_locator(MaxNLocator(nbins=10))

plt.xticks(rotation=90)

plt.title('Distribution of Total Trip Counts')
plt.xlabel('Total Trip Count')
plt.ylabel('Density')
plt.tight_layout()
plt.savefig(f'{cfg.FIGURES_PATH}/{cfg.type_of_study}_unnormalized_trip_count_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# TRIPS AND POPULATION -------------------------------------------------------------------------------------------------

distritos_and_pop["ID"] = distritos_and_pop["ID"].astype(str)
origin_trips["origen"] = origin_trips["origen"].astype(str)

df_combined = pd.merge(distritos_and_pop, origin_trips, left_on="ID", right_on="origen")
df_combined.drop(columns=["ID", "origen"], inplace=True)

df_combined["Population_normalized"] = df_combined["Population"] / df_combined["Population"].max()
df_combined["Viajes_normalized"] = df_combined["total_viajes"] / df_combined["total_viajes"].max()

plt.figure(figsize=(14, 8))

plt.bar(df_combined["name_2"], df_combined["Population_normalized"], label="Population (normalised)", alpha=0.7)

plt.plot(df_combined["name_2"], df_combined["Viajes_normalized"], label="Total Trips (normalised)", color="red", marker="o")

plt.title("Comparison of Population and Total Trips by District", fontsize=16)
plt.xlabel("District", fontsize=14)
plt.ylabel("Normalized Values", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig(f'{cfg.FIGURES_PATH}/{cfg.type_of_study}_APPENDIX_pop_and_trips.png', dpi=300, bbox_inches='tight')
plt.show()