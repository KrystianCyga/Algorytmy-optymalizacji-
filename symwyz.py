
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

    for _ in range(ilosc_iteracji):
        sasiad = generuj_sasiada(permutacja)
        roznica_cmax = oblicz_cmax(sasiad, dane_wejsciowe) - oblicz_cmax(permutacja, dane_wejsciowe)

        # Akceptacja gorszego rozwiązania z pewnym prawdopodobieństwem
        if roznica_cmax < 0 or random.random() < math.exp(-roznica_cmax / temperatura):
            permutacja = sasiad

        # Chłodzenie temperatury
        temperatura *= wspolczynnik_chlodzenia

    return permutacja

if __name__ == "__main__":
    # Parametry algorytmu
    temperatura_poczatkowa = 100.0
    wspolczynnik_chlodzenia = 0.95
    ilosc_iteracji = 1000
    N=3

    # Generowanie losowego zestawu danych
    dane_wejsciowe = generuj_dane_wejsciowe(N)  # Możesz dostosować ilość zadań

    print("Dane wejściowe:")
    print("{:<10} | {:<17} | {:<16} | {:<15}\n".format("Zadanie", "R - przygotowanie", "P - wykonywanie", "Q - dostarczenie"))

    for zadanie in dane_wejsciowe:
        print("{:<10} | {:<17} | {:<16} | {:<15}".format(*zadanie))


    # Tworzenie subplotów
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Wykres dla danych wejściowych
    czas_wykonywania = [zadanie[2] for zadanie in dane_wejsciowe]
    axs[0].barh(range(1, N + 1), [zadanie[2] for zadanie in dane_wejsciowe], color='lightblue', edgecolor='black')
    axs[0].set_xlabel('Czas wykonywania')
    axs[0].set_ylabel('Zadanie')
    axs[0].set_title('Dane wejściowe')
    axs[0].invert_yaxis()  # Odwrócenie osi y dla lepszej czytelności
    axs[0].set_xticks(range(0, max(zadanie[2] for zadanie in dane_wejsciowe)+1, 1))
    axs[0].grid(True)
    axs[0].set_yticks(range(1, N + 1, 1))
    
    
    start_time = timeit.default_timer()

    najlepsza_permutacja = symulowane_wyzarzanie(temperatura_poczatkowa, wspolczynnik_chlodzenia, ilosc_iteracji, dane_wejsciowe)

    elapsed_time = timeit.default_timer() - start_time
    print(f"Czas wykonania: {elapsed_time} sekundy")
    
    # Wyświetlenie wyników
    print("\nNajlepsza permutacja (kolejność zadań):", najlepsza_permutacja)
    cmax=oblicz_cmax(najlepsza_permutacja, dane_wejsciowe)
    print("Maksymalny czas zakończenia (Cmax):", cmax) 

  # Czasy rozpoczęcia
    czasy_rozpoczecia = [0] * N

    # Obliczenia
    czasy_rozpoczecia[0] = dane_wejsciowe[najlepsza_permutacja[0] - 1][1]

    for i in range(1, N):
        zadanieAKT = dane_wejsciowe[najlepsza_permutacja[i] - 1]
        zadaniePOP = dane_wejsciowe[najlepsza_permutacja[i - 1] - 1]
        czasy_rozpoczecia[i] = max(czasy_rozpoczecia[i - 1]+zadaniePOP[2], zadanieAKT[1])


    print(czasy_rozpoczecia)  
    dane_wyjsciowe = [dane_wejsciowe[i-1] for i in najlepsza_permutacja]
    
    # Wykres dla wyników szeregowania
    axs[1].barh(najlepsza_permutacja, [zadanie[2] for zadanie in dane_wyjsciowe], left=czasy_rozpoczecia, color='blue', edgecolor='black')
    axs[1].set_xlabel('Czas wykonywania')
    axs[1].set_ylabel('Zadanie')
    axs[1].set_title('Wynik szeregowania')
    axs[1].set_xticks(range(0, cmax*2 + 1, 1))
    axs[1].grid(True)
    axs[1].set_yticks(range(1, N + 1, 1))
    
    # Adnotacje czasów rozpoczęcia
    for i, txt in enumerate(czasy_rozpoczecia):
        axs[1].annotate(f"{txt}", (txt, najlepsza_permutacja[i]), ha='right', va='bottom')

    

    # Wyświetlenie subplotów
    plt.show()