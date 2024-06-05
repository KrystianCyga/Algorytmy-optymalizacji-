import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Liczba iteracji dla algorytmu
ilosc_iteracji = 100

# Generowanie losowego zestawu danych dla problemu RPQ
def generuj_dane_wejsciowe(ilosc_zadan):
    zadania = [(i+1, random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)) for i in range(ilosc_zadan)]
    return zadania

# Obliczanie wartości Cmax dla danej permutacji zadań
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
def symulowane_wyzarzanie(permutacja, temperatura_poczatkowa, wspolczynnik_chlodzenia, dane_wejsciowe):
    temperatura = temperatura_poczatkowa
    ilosc_iteracji = 1  # Jedna iteracja na raz
    for _ in range(ilosc_iteracji):
        sasiad = generuj_sasiada(permutacja)
        roznica_cmax = oblicz_cmax(sasiad, dane_wejsciowe) - oblicz_cmax(permutacja, dane_wejsciowe)

        # Akceptacja gorszego rozwiązania z pewnym prawdopodobieństwem
        if roznica_cmax < 0 or random.random() < math.exp(-roznica_cmax / temperatura):
            permutacja = sasiad

        # Chłodzenie temperatury
        temperatura *= wspolczynnik_chlodzenia

    return permutacja, temperatura

# Funkcja do aktualizacji wykresu w animacji
def update(frame):
    global permutacja, temperatura, wspolczynnik_chlodzenia, dane_wejsciowe, axs
    axs.clear()  # Wyczyść subplot przed narysowaniem nowej klatki

    # Tworzenie animacji dla kolejnych iteracji algorytmu
    permutacja, temperatura = symulowane_wyzarzanie(permutacja, temperatura, wspolczynnik_chlodzenia, dane_wejsciowe)
    cmax = oblicz_cmax(permutacja, dane_wejsciowe)

    czasy_rozpoczecia = [0] * N
    czasy_rozpoczecia[0] = dane_wejsciowe[permutacja[0] - 1][1]

    for i in range(1, N):
        zadanieAKT = dane_wejsciowe[permutacja[i] - 1]
        zadaniePOP = dane_wejsciowe[permutacja[i - 1] - 1]
        czasy_rozpoczecia[i] = max(czasy_rozpoczecia[i - 1] + zadaniePOP[2], zadanieAKT[1])

    dane_wyjsciowe = [dane_wejsciowe[i - 1] for i in permutacja]

    # Dodanie trzech różnych kolorów: czas r (zielony), czas p (niebieski), czas q (czerwony)
    r_values = [zadanie[1] for zadanie in dane_wyjsciowe]
    p_values = [zadanie[2] for zadanie in dane_wyjsciowe]
    q_values = [zadanie[3] for zadanie in dane_wyjsciowe]
    
    axs.barh(permutacja, r_values, color='green', edgecolor='black', label='Czas r')
    axs.barh(permutacja, p_values, left=r_values, color='blue', edgecolor='black', label='Czas p')
    axs.barh(permutacja, q_values, left=np.array(r_values) + np.array(p_values), color='red', edgecolor='black', label='Czas q')
    
    axs.set_xlabel(f'Czas wykonywania\n (cmax={cmax})')
    axs.set_ylabel('Zadanie')
    axs.set_title(f'Wynik szeregowania - Iteracja: {frame}')
    axs.set_xticks(range(0, max(czasy_rozpoczecia) + max(p_values) + max(q_values) + 1, 5))
    axs.grid(True)
    axs.set_yticks(range(1, N + 1, 1))

    axs.legend(loc='upper right')

    for i, txt in enumerate(czasy_rozpoczecia):
        axs.annotate(f"{txt}", (txt, permutacja[i]), ha='right', va='bottom')

if __name__ == "__main__":
    temperatura_poczatkowa = 100.0
    wspolczynnik_chlodzenia = 0.95
    N = 20  # Liczba zadań

    dane_wejsciowe = generuj_dane_wejsciowe(N)
    permutacja = list(range(1, N + 1))  # Początkowa permutacja
    temperatura = temperatura_poczatkowa  # Inicjalizacja temperatury

    fig, axs = plt.subplots(1, 1, figsize=(15, 5))

    ani = FuncAnimation(fig, update, frames=range(0, ilosc_iteracji + 1), interval=100, repeat=False)
    plt.show()
