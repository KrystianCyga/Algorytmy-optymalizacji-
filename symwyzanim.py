import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter

# Liczba iteracji dla algorytmu
ilosc_iteracji = 400
elo=100
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
        czas_zakonczenia = max(czas_zakonczenia, czas_zakonczenia_zadania + zadanie[3])
    
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

    for _ in range(ilosc_iteracji):
        sasiad = generuj_sasiada(permutacja)
        roznica_cmax = oblicz_cmax(sasiad, dane_wejsciowe) - oblicz_cmax(permutacja, dane_wejsciowe)

        # Akceptacja gorszego rozwiązania z pewnym prawdopodobieństwem
        if roznica_cmax < 0 or random.random() < math.exp(-roznica_cmax / temperatura):
            permutacja = sasiad

        # Chłodzenie temperatury
        temperatura *= wspolczynnik_chlodzenia

    return permutacja

# Funkcja do aktualizacji wykresu w animacji
def update(frame):
    global temperatura_poczatkowa, wspolczynnik_chlodzenia, dane_wejsciowe, axs, ilosc_iteracji
    axs.clear()  # Wyczyść subplot przed narysowaniem nowej klatki

    # Tworzenie animacji dla kolejnych iteracji algorytmu
    permutacja = symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, frame, dane_wejsciowe)
    cmax = oblicz_cmax(permutacja, dane_wejsciowe)

    czasy_rozpoczecia = [0] * N
    czasy_rozpoczecia[0] = dane_wejsciowe[permutacja[0] - 1][1]

    for i in range(1, N):
        zadanieAKT = dane_wejsciowe[permutacja[i] - 1]
        zadaniePOP = dane_wejsciowe[permutacja[i - 1] - 1]
        czasy_rozpoczecia[i] = max(czasy_rozpoczecia[i - 1] + zadaniePOP[2], zadanieAKT[1])

    dane_wyjsciowe = [dane_wejsciowe[i - 1] for i in permutacja]
    r_values = [zadanie[1] for zadanie in dane_wyjsciowe]
    p_values = [zadanie[2] for zadanie in dane_wyjsciowe]
    
    axs.barh(permutacja, [zadanie[1] for zadanie in dane_wyjsciowe],left=czasy_rozpoczecia-np.array(r_values), color='green', edgecolor='black', label='Czas przygotowania',height=0.3)
    axs.barh(permutacja, [zadanie[2] for zadanie in dane_wyjsciowe], left=czasy_rozpoczecia, color='blue', edgecolor='black', label='Czas wykonywania')
    axs.barh(permutacja, [zadanie[3] for zadanie in dane_wyjsciowe], left=np.array(czasy_rozpoczecia) + np.array(p_values), color='red', edgecolor='black', label='Czas stygnięcia',height=0.3)
    
    axs.set_xlabel(f'Czas wykonywania\n (cmax={cmax})')
    axs.set_ylabel('Zadanie')
    axs.set_title(f'Wynik szeregowania - Iteracja: {frame}')
    axs.set_xticks(range(0, elo*2, 5))
    axs.grid(True)
    axs.set_yticks(range(1, N + 1, 1))
    axs.legend(loc='upper right')
    
    for i, txt in enumerate(czasy_rozpoczecia):
        axs.annotate(f"{txt}", (txt, permutacja[i]), ha='right', va='bottom')

if __name__ == "__main__":
    temperatura_poczatkowa = 200.0
    wspolczynnik_chlodzenia = 0.95
    N = 20  # Liczba zadań

    dane_wejsciowe = generuj_dane_wejsciowe(N)

    fig, axs = plt.subplots(1, 1, figsize=(20, 10))

    ani = FuncAnimation(fig, update, frames=range(0, elo + 1), interval=100, repeat=False)
    plt.show()
    # Zapis animacji do pliku mp4
    writer = FFMpegWriter(fps=10, metadata=dict(artist='Me'), bitrate=1800)
    ani.save("symulowane_wyzarzanie.mp4", writer=writer)
