import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

def plotar_rede_comunidades(G, mapa_comunidade, pasta_destino="."):
    """
    Gera a visualização gráfica da rede e RETORNA AS POSIÇÕES.
    Agora salva na pasta especificada.
    """
    nome_arquivo = "nba_rede_comunidades.png"
    print(f"\nGerando imagem da rede global ({nome_arquivo})...")
    
    plt.figure(figsize=(12, 12))
    
    # Layout Fruchterman-Reingold
    pos = nx.spring_layout(G, k=0.15, seed=42) 
    
    cmap = plt.cm.tab10 
    cores_nos = [cmap(mapa_comunidade[node] % 10) for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_size=60, node_color=cores_nos, alpha=0.9)
    nx.draw_networkx_edges(G, pos, alpha=0.1, edge_color='gray')
    
    ids_unicos = sorted(list(set(mapa_comunidade.values())))
    legend_elements = []
    for com_id in ids_unicos:
        cor = cmap(com_id % 10)
        elem = Line2D([0], [0], marker='o', color='w', label=f'Comunidade {com_id}',
                      markerfacecolor=cor, markersize=10)
        legend_elements.append(elem)
    
    plt.legend(handles=legend_elements, loc='upper right', title="Arquétipos", fontsize=10)
    plt.title("Rede de Comunidades da NBA (Similaridade de Estilo)", fontsize=16)
    plt.axis('off')
    
    # Salva na pasta correta
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Imagem global salva em: {caminho_completo}")
    
    return pos

# ... (As outras funções: plotar_zoom_jogador e plotar_radar continuam iguais)
def plotar_zoom_jogador(G, mapa_comunidade, pos, nome_alvo, pasta_destino=".", raio_zoom=0.45):
    if nome_alvo not in G.nodes():
        print(f"[AVISO] Jogador '{nome_alvo}' não encontrado no grafo para zoom.")
        return

    print(f"   -> Gerando Zoom de Rede para: {nome_alvo}...")
    plt.figure(figsize=(10, 10))
    
    cmap = plt.cm.tab10 
    cores_nos = [cmap(mapa_comunidade[node] % 10) for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_size=150, node_color=cores_nos, alpha=0.8)
    nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='gray')
    
    x, y = pos[nome_alvo]
    plt.scatter([x], [y], s=400, facecolors='none', edgecolors='black', linewidth=2, zorder=10)
    
    plt.text(x, y + 0.015, s=nome_alvo, fontsize=14, fontweight='bold', ha='center', 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.3'),
             zorder=20)

    ids_unicos = sorted(list(set(mapa_comunidade.values())))
    legend_elements = []
    for com_id in ids_unicos:
        cor = cmap(com_id % 10)
        elem = Line2D([0], [0], marker='o', color='w', label=f'Comunidade {com_id}',
                      markerfacecolor=cor, markersize=10)
        legend_elements.append(elem)
    
    plt.legend(handles=legend_elements, loc='upper right', title="Arquétipos", fontsize=10)

    plt.xlim(x - raio_zoom, x + raio_zoom)
    plt.ylim(y - raio_zoom, y + raio_zoom)
    
    plt.title(f"Zoom Local: Vizinhança de {nome_alvo}", fontsize=16)
    plt.axis('off')
    
    nome_limpo = nome_alvo.replace(" ", "_")
    nome_arquivo = f"zoom_rede_{nome_limpo}.png"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
    
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()

def plotar_radar(df, jogador1, jogador2, cols_radar, pasta_destino="."):
    scaler_plot = MinMaxScaler()
    cols_validas = [c for c in cols_radar if c in df.columns]
    df_norm = df[cols_validas].copy().astype(float)
    df_norm[:] = scaler_plot.fit_transform(df_norm)

    try:
        v1 = df_norm.loc[df['NAME'] == jogador1].iloc[0].values
        v2 = df_norm.loc[df['NAME'] == jogador2].iloc[0].values
    except IndexError: return

    num_vars = len(cols_validas)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    v1 = np.concatenate((v1, [v1[0]]))
    v2 = np.concatenate((v2, [v2[0]]))
    angles += [angles[0]]
    
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.plot(angles, v1, color='#1f77b4', linewidth=2, label=jogador1)
    ax.fill(angles, v1, color='#1f77b4', alpha=0.25)
    ax.plot(angles, v2, color='#ff7f0e', linewidth=2, label=jogador2)
    ax.fill(angles, v2, color='#ff7f0e', alpha=0.25)
    
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cols_validas, size=8)
    plt.title(f"{jogador1} vs {jogador2}", y=1.08, size=11, weight='bold')
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
    
    nome_arquivo = f"compare_{jogador1}_vs_{jogador2}.png".replace(" ", "_")
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
    plt.savefig(caminho_completo, bbox_inches='tight', dpi=150)
    plt.close()