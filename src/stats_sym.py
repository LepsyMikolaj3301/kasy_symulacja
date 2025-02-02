"""
Program z funkcjami statystycznymi potrzebnymi do symulacji

Potrzeba statystyk dotyczacych:

! do opisania !

"""
import numpy as np
import util_klasy as uk
from matplotlib import pyplot as plt
from numpy.random import gamma
from scipy.stats import gamma as gamma_p
from math import sin
def stats():
    # ŚREDNI CZAS OBSŁUGI KLIENTA (OBS/SOBS)
    mean_czas_na_klient__k_o = 0
    mean_czas_na_klient__k_s = 0
    # ŚREDNIA DLUGOSC KOLEJKI
   
def int_dist_gamma(t: int, k_0: float, scale: float, amp: float, omega: float):
    k_t = k_0 * (1 + amp*sin(omega*t))
    return round(gamma())

def gmma_test():
    
    

    # Parametry rozkładu gamma
    shape = 1 # k (kształt)
    scale = 0.23  # θ (skala)
    # Zakres wartości x
    x = np.linspace(0, 10, 1000)

    # Funkcja gęstości prawdopodobieństwa (PDF) rozkładu gamma
    pdf = gamma.pdf(x, a=shape, scale=scale)

    # Rysowanie wykresu
    plt.figure(figsize=(8, 5))
    plt.plot(x, pdf, label=f'Gamma PDF (k={shape}, θ={scale})', color='blue')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Funkcja gęstości prawdopodobieństwa rozkładu gamma')
    plt.legend()
    plt.grid(True)
    plt.show()
 
def test_kurwa(lam, czas):
    
    interwal = 5
    klienci_x = []
    kl = 0

    
    next_klient_count = 0
    for i in range(czas):
        if next_klient_count <= 0:
            kl += 1
            # next_klient_count = uk.int_dist_exp_sin(i, lam, 3, 0.1)
            # uk.int_dist_exp_sin(i, lam, 0.8,1)
            # uk.int_dist_exp(0.033)
            while (next_klient_count := uk.int_dist_exp_sin(i, lam, 0.8,1)) == 0:
                kl += 1
        next_klient_count -= 1
        if i % interwal == 0:
            klienci_x.append(kl)
            kl = 0
    # print(klienci_x)
    print(f"Suma: {sum(klienci_x)}")
    
    
    return klienci_x
    
            
    
        

def rozklad_test(lam: float, czas: int) -> int:
    # dla takiej wartości w miare działa, ale wciąż są potrzebne dokładniejsze badania
    # ok. 350 klientów na 3600 sekund
    
    # zmienne
    klient_counter = 0
    next_klient_count = 0
    walrus = 0
    
    for i in range(czas):
        if next_klient_count <= 0:
            klient_counter += 1
            while (next_klient_count := uk.int_dist_exp(lam)) == 0:
                walrus += 1
                klient_counter += 1
        next_klient_count -= 1
        
    # print(walrus)
    
    return (klient_counter, walrus)


if __name__ == '__main__':
    
    LAM = [0.12]
    TIME = 57_500
    def plocik(kl_info):
        plt.plot(kl_info)
        plt.show()
        
    # dane z testów:
    for l in LAM:
        testy = []
        for i in range(1000):
            kl_info = test_kurwa(l, TIME)
            
            testy.append(sum(kl_info))
            # plocik(kl_info)
        print(f"L = {l}")
        print(f"Srednia: {np.mean(testy)}")
        print(f"Odch_std: {np.std(testy)}")
        
    # gmma_test()
    
    
    # data_test = [rozklad_test(LAM, TIME) for _ in range(200)]
    
    # print(data_test)
    # data_test_0 = [dt[0] for dt in data_test ]
    
        
    
    