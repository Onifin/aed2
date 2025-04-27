import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.stats import gaussian_kde

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.collections import PolyCollection
import seaborn as sns



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

    plt.savefig(filename, bbox_inches='tight', dpi=300)
    print(f"Gráficos salvos como {filename}")
    plt.show()


def plot_degree_distribution_grouped(d_d_list):
    graphs_per_pdf = 4
    num_graphs = len(d_d_list)
    num_pdfs = (num_graphs + graphs_per_pdf - 1) // graphs_per_pdf

    colors = ['red', 'green', 'yellow', 'blue', 'brown', 'cyan', 'pink', 'purple']

    for pdf_index in range(num_pdfs):
        fig, axes = plt.subplots(2, 2, figsize=(16, 10), constrained_layout=True)
        axes = axes.flatten()

        for i in range(graphs_per_pdf):
            data_index = pdf_index * graphs_per_pdf + i
            if data_index >= num_graphs:
                axes[i].axis('off')
                continue

            data_dict = dict(d_d_list[data_index])
            values = list(data_dict.keys())
            counts = list(data_dict.values())

            color = colors[data_index % len(colors)]

            axes[i].bar(values, counts, color=color, edgecolor='black', alpha=0.85, width=0.8)
            axes[i].set_title(f'Co-authorship Degree Distribution - 20{10 + data_index}', 
                              fontsize=14, fontweight='bold')
            axes[i].set_xlabel('Number of co-authorships', fontsize=12, labelpad=10)
            axes[i].set_ylabel('Frequency', fontsize=12)
            axes[i].grid(axis='y', alpha=0.4, linestyle='--')

            for label in axes[i].get_xticklabels():
                label.set_rotation(90)
                label.set_ha('center')

        plt.show()
        pdf_filename = f'degree_distribution_group_{pdf_index + 1}.pdf'
        plt.savefig(pdf_filename, format='pdf', dpi=300, bbox_inches='tight')
        print(f"PDF salvo: {pdf_filename}")
        plt.close(fig)


def plot_ridgeline(d_d_list, n_e_list, years=None, figsize=(12, 8),
                   overlap=0.7, palette="viridis", alpha=0.8,
                   title="Distribuição de Frequências por Ano",
                   xlabel="Valor", ylabel="Ano"):
    """
    Plota um gráfico ridgeline (joyplot) para dados de frequência por ano,
    colorindo cada curva de acordo com a média de arestas de cada ano.

    Parâmetros:
    - d_d_list: lista de dicionários de frequências. Cada dicionário corresponde a um ano,
                e deve ter o formato {valor: frequência, ...}
    - n_e_list: lista (ou iterável) com a média de arestas para cada ano,
                na mesma ordem de d_d_list
    - years: lista de anos correspondentes aos dados (default: 2010 a 2025)
    - figsize: tamanho da figura
    - overlap: grau de sobreposição entre as curvas (0 a 1)
    - palette: paleta de cores para o colormap
    - alpha: transparência das curvas
    - title: título do gráfico
    - xlabel: legenda do eixo x
    - ylabel: legenda do eixo y
    """
    if years is None:
        years = list(range(2010, 2026))

    if len(d_d_list) != len(n_e_list) or len(d_d_list) != len(years):
        raise ValueError("Os comprimentos de d_d_list, n_e_list e years devem ser iguais")

    dfs = []
    for i, d in enumerate(d_d_list):
        if d: 
            df = pd.DataFrame(list(d.items()), columns=['valor', 'frequencia'])
            df['ano'] = years[i]
            df['media_arestas'] = n_e_list[i]
            dfs.append(df)

    if not dfs:
        raise ValueError("Nenhum dado válido encontrado para plotar")

    data = pd.concat(dfs, ignore_index=True)

    # Encontrar o valor mínimo e máximo para todos os dados
    x_min = data['valor'].min()
    x_max = data['valor'].max()

    fig, ax = plt.subplots(figsize=figsize, facecolor='white')

    norm = mcolors.Normalize(vmin=min(n_e_list), vmax=max(n_e_list))
    cmap = plt.get_cmap(palette)

    for i, year in enumerate(years):
        year_data = data[data['ano'] == year]

        if not year_data.empty:
            x_values = year_data['valor'].values
            y_values = year_data['frequencia'].values

            idx = np.argsort(x_values)
            x_values = x_values[idx]
            y_values = y_values[idx]

            x = np.append(np.append([x_min], x_values), [x_max])
            y = np.append(np.append([0], y_values), [0])

            y = y / y.max() if y.max() > 0 else y

            offset = i * (1.0 - overlap)

            xy = np.column_stack([x, offset + y])

            color = cmap(norm(n_e_list[i]))

            poly = plt.fill(xy[:, 0], xy[:, 1], alpha=alpha, color=color, edgecolor='k', linewidth=0.5)

            plt.axhline(y=offset, color='gray', linestyle='--', alpha=0.3)

    ax.set_yticks([i * (1.0 - overlap) for i in range(len(years))])
    ax.set_yticklabels(years)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, label='Média de Arestas')

    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xlim(x_min, 50)
    plt.ylim(-0.5, len(years) * (1.0 - overlap) + 0.5)

    plt.tight_layout()

    pdf_filename = 'distribuicao_frequencias.pdf'

    plt.savefig(pdf_filename, format='pdf', dpi=300, bbox_inches='tight')
    print(f"PDF salvo: {pdf_filename}")

    #plt.show()  # Adiciona esta linha para exibir o gráfico na aplicação
    plt.close(fig)

    return fig, ax