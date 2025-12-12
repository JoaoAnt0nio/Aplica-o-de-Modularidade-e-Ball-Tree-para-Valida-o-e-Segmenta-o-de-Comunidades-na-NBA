import pandas as pd
import os
import processamento
import visualizacao
import time 


COLS_COMMUNITIES = [
    'PpG_Per36', 'USG%', 'RpG_Per36', 'ApG_Per36', 'SpG_Per36', 
    'BpG_Per36', 'TOpG_Per36', '2PA_Per36', '3PA_Per36', 'FTA_Per36'
]

COLS_SCOUTING = [
    'USG%', 'RpG_Per36', 'ApG_Per36', 'SpG_Per36', 'BpG_Per36', 
    'FTA_Per36', '2PA_Per36', '3PA_Per36', 'PpG_Per36',
    'TS%', 'eFG%', 'TO%', '3P%', 'FT%', 'ORtg', 'DRtg'
]

ARQUIVO_DADOS = "filtered_per_36_stats.csv"

def main():
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"ERRO: {ARQUIVO_DADOS} não encontrado.")
        return

    df = pd.read_csv(ARQUIVO_DADOS)
    df = df.reset_index(drop=True) 
    
    pasta_relatorios = "Relatorios_Globais"
    if not os.path.exists(pasta_relatorios):
        os.makedirs(pasta_relatorios)
    
    caminho_csv_listagem = os.path.join(pasta_relatorios, "nba_comunidades_listagem.csv")
    caminho_csv_medias = os.path.join(pasta_relatorios, "nba_comunidades_medias.csv")

    mapa_comunidade, Grafo = processamento.gerar_comunidades(df, COLS_COMMUNITIES)
    
    processamento.salvar_csv_listagem(df, mapa_comunidade, nome_arquivo=caminho_csv_listagem)
    processamento.salvar_csv_medias(df, mapa_comunidade, COLS_COMMUNITIES, nome_arquivo=caminho_csv_medias)
    
    pos_layout = visualizacao.plotar_rede_comunidades(Grafo, mapa_comunidade, pasta_destino=pasta_relatorios)
    
    modelo_scouting, X_scaled, scaler_scout = processamento.preparar_scouting(df, COLS_SCOUTING)

    while True:
        print("\n" + "="*40)
        print("                 MENU       ")
        print("="*40)
        print("1 - Escolher jogador pelo nome")
        print("2 - Sortear jogador aleatório")
        print("3 - Sair")
        print("-" * 40)
        
        opcao = input("Digite sua opção: ").strip()

        target = ""
        idx_alvo = -1

        if opcao == '1':
            entrada_usuario = input("\nDigite o nome do jogador: ").strip()
            
            jogadores_encontrados = df[df['NAME'].str.lower() == entrada_usuario.lower()]
            
            if jogadores_encontrados.empty:
                print(f"\nJogador '{entrada_usuario}' não encontrado.")
                print("Dica: Verifique a ortografia ou se ele jogou minutos e partidas suficientes na temporada.")
                continue
            
            idx_alvo = jogadores_encontrados.index[0]
            target = jogadores_encontrados.iloc[0]['NAME']

        elif opcao == '2':
            time.sleep(1) 
            amostra = df.sample(1)
            idx_alvo = amostra.index[0]
            target = amostra.iloc[0]['NAME']
            print(f"\nJOGADOR SORTEADO: {target}")

        elif opcao == '3' or opcao.lower() == 'sair':
            break
        
        else:
            print("\nOpção inválida. Tente novamente.")
            continue

        
        stats_alvo = X_scaled[idx_alvo].reshape(1, -1)
        comunidade_alvo = mapa_comunidade.get(target, -1)
        
        print(f"\n>> ANÁLISE: {target} (Comunidade {comunidade_alvo})")
        
        dist, ind = modelo_scouting.kneighbors(stats_alvo, n_neighbors=6)
        
        nome_limpo = target.replace(" ", "_")
        pasta_raiz_jogador = nome_limpo  
        subpasta_comparacoes = os.path.join(pasta_raiz_jogador, f"Comparacoes_{nome_limpo}") 
        
        if not os.path.exists(subpasta_comparacoes):
            os.makedirs(subpasta_comparacoes)

        visualizacao.plotar_zoom_jogador(Grafo, mapa_comunidade, pos_layout, target, pasta_destino=pasta_raiz_jogador)
        
        print(f"\n>> TOP 5 SIMILARES (Resultados na pasta '{pasta_raiz_jogador}'):\n")
        print(f"{'RANK':<5} {'JOGADOR':<25} {'DIST':<10} {'STATUS'}")
        print("-" * 55)
        
        vizinhos_nomes = []
        for i in range(1, len(ind[0])): 
            idx_viz = ind[0][i]
            nome_viz = df.iloc[idx_viz]['NAME']
            comunidade_viz = mapa_comunidade.get(nome_viz, -1)
            vizinhos_nomes.append(nome_viz)
            
            status = " MATCH" if comunidade_viz == comunidade_alvo else " Híbrido"
            print(f"{i:<5} {nome_viz:<25} {dist[0][i]:.4f}       {status}")
        
        for v in vizinhos_nomes:
            visualizacao.plotar_radar(df, target, v, COLS_SCOUTING, pasta_destino=subpasta_comparacoes)
        
        print(f"\nRelatórios gerados em: {os.path.abspath(pasta_raiz_jogador)}")
        input("\nPressione Enter para voltar ao menu") 
if __name__ == "__main__":
    main()