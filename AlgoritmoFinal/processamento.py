import pandas as pd
import networkx as nx
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from networkx.algorithms.community import greedy_modularity_communities

def salvar_csv_listagem(df, mapa_comunidade, nome_arquivo="nba_comunidades_listagem.csv"):
    """Gera CSV com todos os jogadores organizados por comunidade."""
    print(f"\n--- Gerando Listagem de Jogadores: {nome_arquivo} ---")
    df_export = df.copy()
    df_export['Community_ID'] = df_export['NAME'].map(mapa_comunidade)
    df_export = df_export.dropna(subset=['Community_ID'])
    df_export['Community_ID'] = df_export['Community_ID'].astype(int)
    
    if 'USG%' in df_export.columns:
        df_export = df_export.sort_values(by=['Community_ID', 'USG%'], ascending=[True, False])
    else:
        df_export = df_export.sort_values(by=['Community_ID', 'NAME'], ascending=[True, True])
    
    cols_base = ['Community_ID', 'NAME', 'TEAM', 'POS', 'AGE']
    cols_stats = ['PpG_Per36', 'USG%', 'RpG_Per36', 'ApG_Per36', '3PA_Per36', 'BpG_Per36']
    cols_final = cols_base + [c for c in cols_stats if c in df_export.columns]
    
    df_export[cols_final].to_csv(nome_arquivo, index=False)
    print("Arquivo de listagem salvo.")

def salvar_csv_medias(df, mapa_comunidade, cols_features, nome_arquivo="nba_comunidades_medias.csv"):
    """Gera CSV com as MÉDIAS estatísticas de cada comunidade."""
    print(f"\n--- Gerando Relatório de Médias: {nome_arquivo} ---")
    
    df_temp = df.copy()
    df_temp['Community_ID'] = df_temp['NAME'].map(mapa_comunidade)
    df_temp = df_temp.dropna(subset=['Community_ID'])
    df_temp['Community_ID'] = df_temp['Community_ID'].astype(int)
    
    medias = df_temp.groupby('Community_ID')[cols_features].mean()
    contagem = df_temp['Community_ID'].value_counts().sort_index()
    medias.insert(0, 'Count_Players', contagem)
    
    medias = medias.round(2)
    medias.to_csv(nome_arquivo)
    print("Arquivo de médias salvo! (Centróides das comunidades)")

def gerar_comunidades(df, cols_features):
    """Cria o grafo e detecta comunidades. NÃO PLOTA NADA AQUI (Separation of Concerns)."""
    print("--- 1. Analisando Estrutura da Liga (Grafos) ---")
    data_comm = df.dropna(subset=cols_features).reset_index(drop=True)
    scaler = StandardScaler()
    X_comm = scaler.fit_transform(data_comm[cols_features])
    
    k_vizinhos = 6 
    
    knn_graph = NearestNeighbors(n_neighbors=k_vizinhos + 1, metric='euclidean') 
    knn_graph.fit(X_comm)
    indices = knn_graph.kneighbors(X_comm, return_distance=False)

    G = nx.Graph()
    for i in range(len(data_comm)):
        nome_origem = data_comm.iloc[i]['NAME']
        G.add_node(nome_origem)
        for j in range(1, k_vizinhos + 1):
            idx_vizinho = indices[i, j]
            nome_destino = data_comm.iloc[idx_vizinho]['NAME']
            G.add_edge(nome_origem, nome_destino)

    print("Detectando comunidades via Modularidade...")
    try:
        comunidades = list(greedy_modularity_communities(G))
    except:
        return {}, nx.Graph()

    mapa_comunidade = {}
    for id_com, lista_jogadores in enumerate(comunidades):
        for jogador in lista_jogadores:
            mapa_comunidade[jogador] = id_com
    
    return mapa_comunidade, G

def preparar_scouting(df, cols_scouting):
    """Treina o modelo de busca individual (KNN)."""
    print("\n--- 2. Treinando Motor de Scouting ---")
    X = df[cols_scouting].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = NearestNeighbors(n_neighbors=20, algorithm='ball_tree', metric='euclidean')
    model.fit(X_scaled)
    return model, X_scaled, scaler