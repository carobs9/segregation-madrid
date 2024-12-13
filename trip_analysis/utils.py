import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# DEFINING LABELS OF NODES 
district_mapping = pd.read_csv('/Users/caro/Desktop/thesis_project/data_overview/outputs/districts_and_population.csv')
id_to_name = district_mapping.set_index('ID')['name_2'].to_dict()


# TRIP ANALYSIS --------------------------------------------------------------------------------------------------- 

def build_trip_count(df): # FIXED
    # Determine the grouping columns based on whether sociodemographic_var is provided
    grouping_columns = ['origen', 'destino']

    # Group by the determined columns and sum the 'viajes' column
    trip_counts = df.groupby(grouping_columns)['viajes'].sum().reset_index(name='trip_count')
    return trip_counts

def build_distance_count(df): # FIXED, AND NEW
    '''I am obtaining the km per trip! REVIEW'''
    # Group by 'origen' and 'destino' and calculate the sum of 'viajes_km' and 'viajes'
    trip_counts = df.groupby(['origen', 'destino']).agg({
        'viajes_km': 'sum',
        'viajes': 'sum'
    }).reset_index()
    
    # Calculate the ratio and add it as a new column
    trip_counts['distance_per_trip'] = trip_counts['viajes_km'] / trip_counts['viajes']
    
    return trip_counts

def get_district_names(trip_counts):
    # get names of districts
    trip_counts = trip_counts.merge(district_mapping[['ID', 'name_2']], how='left', left_on='origen', right_on='ID')
    trip_counts = trip_counts.rename(columns={'name_2': 'origin'})
    trip_counts = trip_counts.merge(district_mapping[['ID', 'name_2']], how='left', left_on='destino', right_on='ID')
    trip_counts = trip_counts.rename(columns={'name_2': 'destination'})

    # drop extra columns
    trip_counts = trip_counts.drop(columns=['ID_x', 'ID_y'])

    return trip_counts

def normalize_by_pop(trip_counts, population_df):
    trip_counts = trip_counts.merge(population_df, left_on='origen', right_on='ID', how='left')
    # Normalize trip counts by population of the origin district
    trip_counts['normalized_trip_count'] = trip_counts['trip_count'] / trip_counts['Population']
    trip_counts.drop(columns=['ID','Population'], inplace=True)  # removing extra columns
    return trip_counts

def get_income_data(trip_counts, income, income_var_1, income_var_2):
    # get origin incomes
    trip_counts = trip_counts.merge(
    income[['ID', income_var_1, income_var_2]], 
    left_on='origen', 
    right_on='ID', 
    how='left'
)
    # rename
    trip_counts.rename(columns={income_var_1: f'Origin {income_var_1}'}, inplace=True)
    trip_counts.rename(columns={income_var_2: f'Origin {income_var_2}'}, inplace=True)

    # drop extra columns
    trip_counts.drop(columns=['ID'], inplace=True)

    # get destination incomes
    trip_counts = trip_counts.merge(
        income[['ID', income_var_1, income_var_2]], 
        left_on='destino', 
        right_on='ID', 
        how='left'
    )

    # rename columns
    trip_counts.rename(columns={income_var_1: f'Destination {income_var_1}'}, inplace=True)
    trip_counts.rename(columns={income_var_2: f'Destination {income_var_2}'}, inplace=True)
    # drop extra columns
    trip_counts.drop(columns=['ID', 'origen', 'destino'], inplace=True)

    return trip_counts

def add_quantiles(trip_counts, income_var, n_quantiles=6):
    trip_counts[f'income decile origin {income_var}'] = pd.qcut(trip_counts[f'Origin {income_var}'], n_quantiles, labels=False, duplicates='drop')
    trip_counts[f'income decile destination {income_var}'] = pd.qcut(trip_counts[f'Destination {income_var}'], n_quantiles, labels=False, duplicates='drop') 
    return trip_counts

def get_share_trips(all_trips_df, quantiles_df):
    return quantiles_df['normalized_trip_count'].sum() / all_trips_df.normalized_trip_count.sum() * 100

def plot_distances(low_df, high_df, variable):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Combine data into a single DataFrame for easier plotting
    low_df['Income Group'] = f'Low {variable}'
    high_df['Income Group'] = f'High {variable}'
    combined_df = pd.concat([low_df, high_df])

    # Use a strip plot to represent the distances
    sns.stripplot(
        x='distance_per_trip', 
        y='Income Group', 
        data=combined_df, 
        jitter=True, 
        alpha=0.5, 
        palette={f'Low {variable}': 'green', f'High {variable}': 'indigo'},
        ax=ax  # Pass the axis to Seaborn
    )

    # Add mean lines for each group
    low_mean = low_df['distance_per_trip'].mean()
    high_mean = high_df['distance_per_trip'].mean()

    longest_trip = combined_df.loc[combined_df['distance_per_trip'].idxmax()]
    origin = longest_trip['origin']
    destination = longest_trip['destination']
    distance = longest_trip['distance_per_trip']

    longest_trip_high = high_df.loc[high_df['distance_per_trip'].idxmax()]
    origin_high = longest_trip_high['origin']
    destination_high = longest_trip_high['destination']
    distance_high = longest_trip_high['distance_per_trip']

    ax.annotate(
        f'{origin_high} to {destination_high}: {distance_high:.2f} km',
        xy=(distance_high, 1),  # Adjust the Y-coordinate to align with High group
        xytext=(distance_high + 0.1, 1.5),  # Adjust the label position
        fontsize=12,
        color='black',
        ha='left'
    )

    ax.annotate(
        f'{origin} to {destination}: {distance:.2f} km',
        xy=(distance, -0.1),  # Position text close to the dot
        xytext=(distance + 0.1, 0.5),  # Adjust label position
        fontsize=12,
        color='black',
        ha='left'
    )

    ax.axvline(low_mean, color='green', linestyle='--', label=f'Low {variable} Mean: {low_mean:.2f}')
    ax.axvline(high_mean, color='indigo', linestyle='--', label=f'High {variable} Mean: {high_mean:.2f}')

    ax.set_title(f'Distance Per Trip by {variable} Group')
    ax.set_xlabel(r'$D_{ab}$')
    ax.set_ylabel(f'{variable} Group')
    ax.legend()
    fig.tight_layout()

    return fig
