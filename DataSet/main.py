import pandas as pd
import os

url = 'https://www.nbastuffer.com/2024-2025-nba-player-stats/'
nome_arquivo_saida = 'filtered_per_36_stats.csv'
pasta_script = os.path.dirname(os.path.abspath(__file__))
caminho_saida = os.path.join(pasta_script, nome_arquivo_saida)

print(f"Lendo dados de: {url}")

try:
    
    tabelas = pd.read_html(url)
    
    if len(tabelas) < 2:
        raise IndexError("Não foram encontradas tabelas suficientes. Verifique o layout do site.")
    
    df = tabelas[1]
    print(f"Tabela da Temporada Regular carregada. Total de jogadores: {len(df)}")

    cols_check = ['GP', 'MpG']
    for col in cols_check:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df_filtered = df[(df['GP'] >= 41) & (df['MpG'] >= 20)].copy()
    print(f"Jogadores após filtragem (GP>=41, MpG>=20): {len(df_filtered)}")

    stats_replace = {
        'PpG': 'PpG_Per36', 'RpG': 'RpG_Per36', 'ApG': 'ApG_Per36',
        'SpG': 'SpG_Per36', 'BpG': 'BpG_Per36', 'TOpG': 'TOpG_Per36'
    }

    stats_add = {
        'FTA': 'FTA_Per36', '2PA': '2PA_Per36', '3PA': '3PA_Per36'
    }

    for col_orig, col_dest in stats_replace.items():
        if col_orig in df_filtered.columns:
            
            df_filtered[col_orig] = pd.to_numeric(df_filtered[col_orig], errors='coerce')
            df_filtered[col_dest] = ((df_filtered[col_orig] / df_filtered['MpG']) * 36).round(1)
            df_filtered.drop(columns=[col_orig], inplace=True)

    
    for col_orig, col_dest in stats_add.items():
        if col_orig in df_filtered.columns:
            
            df_filtered[col_orig] = pd.to_numeric(df_filtered[col_orig], errors='coerce')
            stat_pg = df_filtered[col_orig] / df_filtered['GP']
            df_filtered[col_dest] = ((stat_pg / df_filtered['MpG']) * 36).round(1)

    df_filtered.to_csv(caminho_saida, index=False)
    print(f"Arquivo salvo em: {caminho_saida}")

except Exception as e:
    print(f"\nErro Crítico: {e}")