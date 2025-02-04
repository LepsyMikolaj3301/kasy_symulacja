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
    coś


TODO:
    - WIZUALIZACJA I UI W CMDku ( pretty print ) !!! !!!!! JEDNAK NIE
    - glowna petla DONE
    - losowanie czasu przyjścia nowego klienta DONE
"""

import json
import util_klasy as uk
import os
from matplotlib import pyplot as plt



# STALE POMOCNICZE (ZAPIS PLIKU)
FILE_NAME = os.path.basename(__file__)
CUR_DIR = os.path.dirname(__file__)



def odczyt_pliku_ster() -> dict:
    """ZAWIERA ZMIENNE SYMULACJI

    Returns:
        dict: Dictionary zawierający zmienne decyzyjne
    """
    with open(CUR_DIR + r'\rsc\plik_ster.json', 'r') as file:
        parametry = json.load(file)
        return parametry
    

class Symulacja:

    def __init__(self, params: dict):
        # parametry ( zmienne symulacji )
        self.czas_sym_pred = params['czas_sym']
        self.liczba_kas_samo_obs = params['liczba_kas_samo_obs']
        self.liczba_kas_obs = params['liczba_kas_obs']
        self.lambd, self.amp, self.czest = params['lambda_amp_czest']
        
        # DANE ZEBRANE Z SYMULACJI
        
        # REALNA DŁUGOŚĆ SYMULACJI
        self.czas_sym = 0
        # ZAPISANI KLIENCI
        self.klients_list = []      
        self.num_generared_list = [] 
        
        # ILOSC KLIENTOW OBSLUZONYCH W ZBIORACH
        self.num_klient__k_o = 0
        self.num_klient__k_s = 0
        
        # CZASY OBSLUGI KLIENTOW
        self.czas_obsl_kl__k_o: list[list] = []
        self.czas_obsl_kl__k_s: list[list] = []
        
        # DlUGOSCI KOLEJEK W ODPOWIEDNIM INTERWALE: INTERWAL = 10
        self.dlg_kolej__k_o: list[list] = []
        self.dlg_kolej__k_s: list = []
        
        # DODATKOWE INFO:
            
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

        
        OGÓLNY ZARYS Z TESTÓW:
        zb_kasy_obs = ZbiorKasyObslugowe(20)

        for klient in test_klienty:
            zb_kasy_obs.klienci_do_kolejki(klient)

        i = 0 


        # WYKMINIONA LOGIKA - TRZEBA ŁADNIE OPISAĆ !!
        while not zb_kasy_obs.war_koniec():
            i += 1
            zb_kasy_obs.aktualizacja_kas()
            zb_kasy_obs.odczekaj_tick_wszyscy()
            print("tick")


        """
        
        # 1. INICJALIZACJA
        
        # określamy długość trwania symulacji przewidywany w założeniach
        czas_sym_pred = self.czas_sym_pred
        
        # tworzymy ogólny zbior kas, zawierający  
        zb_kas: dict[uk.ZbiorKasyObslugowe | uk.ZbiorKasySamoobslugowe] = uk.stworz_zb_kas(liczba_kas_samoobs=self.liczba_kas_samo_obs,
                                                                                           liczba_kas_obs=self.liczba_kas_obs)
        
        # czas symulacji realny
        czas_sym = 0
        
        # czas do następnego klienta
        czas_for_klient = 0
        
        # ilosc utworzonych klientow w danym interwale
        self.num_gen = 0
        
        # warunek zakończenia symulacji
        def koniec():
            if czas_sym > czas_sym_pred and (zb_kas['k_o'].war_koniec() and zb_kas['k_s'].war_koniec()):
                # jeżeli 
                return True
            else:
                return False
        
        # Akcja dodawania klienta do kasy
        def dodaj_klienta():
            # stworzenie klienta
            klient = uk.Klient()
            # dodanie klienta do kasy
            uk.wybor_rodz_kas(zb_kas, klient)
            # ZAPISANIE KLIENTA DO OBIEKTU
            self.klients_list.append(klient.get_all_info())
            # dodanie do licznika interwału
            self.num_gen += 1
    
            
        # 2. GŁÓWNA PĘTLA SYMULACJI
        print(f"\tSYM START\n")
        
        while not koniec(): # czy cały czas minął i czy kasy są puste (war_koncowe)
            
            # 2.1 Czy pora na przyjście następnego klienta (pod warunkiem, że nasz sklep jest wciąż otwarty)
            if czas_for_klient <= 0 and czas_sym < czas_sym_pred:
                dodaj_klienta()
                # wylosowanie nowego czasu do kolejnego klienta
                # czas_for_klient = uk.int_dist_exp_sin(czas_sym, self.lambd, self.amp, self.czest)
                while (czas_for_klient := uk.int_dist_exp_sin(czas_sym, self.lambd, self.amp, self.czest)) == 0:
                    dodaj_klienta()
            
            # 2.2 Aktualizacja stanu kas
            zb_kas['k_o'].aktualizacja_kas()
            zb_kas['k_s'].aktualizacja_kas()
            
            # 2.3 ODCZEKANIE TICKU (JEDNOSTKI - 1s)
            zb_kas['k_o'].odczekaj_tick_wszyscy(czas_sym)
            zb_kas['k_s'].odczekaj_tick_wszyscy(czas_sym)
            
            czas_sym += 1
            czas_for_klient -= 1
            
            # dodatkowe ify
            
            if czas_sym % (self.czas_sym_pred // 10) == 0:
                print('.', end='')
            
            # zapisanie informacji o przyjściu klienta ( do wykresu )
            if czas_sym % uk.INTERWAL == 0:
                self.num_generared_list.append(self.num_gen)
                self.num_gen = 0
            
        print(f'\n\tSYM END')
        
        # 3. Zapisanie INFORMACJI        
        self.czas_sym = czas_sym
        
        self.num_klient__k_o = zb_kas['k_o'].ilosc_obsluzonych_klient
        self.num_klient__k_s = zb_kas['k_s'].ilosc_obsluzonych_klient
        
        # Do czasów obsługi
        # K_obslugowe
        self.czas_obsl_kl__k_o = [ kasa_info[1] for kasa_info in zb_kas['k_o'].infolist_czas_obslugi()]
        # K_samoobslugowe
        self.czas_obsl_kl__k_s = [ kasa_info[1] for kasa_info in zb_kas['k_s'].infolist_czas_obslugi()]
        
        # Do dlugosci kolejek
        # K_obslugowe
        self.dlg_kolej__k_o = [dlg_kol[1] for dlg_kol in zb_kas['k_o'].dlg_kolejek_interwal]
        # K_samoobslugowe
        self.dlg_kolej__k_s = zb_kas['k_s'].dlg_kolejek_interwal
    
        return 1

    def print_result(self):
        print(f"Wszystkie info:")
        print(f"""PARAMETRY:\n\tCzas symulacji: {self.czas_sym_pred}
                            \n\tLiczba kas samoobslugowych: {self.liczba_kas_samo_obs}
                            \n\tLiczba kas obslugowych: {self.liczba_kas_obs}
                            \n\tLambda: {self.lambd}""")
        print('-  -' * 10)
        print(f'''WYNIKI: \n\tRealny Czas symulacji: {self.czas_sym}
                          \n\tIlosc klientow obsluzonych w roznych rodzajach (OBS \\ SOBS): {self.num_klient__k_o} / {self.num_klient__k_s}
                          ''')
        # print(f"""        \n\tCzasy obslugi klientow (OBS \\ SOBS): {self.czas_obsl_kl__k_o[0]} / {self.czas_obsl_kl__k_s[0]}
                        #   \n\tDlugosci kolejek (OBS \\ SOBS): {self.dlg_kolej__k_o[0]} / {self.dlg_kolej__k_s}""")
        print(f"Najdlg Kolejka k_s: {max(self.dlg_kolej__k_s)} w sekundzie: {self.dlg_kolej__k_s.index(max(self.dlg_kolej__k_s))}")
        print(f"Klienci liczba: {len(self.klients_list)}")
    
    
# Informacje o symulacji będą zapisywane jako pliki json
def save_simulation(obj: Symulacja, file_name: str):
    """Zapisuje obiekt symulacji w JSON

    Args:
        obj (Symulacja): Obiekt symulacji
    """
    
    f_name = '\\'.join(['sym_saved', file_name])
    
    modem = 'w' if os.path.exists(CUR_DIR + '\\' + f_name) else 'a'
    
    with open(CUR_DIR + '\\' + f_name, mode=modem) as file:
        json.dump(obj.__dict__, file, indent=6)
        print(f'Object {type(obj).__name__} saved to {file_name}')
    


def test():
    """
    Testy xd
    
    """
    params = {"liczba_kas_samo_obs": 4,
              "liczba_kas_obs": 2,
              "czas_sym": 57_600,
              "lambda_amp_czest": [ 0.21, 0.87, 1 ]
              }
    
    sym_test = Symulacja(params=params)
    sym_test.symulacja()
    sym_test.print_result()
    
    save_simulation(sym_test, 'sym_test.json')
    
def main():
    
    # TODO: 
    #   - zautomatyzowanie robienia symulacji
    #     
    
    
    #   1. Wszystkie wersje parametrow:
    config_sym: list = odczyt_pliku_ster()['schematy_symulacji']
    
    #   2. Przeprowadzenie wszystkich symulacji
    for index, conf in enumerate(config_sym):
        for j in range(3):
            sym: Symulacja = Symulacja(params=conf)
            sym.symulacja()
            print(f"\n\t\tSYMULACJA NR {index} PROBA {j}")
            # sym.print_result()
            save_simulation(sym, 'sym_' + str(index) + '_' + str(j) +'.json')
            print('\n')
        
    #   3. koniec
    print("ALL SYMS SUCCESS")
    pass


if __name__ == "__main__":
    main()
