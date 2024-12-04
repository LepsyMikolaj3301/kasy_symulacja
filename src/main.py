"""
Main program

Przebieg symulacji (szczegółowy):
    Pętla przedstawia przebieg czasowy, w którym będzie
    zasymulowany odstęp czasowy (1 minuta)

    Przebieg klienta w symulacji:
        Wygenerowanie klienta (w zależności od odst. czasowego)
        
        klient ze zrobionymi zakupami zostaje przydzielony do kolejki 
            (kolejek gdy są obsługowe kasy)
        
        * Kolejka *
            Gdy kasa pusta -> przydziel do kasy klienta

        Klient przy kasie:
            - kasowanie i checkout
        
        Deportacja klienta xd
    
TICK w PĘTLI = 1 sekunda            


Importuje:
    - stats_sym.py
    - util_klasy.py


Zawiera:
    wywoławcza main
    

Notes:
     * architektura potrzebna do przypisywania wygen. klientów do kolejek
     dla różnych klas *

    CZY WPROWADZENIE TICK = 1 sekunda MA SENS?

DONE:
    gówno


TODO:
    - WIZUALIZACJA I UI W CMDku ( pretty print ) !!!
    - glowna petla
    - 
"""

import json
import util_klasy as uk


def odczyt_pliku_ster() -> dict:
    with open('plik_ster.json', 'r') as file:
        parametry = json.load(file)
        return parametry

def losuj_czas_mdzy_klientami(ranga_dnia: int):
    """ TA FUNKCJA LOSUJE CZAS MIĘDZY 'PRZYCHODZENIEM' NOWYCH KLIENTÓW DO SKLEPU

    Args:
        rodzaj_dnia (int): RANGA dnia ( czy duży / średni / mały RUCH w sklepie)
    """
    pass

class SymulacjaKasy:

    

    def __init__(self):
        pass






def main():
    pass


if __name__ == "__main__":
    main()
