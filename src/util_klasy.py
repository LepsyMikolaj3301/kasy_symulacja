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
- dodanie stałej płacenia kartą i gotówką
- napisanie klas kolejkowo-zbiorowych      
"""
import random
from queue import Queue
import numpy as np

# STAŁE GLOBALNE
STALA_PAKOWANIA = 0.025  # mniej więcej określenie, ile pakuje się jeden produkt
STALA_PLT_KARTO = 0  # DO DODANIA, PROSZE UZUPEŁNIĆ
STALA_PLT_GOTOWKO = 0  # TO TEŻ
STALA_KASOWANIA_EKSPERT = 0  # TO KURWA TEŻ XD


class Klient:
    """
    Klasa będzie służyła jako bardziej kontener informacji ( struct )
    """

    def __init__(self, wiek, num_produkt,
                 t_na_prod: float, platnosc_karto: bool):
        """
        Args:
            wiek (int): Wiek podawany z rozkładu normalnego dla demografii miast
            num_produkt (int): Generowany w zaleznosci od wieku i rodzaju dnia (duzy/maly ruch -> duze/male zakupy ale z dużym odch std)
            t_na_prod (float): Czas na produkt może być losowany, ale po przemnożeniu w klasie Kasa ( musi być zaokrąglony do INT), bowiem tick (odstęp czasowy) to 1 minuta
            platnosc_karto (bool): Płatność kartą - zależne od wieku
        """

        # Funkcja losująca przedział wiekowy
        def random_age():
            # Dane populacji dla przedziałów wiekowych w 2022 roku (dane Urzędu statystycznego we Wrocławiu)
            age_ranges = {
                "18-24": 30313 + (22382 * 5 / 2),  # 20-24 + 5/2 z 15-19
                "25-34": 56144 + 65721,  # 25-29 + 30-34
                "35-44": 67650 + 57518,  # 35-39 + 40-44
                "45-54": 46934 + 33833,  # 45-49 + 50-54
                "55-64": 29720 + 34885,  # 55-59 + 60-64
                "65+": 42417 + 38473 + 21639 + 15164 + 17874  # 65-69, 70-74, 75-79, 80-84, 85+
            }

            # Cała populacja Wrocławia
            total_population = 674079

            # Wyliczanie prawdopodobieństw dla każdego przedziału wiekowego
            age_probabilities = {age: count / total_population for age, count in age_ranges.items()}

            return random.choices(list(age_probabilities.keys()), weights=list(age_probabilities.values()))[0]

        def random_groceries_size(wiek):

            prawdopodobne_wielkosci_zakupow = {
                "18-24": {"duze": 0.13, "srednie": 0.27, "male": 0.37, "random": 0.08},
                "25-34": {"duze": 0.13, "srednie": 0.38, "male": 0.31, "random": 0.1},
                "35-44": {"duze": 0.12, "srednie": 0.41, "male": 0.32, "random": 0.08},
                "45-54": {"duze": 0.12, "srednie": 0.34, "male": 0.38, "random": 0.07},
                "55-64": {"duze": 0.07, "srednie": 0.28, "male": 0.47, "random": 0.06},
                "65+": {"duze": 0.07, "srednie": 0.24, "male": 0.43, "random": 0.07}
            }

            wielkosci = list(prawdopodobne_wielkosci_zakupow[wiek].keys())  # np. ["duze", "srednie", "male", "random"]
            prawdopodobienstwa = list(prawdopodobne_wielkosci_zakupow[wiek].values())  # np. [0.13, 0.27, 0.37, 0.08]

            # Losowanie wielkości zakupów
            return random.choices(wielkosci, prawdopodobienstwa)

        def random_groceries_amount(size):

            zakresy_ilosci_produktow = {
                "male": {"min": 1, "max": 10},
                "srednie": {"min": 11, "max": 25},
                "duze": {"min": 26, "max": 50},
                "random": {"min": 1, "max": 50}
            }

            minimum = zakresy_ilosci_produktow[size]["min"]
            maximum = zakresy_ilosci_produktow[size]["max"]

            return round(random.uniform(minimum, maximum))

        def czas_skan_bez_ujemnych():
            number_generated = False

            while not number_generated:
                czas_skan = np.random.normal(4.5, 1)
                if czas_skan >= 2:  # Akceptujemy tylko wartości > 2, bo klienci szybciej nie skanują
                    number_generated = True

            return czas_skan

        self.wiek = random_age()
        self.wielk_zakupow = random_groceries_size(self.wiek)
        self.num_produkt = random_groceries_amount(self.wielk_zakupow)
        self.t_na_prod = czas_skan_bez_ujemnych()
        self.platnosc_karto = platnosc_karto


def generate_parametry() -> list:
    """
    funkcja do generowania klienta na początku Iteracji

    Args:
        num_klient (int, optional): liczba klientów do wygenerowania. Defaults to 0.

    Returns:
        list: lista wygenerowanych klientów ( albo pusta lista )
    """

    # Tu generowanie z rozkładów odpowiednich parametrów

    # Tu osobno wygenerowanie przypadku, gdy zakładamy, że wszyscy płacą kartą
    if wszyscy_karto:
        platnosc_karto = True
    else:
        pass  # to do wywalenia gdy poniższe gotowe
        # platnosc_karto = ... i tam jakiś rozkład XD

    # Tu stworzenie obiektów jako listy klientów z zakupami

    # nowi_klienci = [Klient( . . . ) for _ in range(num_klient)]
    # return nowi_klienci


class KasaSamoobslugowa:
    def __init__(self, klient: Klient):
        self.initial_ilosc_prod = klient.num_produkt
        self.t_na_produkt = klient.t_na_prod

        # czas po zakończeniu kasowania
        self.kasa_checkout = self.checkout_time()

        # GIGA WAŻNE - OBLICZENIE WSTĘPNE OBSŁUŻENIA KASY:
        self.przewidywany_czas_obslugi = round(
            self.t_na_produkt * self.initial_ilosc_prod + self.kasa_checkout)
        # GIGA WAŻNE 2 - LICZNIK, ILE TICKÓW ZOSTAŁO DO PRZECZEKANIA
        self.realny_czas = self.przewidywany_czas_obslugi

        # WARTOŚĆ MÓWIĄCA NAM CZY KLIENT SKONCZYL OBSLUGIWANIE KASY
        self.kasa_done = False

    def checkout_time(self):
        return STALA_PAKOWANIA * self.initial_ilosc_prod + STALA_PLT_KARTO

    def odczekaj_tick(self):
        # Ta funkcja nam zwróci wartość True, jeżeli klient został obsłużony
        if self.realny_czas <= 0:
            self.kasa_done = True
        # Inaczej, odczekaj jeden tick
        self.realny_czas -= 1


class ZbiorKasySamoobslugowe:
    def __init__(self, ilosc_kas):
        self.kolejka = Queue()
        self.ilosc_kas = ilosc_kas
        self.zajete_kasy = 0
        self.ilosc_obsluzonych_klient = 0
        self.lista_kas = []

    def klienci_do_kolejki(self, klienci: list):
        for klient in klienci:
            self.kolejka.put(klient)

    def aktualizacja_kas(self):
        """
        Ta metoda:
        1. Usuwa klientów którzy skonczyli zakupy
        2. Dodaje klientów do pustych kas
        """

        # ponizsza petla sprawdza czy klient posłużyl sie kasą i zapisuje informacje
        for i, kasa in enumerate(self.lista_kas):
            if kasa.kasa_done:
                self.lista_kas.pop(i)
                self.zajete_kasy -= 1
                self.ilosc_obsluzonych_klient += 1

        # Przydzielanie klientow z kolejki do kasy
        while self.zajete_kasy < self.ilosc_kas + 1:
            # Do miejsca z kasami, zostaje dodana kasa Samoobsługowa i do niej przydzielony zostaje klient
            # Czyli za każdym razem tworzymi nową instancję
            self.lista_kas.append(KasaSamoobslugowa(self.kolejka.get()))
            self.zajete_kasy += 1


# !!
# Nie tworzymy osobnych instancji - zrobienie nowych metod przyjmij_klienta() które obsługują klienta i iterują informacje

class KasaObslugowa:
    def __init__(self):
        self.initial_ilosc_prod = klient.num_produkt
        self.t_na_produkt = STALA_KASOWANIA_EKSPERT
        self.rodzaj_platnosci = STALA_PLT_KARTO if klient.platnosc_karto else STALA_PLT_GOTOWKO

        # roznica czyli czy pakowanie zajmie mi dłużej niż kasowanie kasjerki
        roznica = (STALA_PAKOWANIA * self.initial_ilosc_prod) - (self.t_na_produkt * self.initial_ilosc_prod)

        # czas po zakończeniu kasowania
        self.kasa_checkout = self.rodzaj_platnosci + (0 if roznica <= 0 else roznica)

        # GIGA WAŻNE - OBLICZENIE WSTĘPNE OBSŁUŻENIA KASY:
        self.przewidywany_czas_obslugi = round(self.t_na_produkt * self.initial_ilosc_prod + self.kasa_checkout)
        # GIGA WAŻNE 2 - LICZNIK, ILE TICKÓW ZOSTAŁO DO PRZECZEKANIA
        self.realny_czas = self.przewidywany_czas_obslugi

        # WARTOŚĆ MÓWIĄCA NAM CZY KLIENT SKONCZYL OBSLUGIWANIE KASY
        self.kasa_done = False

    def odczekaj_tick(self):
        if self.realny_czas <= 0:
            self.kasa_done = True

        self.realny_czas -= 1


class ZbiorKasyObslugowe:
    def __init__(self, ilosc_kas):
        self.ilosc_kas = ilosc_kas
        self.ilosc_obsluzonych_klient = 0
        self.lista_kasa_x_kolejka = [(KasaObslugowa(), Queue())
                                     for _ in range(ilosc_kas)]

    # def klienci_do_kolejki(self, klienci: list):


def test():
    """
    DO TESTOWANIA
    """


if __name__ == "__main__":
    test()
