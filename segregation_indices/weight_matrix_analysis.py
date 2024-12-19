
import config as cfg
import pandas as pd 
import geopandas as gpd
import numpy as np
# for plotting
import seaborn as sns
import contextily as ctx
import matplotlib.pyplot as plt
# for Moran's I
from libpysal.weights import Queen, KNN, Rook
from esda.moran import Moran, Moran_Local
from libpysal.weights import lag_spatial

'''
Great source: https://geographicdata.science/book/notebooks/07_local_autocorrelation.html
'''

# READ DATA ------------------------------------------------------------------------------------------------------

merged = gpd.read_file(cfg.INCOME_DATA / 'geometries_and_income.geojson') 
gdf = merged[['ID', 'geometry'] + cfg.INCOME_VARS_OF_INTEREST] # here I select the variable of interest
gdf = gdf.reset_index(drop=True) # reset the index to calculate the weights with no problems

# BUILD WEIGHT MATRICES --------------------------------------------------------------------------------------------------
queen = Queen.from_dataframe(gdf) # queen weights
queen.transform = 'r' # standardizing
rook = Rook.from_dataframe(gdf) # rook weights
rook.transform = 'r' # standardizing

# PLOTS AND STATS --------------------------------------------------------------------------------------------------

plt.spy( queen.full()[0], markersize=1)
plt.title("Spatial Weights Matrix (Queen Contiguity)")
plt.show()

plt.spy(rook.full()[0], markersize=1)
plt.title("Spatial Weights Matrix (Rook Contiguity)")
plt.show()

for key, neighbors in queen.neighbors.items():
    print(f"Queen Matrix --> Polygon {key} has neighbors: {neighbors}")

for key, neighbors in rook.neighbors.items():
    print(f"Rook Matrix --> Polygon {key} has neighbors: {neighbors}")

print(f"Number of polygons: {queen.n}")
print(f"Average neighbors in Queen matrix: {sum(len(v) for v in queen.neighbors.values()) / queen.n:.2f}")
print(f"Average neighbors Rook matrix: {sum(len(v) for v in rook.neighbors.values()) / rook.n:.2f}")

fig, ax = plt.subplots(figsize=(8, 6))

pd.Series(queen.cardinalities).plot.hist(
    ax=ax, bins=10, alpha=0.5, color="orange", label="Queen"
)

pd.Series(rook.cardinalities).plot.hist(
    ax=ax, bins=10, alpha=0.5, color="red", label="Rook"
)

ax.set_xlabel('Cardinality')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of Cardinalities: Queen vs Rook Weight Matrices')
ax.legend()
if cfg.SAVE_FIGURES:
    plt.savefig(cfg.FIGURES_PATH / f'weights_cardinalities.png', dpi=300, bbox_inches='tight')
plt.show()
