from pathlib import Path

# Set the root path
# ROOT_PATH = Path('C:/Users/rqg886/Desktop/THESIS_PROJECT')
ROOT_PATH = Path('/Users/caro/Desktop/segregation-madrid')
FOLDER_PATH = 'network'

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
FIGURES_PATH = ROOT_PATH / FOLDER_PATH / 'figures'

DATASETS_PATH = ROOT_PATH / 'datasets'

# Set time of study
type_of_study = 'month' # 'week', 'weekend', 'month' or 'morans', or 'two_weeks'

SAVE_FIGURES = True