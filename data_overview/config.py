from pathlib import Path

# Set the root path
# ROOT_PATH = Path('C:/Users/rqg886/Desktop/THESIS_PROJECT')
ROOT_PATH = Path('/Users/caro/Desktop/segregation-madrid')
FOLDER_PATH = 'data_overview'

# general folders
METRO_DATA = ROOT_PATH / 'metro_data' 
MOBILITY_DATA = ROOT_PATH / 'mobility_data' 
DEMOGRAPHIC_DATA = ROOT_PATH / 'demographic_data' 

#subfolders
VIAJES_DATA = MOBILITY_DATA / 'VIAJES' 
PERSONAS_DATA = MOBILITY_DATA / 'PERSONAS'
GEOMETRIA_DATA = MOBILITY_DATA / 'GEOMETRIA' 
ZONIFICACION_DATA = MOBILITY_DATA / 'ZONIFICACION' 

OUTPUTS_PATH = ROOT_PATH / FOLDER_PATH / 'outputs'
INCOME_DATA = ROOT_PATH / 'segregation_indices/data/processed'
FIGURES_PATH = ROOT_PATH / FOLDER_PATH / 'figures'

DATASETS_PATH = ROOT_PATH / FOLDER_PATH / 'outputs'
FIGURES_PATH = ROOT_PATH / FOLDER_PATH / 'figures'

type_of_study = 'month' # 'week', 'weekend', 'month' or 'morans', or 'two_weeks'

# 3. Variables of interest
INCOME_VARS_OF_INTEREST = [
    'Average income per consumption unit',
    'Median income per consumption unit',
    'Average gross income per household',
    'Average gross income per person',
    'Average net income per household',
    'Average net income per person'
]

# 4. Save figures
SAVE_FIGURES = True

# 5. sAVE DATASETS
SAVE_DATASETS = True