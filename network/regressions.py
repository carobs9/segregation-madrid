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

in_weights = check_in_weights(G)
out_weights = check_out_weights(G)

in_weights_df = pd.DataFrame(list(in_weights.items()), columns=['District', 'Total In-weight'])
out_weights_df = pd.DataFrame(list(out_weights.items()), columns=['District', 'Total Out-weight'])

in_weights_df.to_csv(cfg.ROOT_PATH / f'network/weights/{cfg.type_of_study}_in_weights.csv', index=False)
out_weights_df.to_csv(cfg.ROOT_PATH / f'network/weights/{cfg.type_of_study}_out_weights.csv', index=False)

in_weights_df['Median income per consumption unit'] = income['Median income per consumption unit'] / 1000
in_weights_df['Gini Index'] = income['Gini Index']

out_weights_df['Median income per consumption unit'] = income['Median income per consumption unit'] / 1000
out_weights_df['Gini Index'] = income['Gini Index']

# MODEL 1 ------------------------------------------------------------------------------------------------------------------------------

X = in_weights_df['Median income per consumption unit']
y = in_weights_df['Total In-weight']

# Add a constant (intercept) to the model
X = sm.add_constant(X)

# Step 3: Fit the regression model
model = sm.OLS(y, X).fit()

# Step 4: Display the regression results
print(model.summary())

with open(cfg.ROOT_PATH / f'network/regressions/{cfg.type_of_study}_in_weight_median.html', 'w') as file:
    file.write(model.summary().as_html())


# MODEL 2 ------------------------------------------------------------------------------------------------------------------------------

X = out_weights_df['Median income per consumption unit']
y = out_weights_df['Total Out-weight']

# Add a constant (intercept) to the model
X = sm.add_constant(X)

# Step 3: Fit the regression model
model = sm.OLS(y, X).fit()

# Step 4: Display the regression results
print(model.summary())

with open(cfg.ROOT_PATH / f'network/regressions/{cfg.type_of_study}_out_weight_median.html', 'w') as file:
    file.write(model.summary().as_html())


# MODEL 3 ------------------------------------------------------------------------------------------------------------------------------

X = in_weights_df['Gini Index']
y = in_weights_df['Total In-weight']

# Add a constant (intercept) to the model
X = sm.add_constant(X)

# Step 3: Fit the regression model
model = sm.OLS(y, X).fit()

# Step 4: Display the regression results
print(model.summary())

with open(cfg.ROOT_PATH / f'network/regressions/{cfg.type_of_study}_in_weight_gini.html', 'w') as file:
    file.write(model.summary().as_html())

# MODEL 4 ------------------------------------------------------------------------------------------------------------------------------

X = out_weights_df['Gini Index']
y = out_weights_df['Total Out-weight']

# Add a constant (intercept) to the model
X = sm.add_constant(X)

# Step 3: Fit the regression model
model = sm.OLS(y, X).fit()

# Step 4: Display the regression results
print(model.summary())

with open(cfg.ROOT_PATH / f'network/regressions/{cfg.type_of_study}_out_weight_gini.html', 'w') as file:
    file.write(model.summary().as_html())