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
 
def test_nowy_rozklad(czas, lam, amplituda, czest):
    
    interwal = uk.INTERWAL
    klienci_x = []
    kl = 0

    
    next_klient_count = 0
    for i in range(czas):
        if next_klient_count <= 0:
            kl += 1
            # next_klient_count = uk.int_dist_exp_sin(i, lam, 3, 0.1)
            # uk.int_dist_exp_sin(i, lam, 0.8,1)
            # uk.int_dist_exp(0.033)
            # uk.int_dist_exp_sin(i, lam, amplituda, czest)
            while (next_klient_count := uk.int_dist_exp_sin(i, lam, amplituda, czest)) == 0:
                kl += 1
        next_klient_count -= 1
        if i % interwal == 0:
            klienci_x.append(kl)
            kl = 0
    # print(klienci_x)
    # print(f"Suma: {sum(klienci_x)}")
    
    
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
    
    LAM = [0.081, 0.158]
    amplit = [0.765, 0.765]
    czestot = [1, 1]
    TIME = 57_600
    def plocik(kl_info):
        plt.plot(kl_info)
        plt.show()
        
    def plocik_double(kl_1, kl_2):
        figure, axis = plt.subplots(1, 2)
        axis[0].plot(kl_1)
        axis[0].set_title('kl_1')
        axis[1].plot(kl_2)
        axis[1].set_title('kl_2')
        plt.show()
        
    # dane z testów:
    for j in range(2):
        testy_1, testy_2 = [], []
        for i in range(1000):
            kl_info = test_nowy_rozklad(TIME, LAM[j], amplit[j], czestot[j])
            # kl_info_2 = test_nowy_rozklad(TIME, LAM[1], amplit[1], czestot[1])
            testy_1.append(sum(kl_info))
            # testy_2.append(sum(kl_info_2))
            # plocik_double(kl_info, kl_info_2)
            # plocik(kl_info)
        # print(f"L = {LAM[j]}")
        
        print(f"Srednia: {np.mean(testy_1)}")
        print(f"Odch_std: {np.std(testy_1)}")
        
    # gmma_test()
    
    
    # data_test = [rozklad_test(LAM, TIME) for _ in range(200)]
    
    # print(data_test)
    # data_test_0 = [dt[0] for dt in data_test ]
    
        
    
    