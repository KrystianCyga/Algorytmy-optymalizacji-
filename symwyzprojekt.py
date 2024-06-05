import random
import math
import matplotlib.pyplot as plt
import numpy as np

# Generowanie losowego zestawu danych dla problemu RPQ
def generuj_dane_wejsciowe(ilosc_zadan):
    return [(i+1, random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)) for i in range(ilosc_zadan)]

# Obliczanie Cmax dla danej permutacji
def oblicz_cmax(permutacja, dane_wejsciowe):
    czas_zakonczenia = 0
    czas_zakonczenia_zadania = 0
    for i in permutacja:
        zadanie = dane_wejsciowe[i-1]
        czas_zakonczenia_zadania = max(czas_zakonczenia_zadania, zadanie[1]) + zadanie[2]
        czas_zakonczenia = max(czas_zakonczenia, czas_zakonczenia_zadania)
    return czas_zakonczenia

# Generowanie sąsiada przez zamianę dwóch zadań
def generuj_sasiada(permutacja):
    nowa_permutacja = permutacja.copy()
    i, j = random.sample(range(len(permutacja)), 2)
    nowa_permutacja[i], nowa_permutacja[j] = nowa_permutacja[j], nowa_permutacja[i]
    return nowa_permutacja

# Algorytm symulowanego wyżarzania dla problemu RPQ
def symulowane_wyzarzanie(temp_poczatkowa, wsp_chlodzenia, ilosc_iteracji, dane_wejsciowe):
    ilosc_zadan = len(dane_wejsciowe)
    permutacja = list(range(1, ilosc_zadan + 1))
    temperatura = temp_poczatkowa
    temps = []
    cmaxs = []

    for _ in range(ilosc_iteracji):
        sasiad = generuj_sasiada(permutacja)
        cmax1 = oblicz_cmax(permutacja, dane_wejsciowe)
        cmax2 = oblicz_cmax(sasiad, dane_wejsciowe)
        roznica_cmax = cmax2 - cmax1

        # Akceptacja gorszego rozwiązania z pewnym prawdopodobieństwem
        if roznica_cmax < 0 or random.random() < math.exp(-roznica_cmax / temperatura):
            permutacja = sasiad

        # Chłodzenie temperatury
        temperatura *= wsp_chlodzenia
        temps.append(temperatura)
        cmaxs.append(cmax2)

    return permutacja, temps, cmaxs

if __name__ == "__main__":
    # Parametry algorytmu
    temp_poczatkowa = 100.0
    ilosc_iteracji = 100
    N = 30
    ilosc_pomiarow = 100
    
    # Zakres współczynnika chłodzenia
    chlodzenia = np.linspace(0.5, 0.99, 50)
    
    # Generowanie losowego zestawu danych
    dane_wejsciowe = generuj_dane_wejsciowe(N)
    
    # Uruchamianie algorytmu i zbieranie wyników
    cmax_values_avg = []

    for wsp_chlodzenia in chlodzenia:
        cmax_values = []
        for _ in range(ilosc_pomiarow):
            najlepsza_permutacja, temps, cmaxs = symulowane_wyzarzanie(temp_poczatkowa, wsp_chlodzenia, ilosc_iteracji, dane_wejsciowe)
            cmax = oblicz_cmax(najlepsza_permutacja, dane_wejsciowe)
            cmax_values.append(cmax)
        cmax_values_avg.append(np.mean(cmax_values))

    # Dopasowanie regresji liniowej
    regression_coefficients = np.polyfit(chlodzenia, cmax_values_avg, 2)
    regression_line = np.polyval(regression_coefficients, chlodzenia)

    # Wykres zależności uśrednionego Cmax od współczynnika chłodzenia z regresją liniową
    plt.plot(chlodzenia, cmax_values_avg, marker='o', label=f'Cmax (średnia z {ilosc_pomiarow} pomiarów)')
    plt.xlabel('Współczynnik chłodzenia')
    plt.ylabel('Cmax (średnia)')
    plt.title('Zależność uśrednionego Cmax od współczynnika chłodzenia z regresją liniową')
    plt.legend()
    plt.grid(True)
    plt.show()

""" KOD DLA ZMIANY TEMPERATURY POCZATKOWEJ
initial_temperatures = np.linspace(50, 300, 80)
cmax_values_avg = []

for temperatura_poczatkowa in initial_temperatures:
    cmax_values = []

    for _ in range(ilosc_pomiarow):
        najlepsza_permutacja, temps, cmaxs = symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe)
        cmax = oblicz_cmax(najlepsza_permutacja, dane_wejsciowe)
        cmax_values.append(cmax)
    
    cmax_values_avg.append(np.mean(cmax_values))



# Wykres zależności uśrednionego Cmax od temperatury początkowej z regresją liniową
plt.figure(figsize=(10, 6))
plt.plot(initial_temperatures, cmax_values_avg, marker='o', label='Cmax ')
plt.xlabel('Temperatura początkowa')
plt.ylabel('Cmax ')
plt.title('Zależność uśrednionego Cmax od temperatury początkowej')
plt.legend()
plt.grid(True)
plt.show()
"""

""" KOD DLA ZMIANY ILOSCI ITERACJI
    # Zakres ilości iteracji
    iteracje = np.arange(50, 1000, 50)
    
    # Generowanie losowego zestawu danych
    dane_wejsciowe = generuj_dane_wejsciowe(N)  # Możesz dostosować ilość zadań
    
    # Uruchamianie algorytmu i zbieranie wyników
    cmax_values_avg = []

    for ilosc_iteracji in iteracje:
        cmax_values = []

        for _ in range(ilosc_pomiarow):
            najlepsza_permutacja, temps, cmaxs = symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe)
            cmax = oblicz_cmax(najlepsza_permutacja, dane_wejsciowe)
            cmax_values.append(cmax)
        
        cmax_values_avg.append(np.mean(cmax_values))

    # Dopasowanie regresji liniowej
    regression_coefficients = np.polyfit(iteracje, cmax_values_avg, 2)
    regression_line = np.polyval(regression_coefficients, iteracje)

    # Wykres zależności uśrednionego Cmax od ilości iteracji z regresją liniową
    plt.plot(iteracje, cmax_values_avg, marker='o', label='Cmax (średnia z {} pomiarów)'.format(ilosc_pomiarow))
    plt.xlabel('Ilość iteracji')
    plt.ylabel('Cmax (średnia)')
    plt.title('Zależność uśrednionego Cmax od ilości iteracji z regresją liniową')
    plt.legend()
    plt.xticks(np.arange(100, 1000, 100))
    plt.grid(True)
    plt.show()
"""