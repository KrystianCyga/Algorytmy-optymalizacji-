
import random
import math
import matplotlib.pyplot as plt
import timeit
import numpy as np

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

if __name__ == "__main__":
    # Parametry algorytmu
    temperatura_poczatkowa = 100.0
    wspolczynnik_chlodzenia = 0.95
    ilosc_iteracji = 200
    N = 10
    
    # Generowanie losowego zestawu danych
    dane_wejsciowe = generuj_dane_wejsciowe(N)
    
    # Inicjalizacja list na temperaturę, cmax i czasy wykonania
    temps = []
    cmaxs = []
    times = []

    # Pomiar czasu wykonania algorytmu
    start_time = timeit.default_timer()
    
    # Wykonywanie algorytmu
    najlepsza_permutacja, temps, cmaxs = symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe)
    
    # Pomiar czasu zakończenia algorytmu
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    print(f"Czas wykonania algorytmu: {elapsed_time} sekundy")
    
    # Wyświetlenie najlepszej permutacji
    print("Najlepsza permutacja:", najlepsza_permutacja)
    
    # Obliczenie Cmax dla najlepszej permutacji
    cmax = oblicz_cmax(najlepsza_permutacja, dane_wejsciowe)
    print("Maksymalny czas zakończenia (Cmax):", cmax)
    
    # Obliczenie czasów wykonania
    for i in range(len(temps)):
        times.append(start_time + i * (elapsed_time / ilosc_iteracji))
    
    # Wyświetlenie wykresów
    fig, ax1 = plt.subplots()

    # Wykres temperatury
    ax1.plot(times, temps, label='Temperatura', color='tab:red')
    ax1.set_xlabel('Czas wykonania (s)')
    ax1.set_ylabel('Temperatura', color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    
    # Tworzenie drugiej osi y dla wykresu Cmax
    ax2 = ax1.twinx()
    
    # Wykres Cmax
    ax2.plot(times, cmaxs, 'o', label='Wartość maksymalna funkcji celu (Cmax)', color='tab:blue')
    ax2.set_ylabel('Wartość Cmax', color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title('Zależność temperatury i Cmax od czasu działania algorytmu')

    plt.show()
