# Understanding the role of mobility in segregation patterns in the city of Madrid

This study explores the relationship between income inequality and urban mobility in the city of Madrid. Literature shows that bringing mobility into the study of inequality and segregation can bring an extra dimension to its study. By using a granular mobility dataset of trips throughout a month of 2022, a series of methods are developed to measure which districts play a central role in pulling and pushing travellers, and to measure which income groups travel more, and longer distances within the city. This research provides insights on the ongoing income segregation patterns in Madrid, and identifies slightly homophilic travelling tendencies. It also reveals that lower income groups tend to travel more and longer on average than higher income groups. This research contributes to the field of urban studies and emerging fields like Science of Cities or Urban Data Science, and aims to aid policymakers to identify mobility isolated areas in the urban space to develop effective policies to reduce the negative effects of gentrification and segregation.

The main research question driving my research is:

>  To what extent do residents from economically segregated districts in Madrid move differently than those in other districts?

To answer this question, I developed the following hypotheses to guide research:

> Low-income and highly segregated districts push residents out for daily mobility purposes, like work or recreational, whereas high-income and low segregated districts pull residents, as these districts tend to offer higher amenities and work possibilities.

> Residents from low-income and highly segregated districts tend to make a higher number of trips to high-income and low segregated districts than vice versa.

> Residents from low-income and highly segregated districts tend to perform, on average, longer distance trips than those living in high-income and low segregated districts.

## Methods

TODO

## Results

TODO

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

## Script Execution Order and Descriptions

| Order | Folder              | Script Name               | Description                                                                 |
|-------|---------------------|---------------------------|-----------------------------------------------------------------------------|
| 1     | mobility_data       | get_viajes.py            | Extracts raw trip data from MITMA and formats it into a usable dataset for analysis. Different variables can be selected to either download a monthly sample or a smaller one.  |
| 2     | mobility_data       | get_geometrias.py        | Retrieves and cleans the Madrid city geometries and their respective names. |
| 3     | data_overview       | main_descriptives.py     | Generates general descriptive statistics and summary plots for the income data, city landscape and segregation measures. |
| 4     | data_overview       | viajes_stats.py          | Computes trip-level statistics.  |
| 5     | segregation_indices | preprocessing.py         | Cleans and prepares data for segregation measures.               |
| 6     | segregation_indices | assortativity_matrix.py  | Constructs the assortativity matrices used to measure mixing across income deciles. The median income per consumption unit and the Gini index variables can be selected to generate the deciles.|
| 7     | segregation_indices | morans_i.py              | Calculates local and global Moran's I to measure spatial autocorrelation of income levels. The income variables of interest can be selected. |
| 8     | trip_analysis       | trip_count.py            | Computes and analyzes trip counts across districts based on median income and Gini index districts of residence to detect patterns. Outputs the trip count dataset and the shares of trips from low to high quantiles and vice versa.|
| 9     | trip_analysis       | trip_distances.py        | Computes and visualizes trip distances to analyze mobility patterns based on the median income and Gini index quantiles of residence of individuals. |
| 10    | network          | get_graph.py             | Builds a graph structure from mobility data for clustering analysis. It outputs the graph in pickle format, an adjacency matrix displayed as a heatmap, and the adjacency matrix displayed as a numpy file.  |
| 11    | network          | regressions.py           | Runs regression models to analyze relationships between in-weight, out-weight and the variables of interest: median income per consumption unit and the Gini index. |
| 12    | network          | visualization.py         | Generates visualizations of the previously built graph as html.   |


## Configuration Variables

TODO
