import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


def plot_metrics(n_d_list, n_n_list, n_e_list, a_d_list, filename='network_metrics.pdf'):
    years = [i for i in range(2010, 2026)]
    milestones = [2012, 2016, 2020, 2024]  # Anos marcantes

    # Cria uma figura com 4 subplots
    fig, axs = plt.subplots(4, 1, figsize=(10, 12))
    fig.suptitle('Network Metrics Evolution (2010-2025)', fontsize=14, y=1.02)
    fig.tight_layout(pad=4.0)

    # Configurações comuns para as linhas verticais
    line_style = {'linestyle': ':', 'color': 'red', 'alpha': 0.7, 'linewidth': 2}

    # Gráfico 1: Number of Nodes
    axs[0].plot(years, n_n_list)
    for year in milestones:
        axs[0].axvline(x=year, **line_style)
    axs[0].grid()
    axs[0].set_xlabel("Years")
    axs[0].set_ylabel("Number of Nodes")

    # Gráfico 2: Number of Edges
    axs[1].plot(years, n_e_list)
    for year in milestones:
        axs[1].axvline(x=year, **line_style)
    axs[1].grid()
    axs[1].set_xlabel("Years")
    axs[1].set_ylabel("Number of Edges")

    # Gráfico 3: Average Degree
    axs[2].plot(years, a_d_list)
    for year in milestones:
        axs[2].axvline(x=year, **line_style)
    axs[2].grid()
    axs[2].set_xlabel("Years")
    axs[2].set_ylabel("Average Degree")

    # Gráfico 4: Network Density
    axs[3].plot(years, n_d_list)
    for year in milestones:
        axs[3].axvline(x=year, **line_style)
    axs[3].grid()
    axs[3].set_xlabel("Years")
    axs[3].set_ylabel("Network Density")

    # Salva em PDF
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    print(f"Gráficos salvos como {filename}")

    plt.show()

def plot_degree_distribution(d_d_list):
    """
    Plots, displays and saves degree distribution histograms for each year's data as PDF files.

    Parameters:
    d_d_list (list): List of dictionaries containing degree distributions for each year
    """
    for i in range(len(d_d_list)):
        data_dict = dict(d_d_list[i])

        # Prepare data
        values = list(data_dict.keys())
        counts = list(data_dict.values())

        # Create figure with larger size
        plt.figure(figsize=(14, 7))
        bars = plt.bar(values, counts, color='skyblue', edgecolor='navy', alpha=0.8, width=0.8)

        # Customize plot appearance
        plt.title(f'Co-authorship Degree Distribution - 20{10+i}', fontsize=16, pad=20, fontweight='bold')
        plt.xlabel('Number of co-authorships', fontsize=14, labelpad=10)
        plt.ylabel('Frequency', fontsize=14, labelpad=10)

        # Grid and tick customization
        plt.grid(axis='y', alpha=0.4, linestyle='--')
        plt.xticks(fontsize=12, rotation=45)
        plt.yticks(fontsize=12)

        # Adjust layout
        plt.tight_layout()

        # Save as high-quality PDF
        pdf_filename = f'degree_distribution_20{10+i}.pdf'
        plt.savefig(pdf_filename, format='pdf', dpi=300, bbox_inches='tight')
        print(f"Graph saved as {pdf_filename}")

        # Display the plot
        plt.show()

        # Clear the figure for next iteration
        plt.clf()
        plt.close()

# Example usage:
# plot_degree_distribution(your_degree_distribution_list)


def plot_ridgeline_chart(d_d_list):
    """
    Creates and saves a Ridgeline Chart with probability density functions (KDE) for each year's data.

    Parameters:
    d_d_list (list): List of dictionaries containing degree distributions for each year
    """
    plt.figure(figsize=(12, 8))

    # Create a list of years for labeling
    years = [f"20{10+i}" for i in range(len(d_d_list))]

    # Create a grid for KDE evaluation
    x_grid = np.linspace(0, max(max(d.keys()) for d in d_d_list if d) + 5, 500)

    # Create a list to store all KDEs
    kde_results = []

    # Calculate KDE for each year
    for i, data_dict in enumerate(d_d_list):
        if not data_dict:
            continue

        # Expand the data points according to their counts
        values = []
        for val, count in data_dict.items():
            values.extend([val] * count)

        # Calculate KDE
        kde = gaussian_kde(values)
        kde_results.append(kde(x_grid))

    # Create Ridgeline plot
    n_years = len(kde_results)
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, n_years))

    fig, axes = plt.subplots(n_years, 1, figsize=(10, 0.8 * n_years),
                           sharex=True, sharey=True)
    plt.subplots_adjust(hspace=-0.5)

    for i, (ax, year, color, kde) in enumerate(zip(axes, years, colors, kde_results)):
        ax.fill_between(x_grid, kde, color=color, alpha=0.6)
        ax.plot(x_grid, kde, color='black', alpha=0.6, linewidth=0.5)

        # Set year label
        ax.text(0.95, 0.8, year, transform=ax.transAxes,
                ha='right', va='center', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

        # Remove borders and ticks
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='both', which='both', length=0)
        ax.set_yticks([])

    # Set common labels
    fig.text(0.5, 0.02, 'Number of co-authorships', ha='center', fontsize=12)
    fig.text(0.02, 0.5, 'Year', va='center', rotation='vertical', fontsize=12)
    fig.suptitle('Evolution of Co-authorship Degree Distribution', y=0.95, fontsize=14)

    # Save as PDF
    plt.savefig('ridgeline_chart.pdf', format='pdf', dpi=300, bbox_inches='tight')
    print("Ridgeline chart saved as 'ridgeline_chart.pdf'")

    plt.show()