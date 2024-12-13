import config as cfg
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

# ASSORTATIVITY_MATRIX.PY -----------------------------------------------------------------------

def plot_assortativity_matrix(assortativity_matrix, name_of_figure, pearson=None, p_value=None, cmap='viridis', annot=True):
    """
    Plots the assortativity matrix of trips between deciles.
    Parameters:
    - assortativity_matrix (pd.DataFrame): The assortativity matrix to plot.
    - time_of_study (str): Description of the study period (e.g., "Normal Week").
    - var_of_interest (str): The variable of interest for the matrix (e.g., "Renta bruta media por hogar").
    - cmap (str): Color map to use for the heatmap.
    - save_fig (bool): Whether to save the figure to file.
    - fig_path (str or Path): Path to save the figure if save_fig is True.
    Returns:
    - None
    """
    title = f'Assortativity Matrix of Trips Between Deciles\n'
    title += f'{cfg.time_of_study}\nVariable: {cfg.var_of_interest.lower()}'
    if pearson is not None:
        title += f'\nPearson: {pearson:.4f}'
    if p_value is not None:
        title += f'\np-value: {p_value:.4f}'
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        assortativity_matrix, 
        annot=annot, 
        cmap=cmap, 
        cbar_kws={'label': 'Number of Trips'}, 
        fmt=".2f"
    )
    plt.title(title)
    plt.xlabel('Destination District SES')
    plt.ylabel('Home District SES')
    if cfg.SAVE_FIGURES:
        plt.savefig(cfg.FIGURES_PATH / f'{name_of_figure}', dpi=300, bbox_inches='tight')
        print(f"Figure saved at: {cfg.FIGURES_PATH}")
    plt.show()

def calculate_assortativity_coefficient(normalized_matrix): 
    # FIXME: Review this procedure! it might be very wrong, I am unsure about the math behind it
    # Flatten the matrix and extract indices
    i_indices, j_indices = np.meshgrid(np.arange(normalized_matrix.shape[0]), 
                                    np.arange(normalized_matrix.shape[1]), 
                                    indexing='ij')

    # Flatten the matrix and indices
    i_indices_flat = i_indices.flatten()
    j_indices_flat = j_indices.flatten()
    matrix_flat = normalized_matrix.values.flatten()

    # Calculate Pearson correlation coefficient
    rho, p_value = pearsonr(i_indices_flat * j_indices_flat, matrix_flat)
    return rho, p_value
