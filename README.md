# kasy_symulacja
Program symulujący kasy samoobsługowe oraz kasy zwykłe, rozstrzygając do jakiej sie powinno iść w odpowiadających warunkach xd

## Architektura ##

**1. Struktura sklepu ( *main loop* )**
    Struktura sklepu będzie generatorem zawierającym wszystkie inne instancje 
    * **Kasa** to będzie obiekt (lista obiektów dla wielu ) klasy *kasa* który będzie sprecyzowany: samoobsługowa albo zwykła. Jako argument będą brały kolejnych klientów z **kolejki**
    * **kolejka** to zwykła kolejka z biblioteki ` collections - queue`, która będzie w czasie rzeczywistym przydzielać klientów
    * **Klient** będzie generowany w czasie rzeczywistym, czas przyjścia kolejnego klienta zależny od rozkładu wykładniczego

## Jakie rozkłady do czego ##
    dupsko, trzeba zaprojektować

## Ważne strony pomocnicze ##
    [Strona z prostą symulacją](https://realpython.com/simpy-simulating-with-python/)

    *potrzeba kolejnych stron*

## Podział ##

