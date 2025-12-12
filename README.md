# Aplicação de Modularidade e Ball Tree para Validação e Segmentação de Comunidades e Funções Táticas na NBA

Este projeto aplica Teoria dos Grafos, KNN e Ball Tree para analisar estatísticas avançadas da NBA.

O sistema possui duas funções principais:

- Detecção de Comunidades: Identifica arquétipos de estilos de jogo de forma não supervisionada, criando uma rede visual da liga.

- Sistema de Scouting: Permite buscar jogadores similares a um alvo específico, validando se pertencem ao mesmo estilo de jogo e gerando comparativos visuais.

## Artigo Científico 

Este código é a implementação prática do estudo apresentado no artigo abaixo. Para detalhes teóricos aprofundados sobre a metodologia e resultados, acesse o PDF abaixo.

**PDF:** [Aplicação de Modularidade e Ball Tree para Validação e Segmentação de Comunidades e Funções Táticas na NBA](./Aplicação_de_Modularidade_e_Ball_Tree_para_Validação_e_Segmentação_de_Comunidades_na_NBA.pdf)

## Tecnologias Utilizadas

### Linguagem: Python 3.10.12

### Bibliotecas Utilizadas

O projeto foi desenvolvido utilizando as seguintes bibliotecas:

```
import os
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from networkx.algorithms.community import greedy_modularity_communities
```
### Instalação das Bibliotecas 
Para conseguir executar o algoritmo, a instalação das bibliotecas deve ser feita utilizando pip install no terminal do sistema operacional:

```
pip install pandas networkx scikit-learn matplotlib numpy
```

## Aquisição da Base de Dados (Web Scraping) e Filtragem

**Nota Importante**: Esta etapa serve apenas para documentar a metodologia de extração dos dados, a [Base de Dados Processada (.csv)](./AlgoritmoFinal/filtered_per_36_stats.csv) já está incluída na pasta AlgoritmoFinal. Você não precisa executar este script para rodar o projeto principal.

O repositório conta com um módulo dedicado à extração automática de dados atualizados diretamente do Fonte dos dados brutos: [NBA Stuffer](https://www.nbastuffer.com/2024-2025-nba-player-stats/). O script realiza a leitura, filtragem e normalização dos dados.

Localização: Pasta [DataSet](./DataSet)

O que o script faz:

- Acessa os dados da temporada 2024-2025.

- Seleciona apenas a Tabela da Temporada Regular.

- Filtra jogadores com GP >= 41 e MPG >= 20.

- Normaliza todas as estatísticas para Per 36 Minutes.

- Gera o arquivo filtered_per_36_stats.csv.

## Como Executar o Algoritmo

Para executar o algoritmo, deve-se utilizar os seguintes comandos no terminal (em ordem!)

#### Passo 1

```
git clone 'https://github.com/JoaoAnt0nio/Aplica-o-de-Modularidade-e-Ball-Tree-para-Valida-o-e-Segmenta-o-de-Comunidades-na-NBA.git' nba-analytics
```

#### Passo 2

```
cd nba-analytics
```

#### Passo 3

```
cd AlgoritmoFinal
```

### Passo 4

```
python3 main.py
``` 
Após isso, todas as entradas inseridas e as saídas do algoritmo estarão salvas na pasta 'AlgoritmoFinal' dentro de 'nba-analytics'

## Input e Output Esperados

### Input
Ao executar o main.py, o sistema exibirá um Menu Interativo no terminal com as seguintes opções:

- Opção 1 - Escolher jogador pelo nome: * Digite o nome do jogador desejado.

  - Nota: O sistema é flexível quanto à escrita (não diferencia maiúsculas de minúsculas). Exemplo: LeBron James, lebron james ou LEBRON JAMES são aceitos.

- Opção 2 - Sortear jogador aleatório: * O sistema seleciona aleatoriamente um atleta da base de dados para demonstrar a análise. Ideal para testes rápidos.

- Opção 3 - Sair: Encerra a execução.

```text
========================================
                 MENU       
========================================
1 - Escolher jogador pelo nome
2 - Sortear jogador aleatório
3 - Sair
----------------------------------------
Digite sua opção: 
```  

### Output
O algoritmo organiza os resultados automaticamente em pastas dentro do diretório AlgoritmoFinal. A estrutura gerada será:

#### Pasta `Relatorios_Globais`

Gerada automaticamente na primeira execução. Contém a análise macroscópica da liga:

- `nba_rede_comunidades.png`: Visualização completa do grafo da NBA, onde cada cor representa uma comunidade (estilo de jogo).

- `nba_comunidades_listagem.csv`: Lista de todos os jogadores e a qual comunidade pertencem.

- `nba_comunidades_medias.csv`: As médias estatísticas (centroides) de cada comunidade detectada.

#### Pasta do Jogador (ex: LeBron James)

Para cada jogador analisado, uma pasta com seu nome é criada contendo:

- `zoom_rede_LeBron_James.png`: Um recorte do grafo de comunidades focado na vizinhança do jogador analisado.

- Subpasta `Comparacoes_LeBron_James`: Contém os gráficos de radar comparando o jogador alvo com seus 5 vizinhos mais próximos (menores distâncias euclidianas).

#### Saída no Terminal

Além dos arquivos, o terminal exibe em tempo real:

- A comunidade do jogador analisado.

- Uma tabela com o Top 5 Jogadores Similares, a distância euclidiana (grau de semelhança) e o status (MATCH se forem da mesma comunidade, ou Híbrido se forem de comunidades diferentes).

Exemplo de Saída para o jogador LeBron James:

```text
>> ANÁLISE: LeBron James (Comunidade 2)

> Gerando Zoom de Rede para: LeBron James

>> TOP 5 SIMILARES (Resultados na pasta 'LeBron_James'):

RANK  JOGADOR                    DIST        STATUS
-------------------------------------------------------
1     Cade Cunningham            2.2676      MATCH
2     Julius Randle              2.7861      MATCH
3     De'Aaron Fox               2.9055      MATCH
4     Jalen Brunson              2.9353      MATCH
5     Darius Garland             2.9895      MATCH
``` 



### Autores

Humberto Henrique Lima Cunha - graduando em engenharia de computação pelo [CEFET-MG](https://www.cefetmg.br/).
E-mail para contato: humberto17henrique@gmail.com

João Antônio Melo Zacarias - graduando em engenharia de computação pelo [CEFET-MG](https://www.cefetmg.br/).
E-mail para contato: joaoantmeloz@gmail.com
