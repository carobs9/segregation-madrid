# Mobility and Income Segregation in Madrid, Spain

This study explores the relationship between income inequality and urban mobility in the city of Madrid. Literature shows that bringing mobility into the study of inequality and segregation can bring an extra dimension to its study. By using a granular mobility dataset of trips throughout a month of 2022 (obtained from [MITMA Estudios Básicos](https://www.transportes.gob.es/ministerio/proyectos-singulares/estudios-de-movilidad-con-big-data/estudio-basico-diario)), a series of methods are developed to measure which districts play a central role in pulling and pushing travellers, and to measure which income groups travel more, and longer distances within the city. This research provides insights on the ongoing income segregation patterns in Madrid, and identifies slightly homophilic travelling tendencies. It also reveals that lower income groups tend to travel more and longer on average than higher income groups. This research contributes to the field of urban studies and emerging fields like Science of Cities or Urban Data Science, and aims to aid policymakers to identify mobility isolated areas in the urban space to develop effective policies to reduce the negative effects of gentrification and segregation.

The main research question driving my research is:

>  To what extent do residents from economically segregated districts in Madrid move differently than those in other districts?

To answer this question, I developed the following hypotheses to guide research:

> Low-income and highly segregated districts push residents out for daily mobility purposes, like work or recreational, whereas high-income and low segregated districts pull residents, as these districts tend to offer higher amenities and work possibilities.

> Residents from low-income and highly segregated districts tend to make a higher number of trips to high-income and low segregated districts than vice versa.

> Residents from low-income and highly segregated districts tend to perform, on average, longer distance trips than those living in high-income and low segregated districts.

You can read the paper by clicking the here: [Paper](https://carobs9.neocities.org/THESIS_FINAL_BRANAS.pdf)

You can view the resulting mobility network by clicking here: [View Network of Madrid](https://carobs9.neocities.org/no_threshold)

## Methods and Results

### Exploratory Analysis

#### Method
I perform an exploratory analysis to address the state of income distribution in Madrid during 2021. This allows me to select the appropriate income variables for the study. To do so, (1) I plot and study the distribution of six income estimators to understand which are more accurate for representing the income and segregation levels of the districts. Based on this analysis, I select two key variables to understand the interactions between mobility and income: the median income per consumption unit and the Gini index by district. (2) I then calculate Global and Local Moran indices for each district based on the median income per consumption unit to illustrate the clustered patterns of income distribution in the city.

#### Results
Based on this analysis, I conclude that there is spatial autocorrelation in terms of the median income per consumption unit in the city of Madrid in 2021, with significant clustering patterns in 48\% of the districts. 

### Test Hypothesis 1

#### Method
I build an origin-destination (OD) dataset containing normalised trip counts within and between districts. These counts are used to build a mobility network and a consequent adjacency matrix. The construction of a network allows to quantitatively analyse the in and out-weights of the nodes. Lastly, I build complementary assortativity matrices based on trips between income and Gini index deciles to study whether there are any mobility patterns across deciles.

#### Results
Based on the assortativity matrices and the adjacency matrix, I conclude that there is a moderate tendency of individuals to stay within their own Gini index deciles, performing a relatively high number of intra-district trips, but still showing certain intra-district interaction. A lower assortativity pattern was found in the case of median income deciles, indicating higher mixing, but the results were not found to be statistically significant.

No significant relationship between low median income, highly segregated districts and out-weight was found, nor a relationship between high median income, low segregated districts and in-weight. In fact, a significant, positive relationship between highly segregated districts and the in-weight was found.


### Test Hypothesis 2

#### Method
I use the previously created trip counts dataset. The districts of origin and destination are classified into four quantiles based on the median income and also on the Gini index values, and I compare the differences among the furthest quantiles. This allows to further analyse the total number of trips between and within districts based the income background of the individuals.

#### Results
I conclude that residents from lower median income per consumption unit districts perform 1.33% more trips to higher income quantiles than vice versa. I also conclude that residents from low segregated districts also tend to perform around 1.85% more trips to higher segregated districts than vice versa.
The differences in intra-quantile share of trips are 6.57% and 2.3% for the median income and Gini index respectively. 

### Test Hypothesis 3

#### Method
I analyse the average distance of the trips based on the four aforementioned quantiles by variable. I retrieve the average trip distance by OD pair, and compare these based on the top and lowest quantile.

#### Results
I conclude that residents from the lowest median income quantile travel slightly longer distances on average than residents from the highest median income quantile. Residents from the highest Gini index quantile travel shorter distances on average than residents from the lowest Gini index quantile. I also conclude that the average distance of most trips falls under a 0.5 km - 2.5 km window, and that those performing the longest average trips belong to the low-income and low-Gini quantiles.

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
| 3     | segregation_indices | preprocessing.py         | Cleans and prepares data for segregation measures.               |
| 4     | segregation_indices | assortativity_matrix.py  | Constructs the assortativity matrices used to measure mixing across income deciles. The median income per consumption unit and the Gini index variables can be selected to generate the deciles.|
| 5     | segregation_indices | morans_i.py              | Calculates local and global Moran's I to measure spatial autocorrelation of income levels. The income variables of interest can be selected. |
| 6     | trip_analysis       | trip_count.py            | Computes and analyzes trip counts across districts based on median income and Gini index districts of residence to detect patterns. Outputs the trip count dataset and the shares of trips from low to high quantiles and vice versa.|
| 7     | trip_analysis       | trip_distances.py        | Computes and visualizes trip distances to analyze mobility patterns based on the median income and Gini index quantiles of residence of individuals. |
| 8    | network          | get_graph.py             | Builds a graph structure from mobility data for clustering analysis. It outputs the graph in pickle format, an adjacency matrix displayed as a heatmap, and the adjacency matrix displayed as a numpy file.  |
| 9    | network          | regressions.py           | Runs regression models to analyze relationships between in-weight, out-weight and the variables of interest: median income per consumption unit and the Gini index. |
| 10    | network          | visualization.py         | Generates visualizations of the previously built graph as html.   |
| 11    | data_overview       | main_descriptives.py     | Generates general descriptive statistics and summary plots for the income data, city landscape and segregation measures. |
| 12    | data_overview       | viajes_stats.py          | Computes trip-level statistics.  |


## Configuration Variables

| Variable Name | Options              |
|-------|---------------------|
| DF_OF_INTEREST | String of the dataframe from MITMA |
| MONTH_DAYS |List containing days of the month of interest|
| type_of_study     | 'month', 'week', 'weekend', 'morans', 'two_weeks'. 'month' has been used to perform this study, and 'morans' when calculating the morans indices.| 
| ROOT_PATH     | Root path as Path objet      | 
| SAVE_DFS     | Boolean: True / False     | 
| SAVE_FIGURES     | Boolean: True / False       | 
| INCOME_VARS_OF_INTEREST     |     'Gini Index','Average income per consumption unit','Median income per consumption unit','Average gross income per household','Average gross income per person','Average net income per household','Average net income per person'     | 

## Known Issues

The Pyproj CRS method gives problems based on the environment. It is not needed to replicate the study, so it has been commented out through the files. In addition, the Figures, Morans and Month directories need to be created by the user, as the directory is not created by running the code. In the future, this bug will be corrected.
