import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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
        cmaxs.append(oblicz_cmax(permutacja, dane_wejsciowe))

    return permutacja, temps, cmaxs

# Funkcja do aktualizacji wykresu w animacji
def update_plot(frame):
    global permutacja, dane_wejsciowe, temps, cmaxs, temperatura, wspolczynnik_chlodzenia
    temperatura = temperatura_poczatkowa
    sasiad = generuj_sasiada(permutacja)
    cmax1 = oblicz_cmax(permutacja, dane_wejsciowe)
    cmax2 = oblicz_cmax(sasiad, dane_wejsciowe)
    roznica_cmax = cmax2 - cmax1

    if roznica_cmax < 0 or random.random() < math.exp(-roznica_cmax / temperatura):
        permutacja = sasiad

    temperatura *= wspolczynnik_chlodzenia
    temps.append(temperatura)
    cmaxs.append(oblicz_cmax(permutacja, dane_wejsciowe))

    line1.set_data(range(1, frame + 2), temps[:frame + 1])
    scat2.set_offsets(np.column_stack((range(1, frame + 2), cmaxs[:frame + 1])))

    return line1, scat2

if __name__ == "__main__":
    temperatura_poczatkowa = 100.0
    wspolczynnik_chlodzenia = 0.95
    ilosc_iteracji = 100
    N = 30
    temps = []
    cmaxs = []

    dane_wejsciowe = generuj_dane_wejsciowe(N)
    
    permutacja, temps, cmaxs = symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe)
    
    cmax = oblicz_cmax(permutacja, dane_wejsciowe)
    print(cmax)
    fig, ax1 = plt.subplots()

    ax1.set_xlim(0, ilosc_iteracji)
    ax1.set_ylim(min(temps), max(temps))
    ax1.set_xlabel('Liczba iteracji')
    ax1.set_ylabel('Temperatura', color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()
    ax2.set_ylim(min(cmaxs), max(cmaxs))
    ax2.set_ylabel('Wartość Cmax', color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    line1, = ax1.plot([], [], color='tab:red', label='Temperatura')
    scat2 = ax2.scatter([], [], color='tab:blue', label='Wartość Cmax')  # Zmiana na scatter

    plt.title('Zależność temperatury i Cmax od liczby iteracji')
    fig.tight_layout()  # Dostosowanie układu wykresu
    anim = FuncAnimation(fig, update_plot, frames=ilosc_iteracji, interval=50, repeat=False)
    plt.show()
