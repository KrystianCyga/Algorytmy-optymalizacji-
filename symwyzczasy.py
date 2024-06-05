
import random
import math
import matplotlib.pyplot as plt
import timeit
import numpy as np
import itertools

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

def generuj_permutacje(permutacja, lista_permutacji, nowa_permutacja=[]):
    if len(permutacja) == 0:
        lista_permutacji.append(nowa_permutacja)    
    else:
        for i in range(len(permutacja)):
            generuj_permutacje(permutacja[:i] + permutacja[i+1:], lista_permutacji, nowa_permutacja + [permutacja[i]])



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

def algorytm_silowy(dane_wejsciowe):
    permutacja = list(range(1, len(dane_wejsciowe) + 1))
    najlepsza_permutacja = permutacja.copy()
    cmax = oblicz_cmax(permutacja, dane_wejsciowe)
    lista_permutacji = []  
    generuj_permutacje(permutacja, lista_permutacji)
    for perm in lista_permutacji:
        nowe_cmax = oblicz_cmax(perm, dane_wejsciowe)
        if nowe_cmax < cmax:
            najlepsza_permutacja = perm.copy()
    return najlepsza_permutacja

def szybki_algorytm_silowy(dane_wejsciowe):
    permutacja = list(range(1, len(dane_wejsciowe) + 1))
    najlepsza_permutacja = permutacja.copy()
    cmax = oblicz_cmax(permutacja, dane_wejsciowe)
    lista_permutacji = list(itertools.permutations(permutacja))
    for perm in lista_permutacji:
        nowe_cmax = oblicz_cmax(perm, dane_wejsciowe)
        if nowe_cmax < cmax:
            najlepsza_permutacja = list(perm).copy()
    return najlepsza_permutacja


if __name__ == "__main__":
    # Parametry algorytmu
    temperatura_poczatkowa = 100.0
    wspolczynnik_chlodzenia = 0.95
    ilosc_iteracji = 1000
    N=2

    czasy_wykonania_symulowane = []
    ilosci_danych = []
    ilosci_danych2 = []
    czasy_wykonania_silowy = []
    
        
    while N<50000:
        dane_wejsciowe = generuj_dane_wejsciowe(N)
        
        # Symulowane wyżarzanie
        start_time = timeit.default_timer()
        najlepsza_permutacja_symulowane = symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe)
        elapsed_time_symulowane = timeit.default_timer() - start_time
        czasy_wykonania_symulowane.append(elapsed_time_symulowane)
        
        if N<=10:
            # Algorytm silowy
            start_time = timeit.default_timer()
            najlepsza_permutacja_silowy = algorytm_silowy(dane_wejsciowe)
            elapsed_time_silowy = timeit.default_timer() - start_time
            czasy_wykonania_silowy.append(elapsed_time_silowy)
            ilosci_danych2.append(N)

        
        ilosci_danych.append(N)
        
        if N < 10:
             N += 1
        elif N >= 10 and N < 100:
            N += 10
        elif N >= 100 and N < 1000:
            N += 100
        elif N >= 1000 and N < 50000:
            N += 1000

        
    plt.plot(ilosci_danych, czasy_wykonania_symulowane, marker='o', label='Symulowane wyżarzanie')
    plt.plot(ilosci_danych2, czasy_wykonania_silowy, marker='o', label='Algorytm silowy')
    plt.xlabel('Ilość danych (N)')
    plt.ylabel('Czas wykonania (s)')
    plt.title('Czas wykonania algorytmów w zależności od ilości danych')
    plt.legend()
    plt.grid(True)
    plt.show()  
    
    plt.plot(ilosci_danych, czasy_wykonania_symulowane, marker='o', label='Symulowane wyżarzanie')
    plt.plot(ilosci_danych2, czasy_wykonania_silowy, marker='o', label='Algorytm silowy')
    plt.xscale('log')
    plt.xlabel('Ilość danych (N)')
    plt.ylabel('Czas wykonania (s)')
    plt.title('Czas wykonania algorytmów w zależności od ilości danych')
    plt.legend()
    plt.grid(True)
    plt.show()  