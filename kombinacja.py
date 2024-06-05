
import random
import math
import matplotlib.pyplot as plt
import timeit
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation

# Generowanie losowego zestawu danych dla problemu RPQ
def generuj_dane_wejsciowe(ilosc_zadan):
    zadania = [(i+1, random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)) for i in range(ilosc_zadan)]
    return zadania

def oblicz_cmax(permutacja, dane_wejsciowe):
    czas_zakonczenia = 0
    czas_zakonczenia_zadania = 0
    
    for i in permutacja:
        zadanie = dane_wejsciowe[i-1]
        czas_zakonczenia_zadania = max(czas_zakonczenia_zadania, zadanie[1]) + zadanie[2]
        czas_zakonczenia = max(czas_zakonczenia, czas_zakonczenia_zadania)
    
    return czas_zakonczenia


# Generowanie sąsiada poprzez zamianę dwóch zadań w permutacji
def generuj_sasiada(permutacja):
    nowa_permutacja = permutacja.copy()
    i, j = random.sample(range(len(permutacja)), 2)
    nowa_permutacja[i], nowa_permutacja[j] = nowa_permutacja[j], nowa_permutacja[i]
    return nowa_permutacja

# Algorytm symulowanego wyżarzania dla problemu RPQ
def symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe):
    ilosc_zadan = len(dane_wejsciowe)
    permutacja = list(range(1, ilosc_zadan + 1))
    temperatura = temperatura_poczatkowa
    temps = []
    cmaxs = []
    cmax1 = 0
    cmax2 = 0

    for _ in range(ilosc_iteracji):
        sasiad = generuj_sasiada(permutacja)
        cmax1 = oblicz_cmax(permutacja, dane_wejsciowe)
        cmax2 = oblicz_cmax(sasiad, dane_wejsciowe)
        roznica_cmax = cmax2 - cmax1

        # Akceptacja gorszego rozwiązania z pewnym prawdopodobieństwem
        if roznica_cmax < 0 or random.random() < math.exp(-roznica_cmax / temperatura):
            permutacja = sasiad

        # Chłodzenie temperatury
        temperatura *= wspolczynnik_chlodzenia
        temps.append(temperatura)
        cmaxs.append(cmax2)

    return permutacja , temps , cmaxs

def pomiar_dla_parametrow(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe, ilosc_pomiarow=100):
    cmax_values = []

    for _ in range(ilosc_pomiarow):
        najlepsza_permutacja, temps, cmaxs = symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe)
        cmax = oblicz_cmax(najlepsza_permutacja, dane_wejsciowe)
        cmax_values.append(cmax)
    
    return np.mean(cmax_values)

if __name__ == "__main__":
    # Parametry algorytmu
    ilosc_iteracji = 100
    N = 30
    ilosc_pomiarow = 100
    
    # Zakresy parametrów do zmiany
    temperature_range = np.linspace(1, 200, 10)
    cooling_range = np.linspace(0.85, 0.99, 10)
    iteration_range = np.arange(50, 500, 50)
    
    # Generowanie losowego zestawu danych
    dane_wejsciowe = generuj_dane_wejsciowe(N)  # Możesz dostosować ilość zadań
    
    # Zbieranie wyników dla różnych kombinacji parametrów
    wyniki = []

    for temperatura_poczatkowa in temperature_range:
        for wspolczynnik_chlodzenia in cooling_range:
            for ilosc_iteracji in iteration_range:
                cmax = pomiar_dla_parametrow(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe, ilosc_pomiarow)
                wyniki.append((temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, cmax))

    # Sortowanie wyników
    wyniki.sort(key=lambda x: x[3])
    
    dc= pd.DataFrame(wyniki, columns=['Temperatura początkowa', 'Współczynnik chłodzenia', 'Liczba iteracji', 'Cmax (średnia)'])
    dc.to_csv('najlepsze_parametry.csv', index=False)
    # Tworzenie ramki danych Pandas
    df = pd.DataFrame(wyniki[:30], columns=['Temperatura początkowa', 'Współczynnik chłodzenia', 'Liczba iteracji', 'Cmax (średnia)'])
    

    # Wyświetlanie tabeli
    print(df)