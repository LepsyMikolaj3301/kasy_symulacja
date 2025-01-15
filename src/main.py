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
        Będzie ona opisywana przez generator ( nie wiem jeszcze jaki model będzie odwzorowywał )
        
    Args:
        rodzaj_dnia (int): RANGA dnia ( czy duży / średni / mały RUCH w sklepie)
    """
    match ranga_dnia:
        # dzień customowy
        case 0: 
            lamlam  = float(input("Podaj wartosc lambda do rozkladu: "))
            
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
        # czas trwania otwarcia kas ( 6:30 - 22.00)
        self.simulation_duration = 55_800


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
        def stworz_zb_kas(liczba_kas_samoobs: int, liczba_kas_obs: int):
            # do poprawy
            zb_kas = {}
            if liczba_kas_samoobs:
                zb_kas['k_samoobs'] = uk.ZbiorKasySamoobslugowe(liczba_kas_samoobs)
            if liczba_kas_obs:
                zb_kas['k_obs'] = uk.ZbiorKasyObslugowe(liczba_kas_obs)
            return zb_kas

        def wybor_rodz_kas(zb_kas: dict[uk.ZbiorKasyObslugowe | uk.ZbiorKasySamoobslugowe]) -> str:
            """Ta funkcja będzie stwierdzać, do którego zbioru kas powinien byc Klient przydzielony
                Zakładamy, że klient ZAWSZE wybiera KRÓTSZĄ KOLEJKĘ, ponieważ jest mu obojętne, gdzie pójdzie
                Można też dodać założenia z wiekiem, wielkością zakupów itd ALE TO SIE ZOBAAACZY
                
            Args:
                zb_k_obslugowe (ZbiorKasyObslugowe): obiekt klasy Zbiorowej dla kas obsługowych 
                zb_k_samoobslugowe (ZbiorKasySamoobslugowe): obiekt klasy Zbiorowej dla kas samoobsługowych
                klient (Klient): obiekt klasy Klient który będzie przydzielany
            Returns:
                klucz (str): klucz odpowiedniej klasy
            """
            # jezeli tylko jeden rodzaj kasy jest dostępny -> od razu przydziel klienta
            if len(zb_kas.keys()) == 1:
                key_one: str = list(zb_kas.keys())[0]
                return key_one
            
            # znajdujemy dlugosc kolejki dla kas Samoobslugowych
            dlg_kol_k_samobs = zb_kas['k_samoobs'].kolejka.qsize()
            
            # znajdujemy dlugosci kolejek dla kas obslugowych - lista
            dlg_kol_k_obs = [kas_kol[1].qsize() for kas_kol in zb_kas['k_obs'].lista_kasa_x_kolejka]
            
            # porównujemy kolejki ze zbiorów i stwierdzamy do jakiego zbioru przypisujemy 
            # Jeżeli jakakolwiek kolejka będzie krótsza od tych z samoobsługowej, to przypisz do zbioru obsługowej
            for dlg_kol in dlg_kol_k_obs:
                if dlg_kol < dlg_kol_k_samobs:
                    return 'k_obs'
            return 'k_samoobs'
        
        #tworzymy ogólny zbior kas, zawierający  
        zb_kas: dict[uk.ZbiorKasyObslugowe | uk.ZbiorKasySamoobslugowe] = stworz_zb_kas(liczba_kas_samoobs=self.params['liczba_kas_samoobslugowych'],
                                                                                        liczba_kas_obs=self.params['liczba_kas_zwyklych'])
        
        
        

        
            

        pass

# Informacje o symulacji będą zapisywane w pliku JSON
def zapis_sym_json(sym_object: Symulacja):
    with open(r'rsc\\zapis_symulacji.json', 'a') as sym_file:
          json.dump(vars(sym_object), sym_file, indent=6)
    

def test_gestosci_losowania_klientow():
    # Tu trzeba sprawdzić, jakie parametry rozkładu dadzą chciany wynik
    
    pass




def test():
    param = odczyt_pliku_ster()
    print(param)

def main():
    pass


if __name__ == "__main__":
    test()
