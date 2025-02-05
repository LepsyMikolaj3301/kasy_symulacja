# kasy_symulacja - Symulacja transakcji klient-sklep
Program symulujący kasy samoobsługowe oraz kasy zwykłe na podstawie dostępnych danych z badań. Program symuluje przejście wygenerowanego klienta z rozkładu wykładniczego, który następnie "wybiera" do którego rodzaju kas będzie chciał przystąpić. Klient ten następnie czeka w kolejce i skanuje lub czeka na skanowanie jego produktów przez kasjera.
\
Przeprowadzenie symulacji polega na zautomatyzowanym procesie puszczania kilku rodzajów symulacji, wg danych wymagań.
\
**NOTE:** This Project is in Polish, for a polish project in collaboration with Paola. The polish language is used for more clarified description of the simulation.

## Architektura
**1. Struktura sklepu**
Sklep zawiera 2 rodzaje kas: kasy samoobsługowe oraz obsługowe. Jeżeli założymy liczbe kolejek do kas obsługowych jako N, a do samoobsługowej ( 1 kolejka ) jako N_s, to wzorem wg którego klient wybiera kase to: 
min(N, N_s) -> przydziel_klienta_do_kolejki() 
\
Architektura wizualnie ( 3 kasy obs. 3 kasy samoobs.):\
` |Kasa obs| ..... `\
` |Kasa obs| ... `\
` |Kasa obs| .... `\
` |k_s| |k_s| |k_s|`\
`   .     .     .      ......`\

## Jakie rozkłady do czego
Do losowania klientów został wykorzystany rozkład wykładniczy z użyciem efektu sinusoidalnego znanego z wachadła matematycznego
\
$$
f(x; \lambda) = \lambda e^{-\lambda x}, \quad x \geq 0, \lambda > 0  \\
\lambda (t) = \lambda_0(1 + Asin(\omega t))^2
$$
\
Do losowania parametrów klienta wykorzystujemy rozkład ważony na podstawie demografii miasta _Wrocław_ oraz rozkłady uznane wg naszego uznania, bo pasowały

## Źródła
<https://wroclaw.stat.gov.pl/files/gfx/wroclaw/pl/defaultstronaopisowa/1880/1/2/dz_5_ludnosc_2023.pdf>
<https://www.cbos.pl/SPISKOM.POL/2013/K_094_13.PDF>
<https://static.nbp.pl/systemy/platniczy/Zwyczaje-platnicze-w-Polsce-2023.pdf>
<https://bank.pl/na-zakupy-najlepiej-bez-gotowki/>
