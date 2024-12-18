import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import config as cfg
import pandas as pd
import geopandas as gpd
import sys
import logging
from scipy.stats import pearsonr
from utils import *

# Configure general logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Capture all messages from DEBUG and above

# Create a file handler for logging DEBUG and above messages to a file
file_handler = logging.FileHandler('logs/assortativity_matrix_by_dest.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Add the handler to the logger
logger.addHandler(file_handler)

# SET VARIABLES -----------------------------------------------------------------

# FIXME: Make more efficient, and fix variable names to plot nicely
var_of_interest = 'Median income per consumption unit' 
n_income_deciles = 10

if cfg.type_of_study == 'month':
    time_of_study = 'March 2022'
elif cfg.type_of_study == 'week':
    time_of_study = 'Normal Week'
elif cfg.type_of_study == 'two_weeks':
    time_of_study = 'Two Weeks'
elif cfg.type_of_study == 'weekend':
    time_of_study = 'Weekend'
else:
    print('No correct time of study has been set. Maybe you meant week or weekend?')

logger.info(f'I calculate {n_income_deciles} income deciles for different income data in the city of Madrid')
logger.info(f'Timeframe: {time_of_study}')
logger.info(f'I build assortativity matrices for the {var_of_interest}')
logger.info(f'The variables for which income deciles are calculared are: {cfg.INCOME_VARS_OF_INTEREST}')
logger.info(f'Save figures = {cfg.SAVE_FIGURES}')
logger.info(f'Figures path: {cfg.FIGURES_PATH}')


# OPEN DATA ----------------------------------------------------------------------

logger.info('Opening data...')

rent_data = gpd.read_file(cfg.INCOME_DATA / 'geometries_and_income.geojson') # rent data to add to the viajes data to find income per district
rent_data = rent_data[['ID', 'geometry'] + cfg.INCOME_VARS_OF_INTEREST ] # here I select the variables of interest

if cfg.type_of_study == 'month':
    file_name = 'all_viajes_month_0322.csv'
elif cfg.type_of_study == 'week':
    file_name = 'viajes_week_0322.csv'  #TODO: CORRECT IF NEEDED
elif cfg.type_of_study == 'two_weeks':
    file_name = 'viajes_two_weeks_0322.csv'  #TODO: CORRECT IF NEEDED
elif cfg.type_of_study == 'weekend':
    file_name = 'viajes_weekend_0322.csv'
else:
    file_name = 'default_file.csv'  # FIXME: Fallback option if neither is True

mobility = pd.read_csv(cfg.MOBILITY_DATA / f'VIAJES/{file_name}', thousands='.', decimal=',') # week of interest
mobility = mobility.loc[(mobility['actividad_origen'] == 'casa') & (mobility['actividad_destino'] == 'trabajo_estudio')] # trips from home to work
print(mobility.shape)
logger.info(f"Dataframes used: {cfg.INCOME_DATA / 'geometries_and_income.geojson'} and {cfg.MOBILITY_DATA / f'VIAJES/{file_name}'}")
logger.info('Shape of the rent dataset: %s', rent_data.shape)
logger.info('Shape of the mobility dataset: %s', mobility.shape)

# MERGE INCOME AND MOBILITY DATA ----------------------------------------------------------------------

logger.info('1. Merging mobility and income data')
# 1. Adding income data per district to the mobility data, to later calculate deciles and build assortativity matrix
viajes_with_income = pd.merge(
    mobility,
    rent_data,
    left_on='origen',  # The cleaned 'origen' from viajes DataFrame
    right_on='ID',  # The 'ID' from gdf
    how='left'  # Perform a left join to keep all rows from viajes
)

logger.info(f'Variable to calculate matrices on is set to: {var_of_interest}')

# CALCULATE INCOME DECILES ----------------------------------------------------------------------

logger.info(f'2. Calculating {n_income_deciles} income deciles for the {var_of_interest} data.')

# 2. Divide data into income deciles D for each SE class - for each origin and destination, I add the income decile 
if var_of_interest == 'Median income per consumption unit':
    rent_data['income_decile'] = pd.qcut(rent_data[var_of_interest].rank(method='first'), n_income_deciles, labels=False)
elif var_of_interest == 'Gini Index':
    rent_data['income_decile'] = pd.qcut(rent_data[var_of_interest].rank(method='first'), n_income_deciles, labels=False) 
else:
    rent_data['income_decile'] = pd.qcut(rent_data[var_of_interest], n_income_deciles, labels=False)

# Add deciles to df
viajes_with_income = pd.merge(viajes_with_income, rent_data[['ID', 'income_decile']], 
                              left_on='origen', right_on='ID', how='left', suffixes=('', '_origin'))

viajes_with_income = pd.merge(viajes_with_income, rent_data[['ID', 'income_decile']], 
                              left_on='destino', right_on='ID', how='left', suffixes=('', '_dest'))
# Clean df 
viajes_with_income.drop(columns=['residencia', 'estudio_origen_posible', 'estudio_origen_posible', 'ID', 'ID_origin', 'ID_dest'], inplace=True)

# PLOT INCOME DECILES -----------------------------------------------------------------------------------------------

logger.info('Plotting income deciles')
bin_counts = viajes_with_income.groupby('income_decile')['viajes'].sum()
bin_counts.plot(kind='bar')

# 1. matplotlib. FIXME: IS this plot correct? I have to make sure it makes sense.
plt.xlabel('Income Bin')
plt.ylabel('Number of Entries')
plt.title(f'Distribution of Deciles for Destination of Trips\n{time_of_study}\nVariable: {var_of_interest.lower()}')

if cfg.SAVE_FIGURES:
    plt.savefig(cfg.FIGURES_PATH / f'work_dest_{var_of_interest.lower()}_deciles_distribution_destination.png', dpi=300, bbox_inches='tight')
    logger.info(f"Plot saved at: {cfg.FIGURES_PATH / f'{var_of_interest.lower()}_work_dest_deciles_distribution_destination.png'}")

logger.info(f'Income deciles for {cfg.INCOME_VARS_OF_INTEREST} saved!')

# BUILD ASSORTATIVITY MATRICES ----------------------------------------------------------------------------------------

logger.info('Building assortativity matrices...')

# Group by origin and destination deciles and count the trips
trip_counts_by_decile = viajes_with_income.groupby(['renta', 'income_decile', 'income_decile_dest'])['viajes'].sum().reset_index(name='trip_count')
districts = rent_data['ID'].unique()

try:
    # Try using pivot() if there are no duplicate index/column combinations
    assortativity_matrix = trip_counts_by_decile.pivot(
        index='income_decile', 
        columns='income_decile_dest', 
        values='trip_count'
    ).fillna(0)

except ValueError as e:
    logger.debug(f"Encountered an error with pivot(): {e}")
    logger.debug("Switching to pivot_table() to handle duplicates.")
    
    # Use pivot_table() with aggregation to handle duplicates
    assortativity_matrix = trip_counts_by_decile.pivot_table(
        index='income_decile', 
        columns='income_decile_dest', 
        values='trip_count', 
        aggfunc='sum',  # Aggregate duplicates by summing trip counts
        fill_value=0  # Fill missing values with 0
    )

logger.info("Assortativity matrix created successfully!")

# Normalize 
assortativity_matrix_normalized = assortativity_matrix.div(assortativity_matrix.sum(axis=1), axis=0)

logger.info("Assortativity matrix normalized successfully!")

# STRATIFY MOBILITY DATA BY RENT ----------------------------------------------------------------------------------

middle = trip_counts_by_decile[trip_counts_by_decile['renta']=='10-15']
high = trip_counts_by_decile[trip_counts_by_decile['renta']=='>15']

assortativity_matrix_middle = middle.pivot(index='income_decile', columns='income_decile_dest', values='trip_count').fillna(0)
assortativity_matrix_middle_normalized = assortativity_matrix_middle.div(assortativity_matrix_middle.sum(axis=1), axis=0)

assortativity_matrix_high = high.pivot(index='income_decile', columns='income_decile_dest', values='trip_count').fillna(0)
assortativity_matrix_high_normalized = assortativity_matrix_high.div(assortativity_matrix_high.sum(axis=1), axis=0)

logger.info('Stratifying mobility data by rent...')
logger.debug('Put more thought into this, and review')


# GET ASSORTATIVITY COEFFICIENT AND P-VALUE ------------------------------------------------------------------------

rho, p_value = calculate_assortativity_coefficient(assortativity_matrix_normalized)  
rho_middle, p_value_middle = calculate_assortativity_coefficient(assortativity_matrix_middle_normalized)  
rho_high, p_value_high = calculate_assortativity_coefficient(assortativity_matrix_high_normalized)  

# PLOT ASSORTATIVITY MATRICES STRATIFIED BY RENT ------------------------------------------------------------------

plot_assortativity_matrix(assortativity_matrix, f'work_dest_assortativity_matrix_{var_of_interest.lower()}.png', annot=False)
plot_assortativity_matrix(assortativity_matrix_normalized, f'work_dest_normalized_assortativity_matrix_{var_of_interest.lower()}.png', rho, p_value)

plot_assortativity_matrix(assortativity_matrix_middle_normalized, f'work_dest_10_15_bracket_normalized_assortativity_matrix_{var_of_interest.lower()}.png', rho_middle, p_value_middle)
plot_assortativity_matrix(assortativity_matrix_high_normalized, f'work_dest_15_bracket_normalized_assortativity_matrix_{var_of_interest.lower()}.png', rho_high, p_value_high)

# PLOT AND SAVE ASSORTATIVITY MATRICES --------------------------------------------------------------------------------------

logger.info(f"All assortativity matrices figures for {var_of_interest} saved successfully!")

sys.exit("Stopping the script")