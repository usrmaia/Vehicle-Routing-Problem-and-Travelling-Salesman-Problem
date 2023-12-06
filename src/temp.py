from itertools import permutations
from math import sqrt


def calcular_distancia(coord1, coord2):
    return sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


def calcular_distancia_total(rota, coordenadas):
    distancia_total = 0
    for i in range(len(rota) - 1):
        cidade_atual = coordenadas[rota[i]]
        proxima_cidade = coordenadas[rota[i + 1]]
        distancia_total += calcular_distancia(cidade_atual, proxima_cidade)
    return distancia_total


# Coordenadas das cidades
coordenadas = {
    1: (-37.976262, -4.9414188),
    2: (-38.2707613, -5.5189184),
    3: (-38.34942350000001, -6.0319953),
    4: (-38.3040228, -5.810713499999999),
    5: (-38.76299449999999, -5.609255500000002),
    6: (-38.462624, -5.460287399999999),
    7: (-38.6219897, -5.8927263),
    8: (-38.0964766, -5.1467293),
    9: (-38.371994, -5.1084431),
    10: (-37.9618088, -4.7474946),
    11: (-38.460721, -6.043627499999999),
    12: (-38.1539198, -5.7234148),
    13: (-37.9894863, -5.072829099999999),
    14: (-38.2720868, -5.2695453),
    15: (-38.1286594, -5.2442316),
}

# Gerar todas as permutações possíveis das cidades
cidades = list(coordenadas.keys())
rotas_possiveis = permutations(cidades)

# Inicializar variáveis para armazenar a melhor rota e a menor distância
melhor_rota = None
menor_distancia = float("inf")

# Calcular a distância total para cada rota e encontrar a menor
for rota in rotas_possiveis:
    distancia_atual = calcular_distancia_total(rota, coordenadas)
    if distancia_atual < menor_distancia:
        menor_distancia = distancia_atual
        melhor_rota = rota

# Imprimir a melhor rota e a menor distância
print(f"Melhor rota: {melhor_rota}")
print(f"Menor distância: {menor_distancia}")
