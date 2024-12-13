# Understanding the role of mobility in segregation patterns in the city of Madrid
Thesis project to understand the role of mobility in segregation patterns in the city of Madrid.

This study explores the relationship between income inequality and urban mobility in the city of Madrid. Literature shows that bringing mobility into the study of inequality and segregation can bring an extra dimension to its study. By using a granular mobility dataset of trips throughout a month of 2022, a series of methods are developed to measure which districts play a central role in pulling and pushing travellers, and to measure which income groups travel more, and longer distances within the city. This research provides insights on the ongoing income segregation patterns in Madrid, and identifies slightly homophilic travelling tendencies. It also reveals that lower income groups tend to travel more and longer on average than higher income groups. This research contributes to the field of urban studies and emerging fields like Science of Cities or Urban Data Science, and aims to aid policymakers to identify mobility isolated areas in the urban space to develop effective policies to reduce the negative effects of gentrification and segregation.

## Installation

- Install Python (version 3.11 was used for this development).
- Clone the repository from terminal (Git must be installed):

git clone https://...

- To activate the environment, run:
    - On Mac: 
    '''source ./<your_env_name>/bin/activate'''
    - On Windows:
     '''./<your_env_name>/Scripts/activate'''
    - On Linux:
     '''./<your_env_name>/bin/activate'''

- To Install the dependencies:
'''
pip install -r requirements.txt
'''

## Known Issues

Pyproj package is giving problems with the CRS.

## Order of the scripts

| Folder | File 1 | File 2 | File 3 |
| --- | --- | --- | --- |
| mobility_data | get_viajes.py | get_geometrias.py | ... |
| data_overview | main_descriptives.py  | viajes_stats.py | ... |
| segregation_indices | preprocessing.py  | assortativity_matrix.py| morans_i.py |
| trip_analysis | trip_count.py  | trip_distances.py  ... |
| clustering | get_graph.py  | regressions.py | visualization |


mobility_data:
    1. get_viajes.py 
    2. get_geometrias.py

data_overview:
    1. main_descriptives.py (fix)
    2. viajes_stats.py (fix)

segregation_indices:

trip_analysis:
    1. trip_analysis

clustering:
    1. get_graph.py
    2. regressions.py
    3. visualization.py
 
