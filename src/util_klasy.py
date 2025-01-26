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

# STAŁE GLOBALNE
STALA_PAKOWANIA = 0.5  # mniej więcej określenie, ile pakuje się jeden produkt
STALA_PLT_KARTO = 7  # czas zapłacenia kartą
STALA_PLT_GOTOWKO = 14  # czas zapłacenia gotówką
STALA_KASOWANIA_EKSPERT = 2  # czas skasowania jednego produktu przez kasjera


class Klient:
    """
    Klasa będzie służyła jako bardziej kontener informacji ( struct )
    """

    def __init__(self, param):
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
                czas_skan = normal(4.5, 1)
                if czas_skan >= 2:  # Akceptujemy tylko wartości > 2, bo klienci szybciej nie skanują
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
            self.wiek = '0'
            self.num_produkt = param['num_produkt']
            self.t_na_prod = param['t_na_prod']
            self.platnosc_karto = param['platnosc_karto']
        else:
            self.wiek = random_age()
            self.wielk_zakupow = random_groceries_size(self.wiek)
            self.num_produkt = random_groceries_amount(self.wielk_zakupow)
            self.t_na_prod = czas_skan_bez_ujemnych()
            self.platnosc_karto = czy_karta(self.wiek)




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
            return STALA_PAKOWANIA * self.initial_ilosc_prod + STALA_PLT_KARTO

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

    def klienci_do_kolejki(self, klient: Klient):
        self.kolejka.put(klient)

    def odczekaj_tick_wszyscy(self):
        for i in range(self.ilosc_kas):
            self.lista_kas[i].odczekaj_tick()

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
        


# !!
# CZĘŚĆ KAS OBSŁUGOWYCH
# 
# 
class KasaObslugowa:
    def __init__(self):

        self.t_na_produkt = STALA_KASOWANIA_EKSPERT
        
        self.lista_czasow_obslugi = []
        # GIGA WAŻNE - LICZNIK, ILE TICKÓW ZOSTAŁO DO PRZECZEKANIA
        self.realny_czas_counter = 0

        # WARTOŚĆ MÓWIĄCA NAM CZY KLIENT OBSLUGUJE KASE
        self.is_with_klient = False

    def przyjmij_klienta(self, klient: Klient):

        # Resetujemy wartość, czyli nowy klient jest obsługiwany
        self.is_with_klient = True
        self.initial_ilosc_prod = klient.num_produkt
        self.rodzaj_platnosci = STALA_PLT_KARTO if klient.platnosc_karto else STALA_PLT_GOTOWKO

        # roznica czyli czy pakowanie zajmie mi dłużej niż kasowanie kasjerki
        roznica = (STALA_PAKOWANIA * self.initial_ilosc_prod) - (self.t_na_produkt * self.initial_ilosc_prod)

        # czas po zakończeniu kasowania
        self.kasa_checkout = self.rodzaj_platnosci + (0 if roznica <= 0 else roznica)

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
        self.ilosc_obsluzonych_klient = 0

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

    def odczekaj_tick_wszyscy(self):
        # Odczekujemy po wszystkich kasach TICK
        for i in range(self.ilosc_kas):
            self.lista_kasa_x_kolejka[i][0].odczekaj_tick()

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
                self.lista_kasa_x_kolejka[i][0].przyjmij_klienta(self.lista_kasa_x_kolejka[i][1].get())

def czas_nast_klient(lamb: float) -> int:
    # wylosuj ilosc sekund do przyjscia nastepnego klienta
    return round(exponential(1/lamb))

def test_exp():
    # dla takiej wartości w miare działa, ale wciąż są potrzebne dokładniejsze badania
    # ok. 350 klientów na 3600 sekund
    LAM = 0.1
    # zmienne
    klient_counter = 0
    next_klient_count = 0
    
    for i in range(3600):
        if next_klient_count <= 0:
            next_klient_count = czas_nast_klient(LAM)
            klient_counter += 1
        next_klient_count -= 1
    print(f"Klient counter: {klient_counter}")

def test():
    """
    DO TESTOWANIA GŁÓWNEJ LOGIKI
    """
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
    
    test_klienty: Klient = [ Klient(param=param_test_gen()) for _ in range(180) ]
    
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
    print(i)
    print('end')
    
    

if __name__ == "__main__":
    # test()
    test_exp()