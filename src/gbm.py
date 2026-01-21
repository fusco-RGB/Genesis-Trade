"""
gbm.py
Generatore di prezzi simulati usando una versione semplificata di Geometric Brownian Motion (GBM).
Usato per simulare la serie di prezzi per il grafico a candele.
"""
import math
import random

def genera_prossimo_prezzo(prezzo_attuale, trend, volatilita):
    """
    prezzo_attuale: il prezzo dell'ultimo turno
    trend: la tendenza generale (positivo sale, negativo scende)
    volatilita: quanto è 'nervosa' la moneta (0.01 è calma, 0.05 è instabile)
    """
    
    # Rappresenta l'incertezza del mercato (numero casuale tra -1 e 1 circa)
    variazione_casuale = random.gauss(0, 1)
    
    # Formula GBM semplificata
    esponente = (trend - 0.5 * volatilita**2) + (volatilita * variazione_casuale)
    nuovo_prezzo = prezzo_attuale * math.exp(esponente)
    
    return round(nuovo_prezzo, 2)


def generate_price_series(initial_price, mu, sigma, steps=100):
    """
    Genera una serie di prezzi sequenziali usando la funzione GBM esistente.
    Restituisce una lista di prezzi (float) di lunghezza `steps`.

    initial_price: prezzo iniziale
    mu: drift (trend)
    sigma: volatilità
    steps: numero di punti da generare
    """
    prices = [round(initial_price, 2)]
    current = initial_price
    for _ in range(steps - 1):
        current = genera_prossimo_prezzo(current, mu, sigma)
        prices.append(current)
    return prices
