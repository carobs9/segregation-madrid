# Understanding the role of mobility in segregation patterns in the city of Madrid
Thesis project to understand the role of mobility in segregation patterns in the city of Madrid.

This study explores the relationship between income inequality and urban mobility in the city of Madrid. Literature shows that bringing mobility into the study of inequality and segregation can bring an extra dimension to its study. By using a granular mobility dataset of trips throughout a month of 2022, a series of methods are developed to measure which districts play a central role in pulling and pushing travellers, and to measure which income groups travel more, and longer distances within the city. This research provides insights on the ongoing income segregation patterns in Madrid, and identifies slightly homophilic travelling tendencies. It also reveals that lower income groups tend to travel more and longer on average than higher income groups. This research contributes to the field of urban studies and emerging fields like Science of Cities or Urban Data Science, and aims to aid policymakers to identify mobility isolated areas in the urban space to develop effective policies to reduce the negative effects of gentrification and segregation.

## Installation

- Install Python (version 3.11 was used for this development).
- Clone the repository from terminal (Git must be installed):
     ```
     git clone https://github.com/carobs9/segregation-madrid.git
     ```

- To activate the environment, run:
    - On Mac:
      ```
      source ./<your_env_name>/bin/activate
      ```
    - On Windows:
      ```
      ./<your_env_name>/Scripts/activate
      ```
    - On Linux:
       ```
      ./<your_env_name>/bin/activate
      ```

- To Install the dependencies:
       ```
      pip install -r requirements.txt
      ```
## Known Issues

Pyproj package is giving problems with the CRS.

## Order of the scripts

# Script Execution Order and Descriptions

| Order | Folder              | Script Name               | Description                                                                 |
|-------|---------------------|---------------------------|-----------------------------------------------------------------------------|
| 1     | mobility_data       | get_viajes.py            | Extracts raw trip data from MITMA and formats it into a usable dataset for analysis. Different variables can be selected to either download a monthly sample or a smaller one.  |
| 2     | mobility_data       | get_geometrias.py        | Fetches and processes geometric boundaries of regions (e.g., neighborhoods). |
| 3     | data_overview       | main_descriptives.py     | Generates descriptive statistics and summary plots for the trip data.     |
| 4     | data_overview       | viajes_stats.py          | Computes trip-level statistics such as average distances and frequencies.  |
| 5     | segregation_indices | preprocessing.py         | Cleans and prepares data for segregation index calculations.               |
| 6     | segregation_indices | assortativity_matrix.py  | Constructs an assortativity matrix to measure income-based segregation.    |
| 7     | segregation_indices | morans_i.py              | Calculates Moran's I to measure spatial autocorrelation of income levels.  |
| 8     | trip_analysis       | trip_count.py            | Analyzes trip counts across regions to detect patterns.                    |
| 9     | trip_analysis       | trip_distances.py        | Computes and visualizes trip distances to analyze mobility patterns.       |
| 10    | clustering          | get_graph.py             | Builds a graph structure from mobility data for clustering analysis.       |
| 11    | clustering          | regressions.py           | Runs regression models to analyze relationships between mobility and socioeconomic factors. |
| 12    | clustering          | visualization.py         | Generates visualizations of clusters, graphs, and key mobility patterns.   |


