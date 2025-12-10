# Aplicação de Modularidade e Ball Tree para Validação e Segmentação de Comunidades e Funções Táticas na NBA

Este projeto aplica Teoria dos Grafos e algoritmos de Machine Learning (KNN e Ball Tree) para analisar estatísticas avançadas da NBA.

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

### Autores

Humberto Henrique Lima Cunha - graduando em engenharia de computação pelo [CEFET-MG](https://www.cefetmg.br/).
E-mail para contato: humberto17henrique@gmail.com

João Antônio Melo Zacarias - graduando em engenharia de computação pelo [CEFET-MG](https://www.cefetmg.br/).
E-mail para contato: joaoantmeloz@gmail.com
