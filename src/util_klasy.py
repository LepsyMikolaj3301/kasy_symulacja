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

    Dodatkowo:

TODO:
- dodanie stałej płacenia kartą i gotówką
- napisanie klas kolejkowo-zbiorowych      
"""
import random
from queue import Queue


# STAŁE GLOBALNE
STALA_PAKOWANIA = 0.025  # mniej więcej określenie, ile pakuje się jeden produkt
STALA_PLT_KARTO = 0  # DO DODANIA, PROSZE UZUPEŁNIĆ
STALA_PLT_GOTOWKO = 0  # TO TEŻ
STALA_KASOWANIA_EKSPERT = 0  # TO KURWA TEŻ XD


def generate_klient(wszyscy_karto: bool, num_klient=0) -> list:
    """
    funkcja do generowania klienta na początku Iteracji

    Args:
        num_klient (int, optional): liczba klientów do wygenerowania. Defaults to 0.

    Returns:
        list: lista wygenerowanych klientów ( albo pusta lista )
    """

    # Od razu zwrócenie pustej listy, by zoptymalizować
    if num_klient == 0:
        return []

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


class Klient:
    """
    Klasa będzie służyła jako bardziej kontener informacji ( struct ) 
    """

    def __init__(self, wiek, num_produkt, t_na_prod: float, platnosc_karto: bool):
        """
        Args:
            wiek (int): Wiek podawany z rozkładu normalnego dla demografii miast
            num_produkt (int): Generowany w zaleznosci od wieku i rodzaju dnia (duzy/maly ruch -> duze/male zakupy ale z dużym odch std)
            t_na_prod (float): Czas na produkt może być losowany, ale po przemnożeniu w klasie Kasa ( musi być zaokrąglony do INT), bowiem tick (odstęp czasowy) to 1 minuta
            platnosc_karto (bool): Płatność kartą - zależne od wieku 
        """
        self.wiek = wiek
        self.num_produkt = num_produkt
        self.t_na_prod = t_na_prod
        self.platnosc_karto = platnosc_karto


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

        self.lista_czasow_obslugi.append(self.czas_obslugi)

        # nadanie counterowi nowego czasu, nowego klienta
        self.realny_czas_counter = self.czas_obslugi
    
    def odczekaj_tick(self):
        # Ta funkcja nam zwróci wartość True, jeżeli klient został obsłużony
        if self.realny_czas_counter <= 0:
            self.is_with_klient = False
        # Inaczej, odczekaj jeden tick
        self.realny_czas_counter -= 1


class ZbiorKasySamoobslugowe:
    def __init__(self, ilosc_kas):
        self.kolejka = Queue()
        self.lista_kas = [KasaSamoobslugowa() for _ in range(ilosc_kas)] 
        self.ilosc_kas = ilosc_kas

    def klienci_do_kolejki(self, klient: Klient):
        self.kolejka.put(klient)

    def odczekaj_tick_wszyscy(self):
        for i in range(self.ilosc_kas):
            self.lista_kas[i].odczekaj_tick()


    def aktualizacja_kas(self):
        """
        Ta metoda:
        1. Sprawdza czy kasa jest pusta, jak jest - dodaje klienta
        """
        for i, kasa in enumerate(self.lista_kas):
            if not kasa.is_with_klient:
                self.lista_kas[i].przyjmij_klienta(self.kolejka.get())
        

# !! 
# Nie tworzymy osobnych instancji - zrobienie nowych metod przyjmij_klienta() które obsługują klienta i iterują informacje

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

        self.lista_czasow_obslugi.append(self.czas_obslugi)

        # nadanie counterowi nowego czasu, nowego klienta
        self.realny_czas_counter = self.czas_obslugi


    def odczekaj_tick(self):

        if self.realny_czas_counter <= 0:
            self.is_with_klient = False

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
        for i in range(self.ilosc_kas):
            self.lista_kasa_x_kolejka[i][0].odczekaj_tick()

    def aktualizacja_kas(self):
        """
        Ta metoda:
        1. Sprawdza czy kasa jest pusta, jak jest - dodaje klienta
        """
        for i, kasa_kolejka in enumerate(self.lista_kasa_x_kolejka):
            if not kasa_kolejka[0].is_with_klient:
                self.lista_kasa_x_kolejka[i][0].przyjmij_klienta(self.lista_kasa_x_kolejka[i][1].get())

            

def test():
    """
    DO TESTOWANIA
    """

if __name__ == "__main__":
    test()
