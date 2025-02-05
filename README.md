# kasy_symulacja - Symulacja transakcji klient-sklep
Program symulujący kasy samoobsługowe oraz kasy zwykłe na podstawie dostępnych danych z badań. Program symuluje przejście wygenerowanego klienta z rozkładu wykładniczego, który następnie "wybiera" do którego rodzaju kas będzie chciał przystąpić. Klient ten następnie czeka w kolejce i skanuje lub czeka na skanowanie jego produktów przez kasjera.

Przeprowadzenie symulacji 
## Architektura

**1. Struktura sklepu**
    Struktura sklepu będzie generatorem zawierającym wszystkie inne instancje 
    * **Kasa** to będzie obiekt (lista obiektów dla wielu ) klasy *kasa* który będzie sprecyzowany: samoobsługowa albo zwykła. Jako argument będą brały kolejnych klientów z **kolejki**
    * **kolejka** to zwykła kolejka z biblioteki `collections - queue`, która będzie w czasie rzeczywistym przydzielać klientów
    * **Klient** będzie generowany w czasie rzeczywistym, czas przyjścia kolejnego klienta zależny od rozkładu wykładniczego

## Jakie rozkłady do czego


## Ważne strony pomocnicze

## Podział

