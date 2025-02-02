"""
    util_klasy.py czyli program zawierający wszystkie potrzebne obiekty
    do głównego programu.

    Zawartosc:
        - class Klient
        - class ZbiorKasySamoobsługowe
        - class ZbiorKasyZwykła
    
        Powyższe 2 to klasy tzw kolejkowo-zbiorowe 
        ( one zawierają mniejsze pojedyńcze kasy i kolejke)
    Dodatkowo:
        - class KasaZwykla
        - class KasaSamoobslugowa
        
    WAŻNE:
        ZAŁOŻENIA KAS:
            Klasy Kasa to dwie różne klasy, mające swoją "polityke kolejkową"

        NA ZAJĘCIA:
        https://static.nbp.pl/systemy/platniczy/Zwyczaje-platnicze-w-Polsce-2023.pdf
        Czy ma sens uzależniać to od wieku?

    Dodatkowo:

TODO:
- dodanie stałej płacenia kartą i gotówką -> zrobione przez Paole 
- połączenie kas samoobsługowych i obsł w wspólnym działaniu ( kasy mieszane )
- dodanie obsłużenia lub "kary" w płaceniu gotówką w kasie samoobsługowej 
- dodanie zapisywania zebranych danych oraz integracja w main.py  

?- opcjonalne: Zrobienie przypadek SAMPLE (perspektywa klienta i analiza np. ile on czekał w różnych konfiguracjach kas)
"""
import random
from queue import Queue
from numpy.random import normal, exponential
from math import sin

# STAŁE GLOBALNE
STALA_PAKOWANIA = 2.5 # mniej więcej określenie, ile pakuje się jeden produkt
STALA_PLT_KARTO_NORMAL = 12.5  # czas zapłacenia kartą
STALA_WPR_PIN = 14.5 # czas wprowadzania pinu
STALA_PLT_GOTOWKO = 34  # czas zapłacenia gotówką
STALA_KASOWANIA_EKSPERT = 2  # czas skasowania jednego produktu przez kasjera
INTERWAL = 10


class Klient:
    """
    Klasa będzie służyła jako bardziej kontener informacji ( struct )
    """

    def __init__(self, param=None):
        """
        Args:
            wiek (int): Wiek losowany zgodnie z demografią miasta Wrocławia (2022)
            num_produkt (int): Ilość kupowanych produktów zależnie od wieku klienta
            t_na_prod (float): Czas na produkt może być losowany, ale po przemnożeniu w klasie Kasa ( musi być zaokrąglony do INT), bowiem tick (odstęp czasowy) to 1 minuta
            platnosc_karto (bool): Płatność kartą - zależne od wieku (badania NBP 2023)
        """

        # Funkcja losująca wiek klienta
        def random_age():
            # Dane populacji dla przedziałów wiekowych w 2022 roku (dane Urzędu statystycznego we Wrocławiu)
            age_ranges = {
                (18, 24): 30313 + (22382 * 5 / 2),  # 20-24 + 5/2 z 15-19
                (25, 34): 56144 + 65721,  # 25-29 + 30-34
                (35, 44): 67650 + 57518,  # 35-39 + 40-44
                (45, 54): 46934 + 33833,  # 45-49 + 50-54
                (55, 64): 29720 + 34885,  # 55-59 + 60-64
                (65, 100): 42417 + 38473 + 21639 + 15164 + 17874  # 65-69, 70-74, 75-79, 80-84, 85+
            }

            # Cała populacja Wrocławia
            total_population = 674079

            # Wyliczanie prawdopodobieństw dla każdego przedziału wiekowego
            age_probabilities = {age: count / total_population for age, count in age_ranges.items()}

            # Wylosowanie przedziału wiekowego klienta
            przedzial = random.choices(list(age_probabilities.keys()), weights=list(age_probabilities.values()))[0]

            # Wylosowanie konkretnego wieku z przedziału
            return random.randint(przedzial[0], przedzial[1])

        # Funkcja wyznaczająca przedział wiekowy klienta odpowiedni dla słownika ze statystykami
        # (różne badania - różne przedziały wiekowe)
        def znajdz_przedzial(slownik, wiek):

            przedzial = None
            for klucz_przedzialu in slownik:
                if klucz_przedzialu[0] <= wiek <= klucz_przedzialu[1]:
                    przedzial = klucz_przedzialu
                    break
            return przedzial

        # Funckja losująca wielkość zakupów (małe, duże) w zależności od wieku klienta
        def random_groceries_size(wiek):

            prawdopodobne_wielkosci_zakupow = {
                (18, 24): {"duze": 0.13, "srednie": 0.27, "male": 0.37, "random": 0.08},
                (25, 34): {"duze": 0.13, "srednie": 0.38, "male": 0.31, "random": 0.1},
                (35, 44): {"duze": 0.12, "srednie": 0.41, "male": 0.32, "random": 0.08},
                (45, 54): {"duze": 0.12, "srednie": 0.34, "male": 0.38, "random": 0.07},
                (55, 64): {"duze": 0.07, "srednie": 0.28, "male": 0.47, "random": 0.06},
                (65, 100): {"duze": 0.07, "srednie": 0.24, "male": 0.43, "random": 0.07}
            }

            # Znalezienie odpowiedniego przedziału wiekowego
            przedzial = znajdz_przedzial(prawdopodobne_wielkosci_zakupow, wiek)

            wielkosci = list(prawdopodobne_wielkosci_zakupow[przedzial].keys())  # np. ["duze", "srednie", "male", "random"]
            prawdopodobienstwa = list(prawdopodobne_wielkosci_zakupow[przedzial].values())  # np. [0.13, 0.27, 0.37, 0.08]

            # Losowanie wielkości zakupów
            return random.choices(wielkosci, prawdopodobienstwa)[0]

        # Funkcja losująca konkretną liczbę produktów kupowanych przez klienta
        def random_groceries_amount(size):

            # Przyjęte przez nas ilości produktów dla małych, średnich i dużych zakupów
            zakresy_ilosci_produktow = {
                "male": {"min": 1, "max": 10},
                "srednie": {"min": 11, "max": 25},
                "duze": {"min": 26, "max": 50},
                "random": {"min": 1, "max": 50}
            }

            minimum = zakresy_ilosci_produktow[size]["min"]
            maximum = zakresy_ilosci_produktow[size]["max"]

            # Wylosowanie ilości produktów
            return round(random.uniform(minimum, maximum))

        def czas_skan_bez_ujemnych():
            number_generated = False

            while not number_generated:
                # 
                czas_skan = normal(4.5, 1)
                if czas_skan >= STALA_KASOWANIA_EKSPERT:  # Akceptujemy tylko wartości > 2, bo klienci szybciej nie skanują
                    number_generated = True

            return czas_skan

        # Funkcja losująca, czy klient korzysta z płatności bezgotówkowych
        def czy_karta(wiek):

            prawdopodobienstwo_platnosci_bezgotowkowej = {
                (18, 24): 0.585 + 0.085,
                (25, 39): 0.771 + 0.03,
                (40, 54): 0.669 + 0.013,
                (55, 64): 0.408 + 0.0,
                (65, 100): 0.328 + 0.004
            }

            przedzial = znajdz_przedzial(prawdopodobienstwo_platnosci_bezgotowkowej, wiek)

            prawd_karta = prawdopodobienstwo_platnosci_bezgotowkowej[przedzial]
            prawdopodobienstwa = [prawd_karta, 1 - prawd_karta]

            return random.choices([True, False], prawdopodobienstwa)[0]

        if param:
            self.wiek = param['wiek']
            self.num_produkt = param['num_produkt']
            self.t_na_prod = param['t_na_prod']
            self.platnosc_karto = param['platnosc_karto']
        else:
            self.wiek = random_age()
            self.wielk_zakupow = random_groceries_size(self.wiek)
            self.num_produkt = random_groceries_amount(self.wielk_zakupow)
            self.t_na_prod = czas_skan_bez_ujemnych()
            self.platnosc_karto = czy_karta(self.wiek)
    
    # def __str__(self):
    #     print(f'Wiek: {self.wiek}')
    #     print(f'Num_prod: {self.num_produkt}')
    #     print(f't_na_prod: {self.t_na_prod}')
    #     print(f'Karto: {self.platnosc_karto}')



class KasaSamoobslugowa:
    def __init__(self):
        
        # lista zawierająca czase obsłużonych klientów
        self.lista_czasow_obslugi = []
        # GIGA WAŻNE - LICZNIK, ILE TICKÓW ZOSTAŁO DO PRZECZEKANIA
        self.realny_czas_counter = 0

        # WARTOŚĆ MÓWIĄCA NAM CZY KLIENT OBSŁUGUJE KASE
        self.is_with_klient = False

    def przyjmij_klienta(self, klient: Klient):
        # Resetujemy wartość, czyli nowy klient jest obsługiwany
        self.is_with_klient = True

        self.initial_ilosc_prod = klient.num_produkt
        self.t_na_produkt = klient.t_na_prod
        
        def checkout_time() -> float:
            # WYDŁUŻONA PŁATNOŚĆ ZE WZGLĘDU NA WPROWADZENIE PINU -> WIĘCEJ NIŻ 20 PRODUKTÓW MOŻE WSKAZYWAĆ NA WPR PINU
            platnosc_karto = STALA_PLT_KARTO_NORMAL + STALA_WPR_PIN if klient.num_produkt > 20 else STALA_PLT_KARTO_NORMAL
            return STALA_PAKOWANIA * self.initial_ilosc_prod + platnosc_karto

        # czas po zakończeniu kasowania
        self.kasa_checkout = checkout_time()
        # GIGA WAŻNE - OBLICZENIE WSTĘPNE OBSŁUŻENIA KASY:
        self.czas_obslugi = round(self.t_na_produkt * self.initial_ilosc_prod + self.kasa_checkout)

        # Zapisanie do kasy informacji ile obsługiwano jednego klienta
        self.lista_czasow_obslugi.append(self.czas_obslugi)

        # nadanie counterowi nowego czasu, nowego klienta
        self.realny_czas_counter = self.czas_obslugi
    
    def odczekaj_tick(self):
        # Ta funkcja nam zwróci wartość True, jeżeli klient został obsłużony
        if self.realny_czas_counter <= 0:
            self.is_with_klient = False
        else:
            # Inaczej, odczekaj jeden tick
            self.realny_czas_counter -= 1


class ZbiorKasySamoobslugowe:
    def __init__(self, ilosc_kas: int):
        self.kolejka = Queue()
        self.lista_kas = [KasaSamoobslugowa() for _ in range(ilosc_kas)] 
        self.ilosc_kas = ilosc_kas
        self.interwal = INTERWAL
        self.dlg_kolejek_interwal = []
        # INFORMACJE ZEBRANE O KLIENTACH
        self.ilosc_obsluzonych_klient = 0

    def klienci_do_kolejki(self, klient: Klient):
        self.kolejka.put(klient)

    def odczekaj_tick_wszyscy(self, true_czas):
        # odczytanie długości kolejki
        def zapisz_dlg_kolejki():
            self.dlg_kolejek_interwal.append(self.kolejka.qsize())
        
        for i in range(self.ilosc_kas):
            self.lista_kas[i].odczekaj_tick()
        if true_czas % self.interwal == 0:
            zapisz_dlg_kolejki()
        
        
    def war_koniec(self) -> bool:
        # Pętla sprawdzająca czy wszystkie kasy są puste
        for kasa in self.lista_kas:
            if kasa.is_with_klient:
                return False
        # jeżeli nie zreturnuje, to znaczy, że kasy puste
        # jeżeli kolejka pusta -> return True
        return self.kolejka.empty()


    def aktualizacja_kas(self):
        
        for i, kasa in enumerate(self.lista_kas):
            # sprawdzamy czy ktoś jeszcze jest w kolejce
            if self.kolejka.empty():
                break
            # jeżeli jest, to mozemy dodać do kasy
            if not kasa.is_with_klient:
                self.lista_kas[i].przyjmij_klienta(self.kolejka.get())
                # zapisanie info o przyjeciu klienta
                self.ilosc_obsluzonych_klient += 1
    
    def infolist_czas_obslugi(self) -> list[tuple]:
        list_obsluga_kl = []
        for i, kasa in enumerate(self.lista_kas):
            list_obsluga_kl.append( (i, kasa.lista_czasow_obslugi) )
        return list_obsluga_kl
        


# !!
# CZĘŚĆ KAS OBSŁUGOWYCH
# 
# 
class KasaObslugowa:
    def __init__(self):

        self.t_na_produkt = STALA_KASOWANIA_EKSPERT
        
        # ZBIERANE INFORMACJE O KLIENTACH
        self.lista_czasow_obslugi = []
        
        # GIGA WAŻNE - LICZNIK, ILE TICKÓW ZOSTAŁO DO PRZECZEKANIA
        self.realny_czas_counter = 0

        # WARTOŚĆ MÓWIĄCA NAM CZY KLIENT OBSLUGUJE KASE
        self.is_with_klient = False

    def przyjmij_klienta(self, klient: Klient):

        # Resetujemy wartość, czyli nowy klient jest obsługiwany
        self.is_with_klient = True
        self.initial_ilosc_prod = klient.num_produkt
        
        # WYDŁUŻONA PŁATNOŚĆ ZE WZGLĘDU NA WPROWADZENIE PINU -> WIĘCEJ NIŻ 20 PRODUKTÓW MOŻE WSKAZYWAĆ NA WPR PINU
        platnosc_karto = STALA_PLT_KARTO_NORMAL + STALA_WPR_PIN if klient.num_produkt > 20 else STALA_PLT_KARTO_NORMAL
            
        self.platnosc = platnosc_karto if klient.platnosc_karto else STALA_PLT_GOTOWKO

        # roznica czyli czy pakowanie zajmie mi dłużej niż kasowanie kasjerki
        roznica = (STALA_PAKOWANIA * self.initial_ilosc_prod) - (self.t_na_produkt * self.initial_ilosc_prod)

        # czas po zakończeniu kasowania
        self.kasa_checkout = self.platnosc + (0 if roznica <= 0 else roznica)

        # GIGA WAŻNE - OBLICZENIE WSTĘPNE OBSŁUŻENIA KASY:
        self.czas_obslugi = round(self.t_na_produkt * self.initial_ilosc_prod + self.kasa_checkout)

        # dodajemy do historii czas obsługi klienta
        self.lista_czasow_obslugi.append(self.czas_obslugi)

        # nadanie counterowi nowego czasu, nowego klienta
        self.realny_czas_counter = self.czas_obslugi


    def odczekaj_tick(self):
        # odczekanie ticku pojedyńczej kasy
        if self.realny_czas_counter <= 0:
            self.is_with_klient = False
        else:
            self.realny_czas_counter -= 1


class ZbiorKasyObslugowe:
    def __init__(self, ilosc_kas):
        self.ilosc_kas = ilosc_kas
        self.interwal = INTERWAL
        
        # DANE ZEBRANE:
        self.ilosc_obsluzonych_klient = 0
        self.dlg_kolejek_interwal = [(i, []) for i in range(ilosc_kas)]
        
        
        # TWORZENIE LIST PAR: ( KASA, KOLEJKA )
        self.lista_kasa_x_kolejka = [(KasaObslugowa(), Queue())
                                     for _ in range(ilosc_kas)]

    def klienci_do_kolejki(self, klient: Klient):

        # PRZYDZIELAMY KLIENTA DO NAJKRÓTSZEJ KOLEJKI

        # tymczasowa lista z długościami kolejek
        lista_dlg_kolejek = [kasa_kolejka[1].qsize() for kasa_kolejka in self.lista_kasa_x_kolejka]
        # index najmniejszej wartości z lista_dlg_kolejek
        index_min = min(range(len(lista_dlg_kolejek)), key=lista_dlg_kolejek.__getitem__)

        # Przydziel klienta do najkrótszej kolejki
        self.lista_kasa_x_kolejka[index_min][1].put(klient)

    def odczekaj_tick_wszyscy(self, true_czas: int):
        
        
        def zapisz_dlg_kolejek():
            # zapisujemy w danym interwale wszystkie długości kolejek, do każdej kasy
            for i, kasa_kolej in enumerate(self.lista_kasa_x_kolejka):
                kolej: Queue = kasa_kolej[1]
                self.dlg_kolejek_interwal[i][1].append(kolej.qsize())
            
        # Odczekujemy po wszystkich kasach TICK
        for i in range(self.ilosc_kas):
            self.lista_kasa_x_kolejka[i][0].odczekaj_tick()
            
            
        # sprawdzenie, czy co interwał mamy zapisywać stan kolejki
        if true_czas % self.interwal == 0:
            zapisz_dlg_kolejek()
        

    def war_koniec(self) -> bool:
        # Sprawdzamy czy kolejki są puste, jeżeli one są puste 
        for i in range(self.ilosc_kas):
            if not self.lista_kasa_x_kolejka[i][1].empty() or self.lista_kasa_x_kolejka[i][0].is_with_klient:
                return False
        return True

    def aktualizacja_kas(self):
        # Sprawdza czy kasa jest pusta, jak jest - dodaje klienta
        for i, kasa_kolejka in enumerate(self.lista_kasa_x_kolejka):
            # sprawdza wcześniej czy kolejka nie jest pusta ( był bug z tym związany )
            if kasa_kolejka[1].empty():
                continue
            # teraz sprawdzamy czy kasa jest pusta
            if not kasa_kolejka[0].is_with_klient:
                # dodajemy klienta do kasy
                self.lista_kasa_x_kolejka[i][0].przyjmij_klienta(self.lista_kasa_x_kolejka[i][1].get())
                # zwiększamy licznik
                self.ilosc_obsluzonych_klient += 1
    
    def infolist_czas_obslugi(self) -> list[tuple]:
        list_obsluga_kl = []
        for i, kasa_kolejka in enumerate(self.lista_kasa_x_kolejka):
            list_obsluga_kl.append( (i, kasa_kolejka[0].lista_czasow_obslugi) ) # [ (1, [278, 283, 929, ...])]
        return list_obsluga_kl
    

# WRAPPER DO MAIN - Wybór zbioru klasy
def stworz_zb_kas(liczba_kas_samoobs: int, liczba_kas_obs: int) -> dict[ZbiorKasyObslugowe | ZbiorKasySamoobslugowe]:
    """Tworzymy obiekt ZB_KAS ktory wrappuje kasy samoobslugowe i obslugowe

    Args:
        liczba_kas_samoobs (int): parametr do tworzenia obiektu ZbiorKasySamoobslugowe
        liczba_kas_obs (int): parametr do tworzenia obiektu ZbiorKasyObs

    Returns:
        zb_kas (dict): Dict zaw. zbiory 2 roznych kas
    """
    zb_kas = {}
    if liczba_kas_samoobs:
        zb_kas['k_s'] = ZbiorKasySamoobslugowe(liczba_kas_samoobs)
    if liczba_kas_obs:
        zb_kas['k_o'] = ZbiorKasyObslugowe(liczba_kas_obs)
    return zb_kas

def wybor_rodz_kas(zb_kas: dict[ZbiorKasyObslugowe | ZbiorKasySamoobslugowe], klient: Klient):
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
    
    
    # PRZYPADKI SKRAJNE
    # przypadek gdy nie ma kas określonych
    if len(zb_kas.keys()) == 0:
        raise Exception("BRAK LICZBY KAS -> NIE MA SKLEPU")
    
    # jezeli tylko jeden rodzaj kasy jest dostępny -> od razu przydziel klienta
    if len(zb_kas.keys()) == 1:
        zb_kas[list(zb_kas.keys())[0]].klienci_do_kolejki(klient)
    
     # WAŻNE - JEŻELI KLIENT NIE MOŻE PLACIC KARTO -> PRZYDZIEL DO KAS OBSLUGOWYCH
    if not klient.platnosc_karto:
        zb_kas['k_o'].klienci_do_kolejki(klient)
        return
    
    # znajdujemy dlugosc kolejki dla kas Samoobslugowych
    dlg_kol_k_samobs = zb_kas['k_s'].kolejka.qsize()
    
    # znajdujemy dlugosci kolejek dla kas obslugowych - lista dlugosci kolejek
    dlg_kol_k_obs = [kas_kol[1].qsize() for kas_kol in zb_kas['k_o'].lista_kasa_x_kolejka]
    
    # porównujemy kolejki ze zbiorów i stwierdzamy do jakiego zbioru przypisujemy 

    # Jeżeli jakakolwiek kolejka będzie krótsza od tych z samoobsługowej, to przypisz do zbioru obsługowej
    for dlg_kol in dlg_kol_k_obs:
        if dlg_kol < dlg_kol_k_samobs:
            # jezeli jakakolwiek kolejka do obslogowych jest krotsza od bezobsl. to przydziela do tego zbioru
            zb_kas['k_o'].klienci_do_kolejki(klient)
            break
    else:
        # jezeli nie znajdzie sie taka klasa, to przydzielamy do kas samoobs.
        zb_kas['k_s'].klienci_do_kolejki(klient)
    return



def int_dist_exp(lamb: float) -> int:
    # wylosuj ilosc sekund do przyjscia nastepnego klienta
    return round(exponential(1/lamb))

def int_dist_exp_sin(t: int, lamb_0: float, amp: float, omega: float) -> int:
    """FUNKCJA ZWRACAJĄCA CZAS OCZEKIWANIA DO KOLEJNEGO KLIENTA

        NADANA WZOREM: 
        X ~ Exp(lambd_t)
        p(x | t) = lam_t*e^(-lam_t*x)
        gdzie: lam_t = lamb_0 * ( (1 + amp*sin(omega * t))**2 ) 

    Args:
        t (int): czas globalny
        lamb_0 (float): lambda 0
        amp (float): amplituda efektu sinusoidalnego
        omega (float): częstotliwość --"--

    Returns:
        int: zaokrąglony sample rozkładu
    """
    lam_t = lamb_0*((1 + amp*sin(omega * t))**2)
    return round(exponential(1/lam_t))


def test():
    """
    DO TESTOWANIA GŁÓWNEJ LOGIKI
    """
    
    from matplotlib import pyplot as plt
    
    def param_test_gen():
        param = {'wiek': random.randint(7, 90),
                 'num_produkt': random.randint(1, 40),
                 't_na_prod': min(12, max(2, random.gauss(3.5))),
                 'platnosc_karto': True}
        return param
    
    param_test = {'wiek': 18,
                  'num_produkt': 2,
                  't_na_prod': 1,
                  'platnosc_karto': True}
    
    test_klienty: list[Klient] = [ Klient(param=None) for _ in range(180) ]
    
    zb_kas = stworz_zb_kas(liczba_kas_obs=2, liczba_kas_samoobs=9)

    for klient in test_klienty:
        wybor_rodz_kas(zb_kas, klient)

    i = 0 


    # WYKMINIONA LOGIKA - TRZEBA ŁADNIE OPISAĆ !!
    while not (zb_kas['k_o'].war_koniec() and zb_kas['k_s'].war_koniec()):
        i += 1
        zb_kas['k_o'].aktualizacja_kas()
        zb_kas['k_s'].aktualizacja_kas()
        zb_kas['k_o'].odczekaj_tick_wszyscy(i)
        zb_kas['k_s'].odczekaj_tick_wszyscy(i)
        print("tick")
    print(i)
    
    print(f"Obsluzeni klienci k_o: {zb_kas['k_o'].ilosc_obsluzonych_klient}")
    print(f"Obsluzeni klienci k_s: {zb_kas['k_s'].ilosc_obsluzonych_klient}")

    print(f"Czas obslugi: {zb_kas['k_o'].infolist_czas_obslugi()[0]}")
    print(f"dlg kolejek lista: {zb_kas['k_o'].dlg_kolejek_interwal[0]}")
    
    print(f"Czas obslugi: {zb_kas['k_s'].infolist_czas_obslugi()[0]}")
    print(f"dlg kolejek lista: {zb_kas['k_s'].dlg_kolejek_interwal}")
    
    x = zb_kas['k_o'].dlg_kolejek_interwal[0][1]
    xx = zb_kas["k_o"].infolist_czas_obslugi()[0][1]
    plt.plot(xx)
    plt.show()
    
    
    # spr = [sum(x[1]) for x in zb_kasy_obs.infolist_czas_obslugi()]
    # print(f"spr: {spr}")
    print('end')
    
    

if __name__ == "__main__":
    test()
    # for i in range(5):
    #     print(f"\n\tTEST {i}")
    #     exponential_test()