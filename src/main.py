"""
Main program

Importuje:
    - stats_sym.py


Zawiera:
    wywoławcza main
    
    klasa Sklep
    
    funkcja run

Notes:
    - simpy.Resource() używany do tego, gdy jest coś ograniczonego
    przykład u nas: kasy ( tylko jakie? )
    
przykładowy projekt
https://realpython.com/simpy-simulating-with-python/

"""

import simpy

import json


def odczyt_pliku_ster() -> dict:
    with open('plik_ster.json', 'r') as file:
        parametry = json.load(file)
        return parametry

# TO DO:
# napisać klase Klient, która będzie obszerna z róznymi parametrami
# klasa klient będzie generowana później w funkcji przeprowadzającej symulacje
# czyli funkcja zrob_zakupy()


class Sklep:
    def __init__(self, env, plik_ster):
        # parametry
        parametry = odczyt_pliku_ster()

        self.env = env
        self.ilosc_kas = tuple(parametry["liczba_kas_samoobslugowych"],
                               parametry['liczba_kas_zwyklych'])
        
        if self.ilosc_kas[0]:
            self.kasa_sam = simpy.Resource(env, self.ilosc_kas[0])
        else:
            self.kasa_sam = None

        if self.ilosc_kas[1]:
            self.kasa_zw = simpy.Resource(env, self.ilosc_kas[1])
        else:
            self.kasa_zw = None



        pass

    # to do:
    # napisac funkcje skasuj_zakupy()


# zrob_zakupy() będzie funkcją która tyczy się pojedyńczego klienta
# ich czas zakupów będzie zależeć od parametrów z kartki i ich rozkładów
# ale starajmy się, by ich rozkłady nie były z dużym odchyleniem std. by symulacja była wiarygodna

# funkcja statystyk

# funkcja main ( do ogarnięcia muzgowego )