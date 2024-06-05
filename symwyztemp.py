import random
import math
import matplotlib.pyplot as plt
import numpy as np

def generuj_dane_wejsciowe(N):
    dane_wejsciowe = []
    for _ in range(N):
        r = random.randint(0, 10)
        p = random.randint(1, 10)
        q = random.randint(0, 10)
        dane_wejsciowe.append((r, p, q))
    return dane_wejsciowe

def symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe):
    N = len(dane_wejsciowe)
    najlepsza_permutacja = list(range(N))
    random.shuffle(najlepsza_permutacja)
    najlepszy_cmax = oblicz_cmax(najlepsza_permutacja, dane_wejsciowe)
    aktualna_permutacja = najlepsza_permutacja[:]
    aktualny_cmax = najlepszy_cmax
    temperatura = temperatura_poczatkowa

    temps = []
    cmaxs = []

    for i in range(ilosc_iteracji):
        if temperatura <= 50:
            break
        
        temps.append(temperatura)
        cmaxs.append(aktualny_cmax)
        
        # Losowe zamiana dwóch elementów permutacji
        i, j = random.sample(range(N), 2)
        nowa_permutacja = aktualna_permutacja[:]
        nowa_permutacja[i], nowa_permutacja[j] = nowa_permutacja[j], nowa_permutacja[i]
        nowy_cmax = oblicz_cmax(nowa_permutacja, dane_wejsciowe)

        delta = nowy_cmax - aktualny_cmax
        if delta < 0 or random.random() < np.exp(-delta / temperatura):
            aktualna_permutacja = nowa_permutacja
            aktualny_cmax = nowy_cmax

        if aktualny_cmax < najlepszy_cmax:
            najlepsza_permutacja = aktualna_permutacja
            najlepszy_cmax = aktualny_cmax

        temperatura *= wspolczynnik_chlodzenia

    return najlepsza_permutacja, temps, cmaxs

def oblicz_cmax(permutacja, dane_wejsciowe):
    N = len(dane_wejsciowe)
    t = 0  # Czas bieżący
    cmax = 0

    for i in permutacja:
        r, p, q = dane_wejsciowe[i]
        if t < r:
            t = r
        t += p
        cmax = max(cmax, t + q)

    return cmax

# Parametry algorytmu
wspolczynnik_chlodzenia = 0.95
ilosc_iteracji = 1000  # Wysoka liczba iteracji, ale zatrzymanie przy 50 stopniach
N = 30
ilosc_pomiarow = 100  # Zmniejszona liczba pomiarów

# Generowanie losowego zestawu danych
dane_wejsciowe = generuj_dane_wejsciowe(N)  # Możesz dostosować ilość zadań

# Uruchamianie algorytmu i zbieranie wyników
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
