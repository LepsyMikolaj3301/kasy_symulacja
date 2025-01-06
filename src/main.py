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

    

DONE:
    gówno


TODO:
    - WIZUALIZACJA I UI W CMDku ( pretty print ) !!! !!!!!
    - glowna petla
    - losowanie czasu przyjścia nowego klienta
"""

import json
import util_klasy as uk


def odczyt_pliku_ster() -> dict:

    with open(r'rsc\\plik_ster.json', 'r') as file:
        parametry = json.load(file)
        return parametry
    


def losuj_czas_nowy_klient(ranga_dnia: int):
    """ TA FUNKCJA LOSUJE CZAS MIĘDZY 'PRZYCHODZENIEM' NOWYCH KLIENTÓW DO SKLEPU

    Args:
        rodzaj_dnia (int): RANGA dnia ( czy duży / średni / mały RUCH w sklepie)
    """
    match ranga_dnia:
        # dzień customowy
        case 0: 
            pass
        # dzień roboczy - mały ruch ( środa w lidlu )
        case 1:
            pass
        # dzień zwykły - zwyczajny ruch ( sobota w lidlu )
        case 2:
            pass
        # dzień ruchliwy - duży ruch ( BLACK FRIDAY w lidlu )
        case 3:
            pass
        

      
class Symulacja:

    def __init__(self):
        self.params = odczyt_pliku_ster()

      

    def symulacja(self):
        """
        GLOWNA PETLA SYMULACJI

        przebieg:

            1. Inicjalizacja
            2. PETLA: 
                a. Sprawdzenie czas_for_klient (if 0: stworzenie klienta Klient(), dodanie do kolejki oraz wylosowanie nowego czas_for_klient)
                b. Wykonanie TICKu
                c. wyświetlenie wyników
            3. Zapisanie wyników i wyświetlenie wyników końcowych

        """
        

        
            

        pass

# Informacje o symulacji będą zapisywane w pliku JSON
def zapis_sym_json(sym_object: Symulacja):
    with open(r'rsc\\zapis_symulacji.json', 'a') as sym_file:
          json.dump(vars(sym_object), sym_file, indent=6)
    






def test():
    param = odczyt_pliku_ster()
    print(param)

def main():
    pass


if __name__ == "__main__":
    test()
