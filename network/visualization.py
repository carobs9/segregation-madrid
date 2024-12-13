import networkx as nx
import geopandas as gpd
import config as cfg
from utils import *
import matplotlib.cm as cm
from pyvis.network import Network

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

all_viajes = pd.read_csv(cfg.MOBILITY_DATA / f'VIAJES/{file_name}', thousands='.', decimal=',') #df of interest
filtered_df = all_viajes.loc[(all_viajes['actividad_origen'] == 'casa')]
income = gpd.read_file('/Users/caro/Desktop/thesis_project/segregation_indices/data/processed/geometries_and_income.geojson')
trip_counts = pd.read_csv(f'/Users/caro/Desktop/thesis_project/trip_analysis/outputs/{cfg.type_of_study}_normalized_trip_count.csv')

gdf = gpd.read_file(cfg.ZONIFICACION_DATA / 'distritos/madrid_gdf.geojson')  # for positions when plotting
gdf = gdf.to_crs(epsg=4326)

income['Gini Index Scaled'] = income['Gini Index'] # ** 2.5
var_of_interest = 'Gini Index Scaled' # or 'Gini Index Scaled' or Median income per consumption unit

district_counts = filtered_df['origen'].value_counts().reset_index()
district_counts.columns = ['ID', 'Population']

G = define_graph(trip_counts, remove_weak_edges=False, threshold=0.2, standardise=True)
G = update_node_sizes(G, income, var_of_interest)
edge_widths = set_art(G, 0.1)
positions = get_positions(gdf) 
positions = {k: tuple(v) for k, v in positions.items()}
nx.set_node_attributes(G, positions, 'pos')

id_to_name = district_mapping.set_index('ID')['name_2'].to_dict()
G = nx.relabel_nodes(G, id_to_name)

in_weights = check_in_weights(G)
out_weights = check_out_weights(G)

nx.set_node_attributes(G, in_weights, 'size')
edge_widths = set_art(G, 0.1)

# change node colors
norm = mcolors.Normalize(vmin=income['Median income per consumption unit'].min(),
                          vmax=income['Median income per consumption unit'].max())

# Create a colormap
colormap = cm.get_cmap('RdPu')  # Choose a colormap (e.g., 'RdYlBu')

# Map normalized values to colors
income['Color'] = income['Median income per consumption unit'].apply(lambda x: mcolors.to_hex(colormap(norm(x))))
color_map = income.set_index('ID')['Color'].to_dict()

net = Network(notebook=True, directed=True, cdn_resources='remote',height='800px', width="100%", bgcolor="#222222", font_color="white",filter_menu=True )

# Ensure physics is disabled to use fixed positions
net.toggle_physics(False)

# Add nodes with fixed positions, sizes, and colors
for node, pos in positions.items():
    # Get the color for the node from the mapping, default to a neutral color if not found
    color = color_map.get(node, '#cccccc')  # Use '#cccccc' as the default color
    
    # Add node with fixed positions
    net.add_node(
        node,
        x = pos[0],
        y = pos[1],
        label=id_to_name.get(node, str(node)),  # Use a friendly label
        size=in_weights.get(node, 500) * 10,  # Scale size
        color=color  # Assign color based on income
    )

# Ensure edges are added (if not already)
for u, v, data in G.edges(data=True):
    label = f"{data['weight']:.2f}"  # Customize the label format as needed
    net.add_edge(u, v, value=data['weight'], color='grey', label=label)

net.set_options("""
    var options = {
      "nodes": {
        "shape": "dot",
        "scaling": {
          "min": 1,
          "max": 15
        },
        "font": {
          "size": 30,
          "color": "white"
        }
      },
      "edges": {
        "scaling": {
          "min": 1,
          "max": 5
        },
        "font": {
          "size": 20,
          "color": "white",
          "face": "arial"
        },
        "arrows": {
          "to": { 
            "enabled": true
          },
          "scaleFactor": 0.001
        }
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -5000
        },
        "minVelocity": 0.5
      },
      "layout": {
        "improvedLayout": true
      },
      "interaction": {
        "hover": false
      },
      "manipulation": {
        "enabled": false
      },
      "background": {
        "color": "black"
      }
    }
""")
                

legend_html = """
<div style="position: absolute; top: 50%; right: 10px; transform: translateY(-50%);
            background-color: #222; color: white; padding: 15px; border-radius: 5px; text-align: center;">
  <h4 style="margin: 10px 0;">Income Scale</h4>
  <div style="position: relative; width: 20px; height: 200px; background: linear-gradient(to bottom, #67001f, #f4a582, #f7f4f9); margin: 20px auto;">
    <span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 12px;">High</span>
    <span style="position: absolute; bottom: -25px; left: 50%; transform: translateX(-50%); font-size: 12px;">Low</span>
  </div>
</div>
"""
# Add the legend HTML at the end of the body
net = net.replace("</body>", legend_html + "</body>")

with open("htmls/labels_02_threshold.html", "w") as f:
    f.write(net)