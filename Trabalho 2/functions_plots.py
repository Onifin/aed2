import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde



def plot_metrics(n_d_list, n_n_list, n_e_list, a_d_list, filename='network_metrics.pdf'):
    """
    Plota a evolução de métricas de redes científicas de 2010 a 2025 e salva como PDF.

    Parâmetros:
    - n_d_list: Lista com os valores de densidade da rede.
    - n_n_list: Lista com os números de nós.
    - n_e_list: Lista com os números de arestas.
    - a_d_list: Lista com os graus médios.
    - filename: Nome do arquivo de saída em PDF.
    """
    years = list(range(2010, 2026))
    milestones = [2012, 2016, 2020, 2024]
    metrics = [
        ("Number of Nodes", n_n_list),
        ("Number of Edges", n_e_list),
        ("Average Degree", a_d_list),
        ("Network Density", n_d_list)
    ]

    # Configurações do gráfico
    fig, axs = plt.subplots(len(metrics), 1, figsize=(10, 15))
    #fig.suptitle('Network Metrics Evolution (2010–2025)', fontsize=16, y=1.02)
    fig.tight_layout(pad=4.0)

    line_style = {'linestyle': ':', 'color': 'red', 'alpha': 0.7, 'linewidth': 2}

    for i, (label, values) in enumerate(metrics):
        ax = axs[i]
        ax.plot(years, values, marker='o', label=label)
        ax.set_xlabel("Year")
        ax.set_ylabel(label)
        ax.grid(True)
        for year in milestones:
            ax.axvline(x=year, **line_style)
        ax.legend()

    # Salva o gráfico
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    print(f"Gráficos salvos como {filename}")
    plt.show()





def plot_degree_distribution_grouped(d_d_list):
    """
    Plots, displays and saves grouped degree distribution histograms (4 per PDF page),
    each with a specific distinct color.
    
    Parameters:
    d_d_list (list): List of dictionaries containing degree distributions for each year
    """
    graphs_per_pdf = 4
    num_graphs = len(d_d_list)
    num_pdfs = (num_graphs + graphs_per_pdf - 1) // graphs_per_pdf

    # Lista de cores específicas
    colors = ['skyblue', 'lightcoral', 'mediumseagreen', 'plum', 'gold', 'lightsalmon', 'deepskyblue', 'khaki']

    for pdf_index in range(num_pdfs):
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        axes = axes.flatten()

        for i in range(graphs_per_pdf):
            data_index = pdf_index * graphs_per_pdf + i
            if data_index >= num_graphs:
                axes[i].axis('off')
                continue

            data_dict = dict(d_d_list[data_index])
            values = list(data_dict.keys())
            counts = list(data_dict.values())

            # Cor específica para o gráfico atual, com fallback em loop se necessário
            color = colors[data_index % len(colors)]

            axes[i].bar(values, counts, color=color, edgecolor='black', alpha=0.85, width=0.8)
            axes[i].set_title(f'Co-authorship Degree Distribution - 20{10 + data_index}', fontsize=14, fontweight='bold')
            axes[i].set_xlabel('Number of co-authorships', fontsize=12)
            axes[i].set_ylabel('Frequency', fontsize=12)
            axes[i].grid(axis='y', alpha=0.4, linestyle='--')

            for label in axes[i].get_xticklabels():
                label.set_rotation(90)
                label.set_ha('center')

        plt.tight_layout()
        plt.show()  # Mostra o gráfico antes de salvar
        pdf_filename = f'degree_distribution_group_{pdf_index + 1}.pdf'
        plt.savefig(pdf_filename, format='pdf', dpi=300, bbox_inches='tight')
        print(f"PDF salvo: {pdf_filename}")
        plt.close(fig)




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