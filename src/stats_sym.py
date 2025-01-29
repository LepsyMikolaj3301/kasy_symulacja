"""
Program z funkcjami statystycznymi potrzebnymi do symulacji

Potrzeba statystyk dotyczacych:

! do opisania !

"""
import numpy as np
import util_klasy as uk

def stats():
    # ŚREDNI CZAS OBSŁUGI KLIENTA (OBS/SOBS)
    mean_czas_na_klient__k_o = 0
    mean_czas_na_klient__k_s = 0
    # ŚREDNIA DLUGOSC KOLEJKI


if __name__ == '__main__':
    
    LAM = .035
    TIME = 40_500
    # dane z testów:  
    data_test = [uk.exponential_test(LAM, TIME) for i in range(200)]
    
    print(data_test)
    
    print(f"Srednia: {np.mean(data_test)}")
    print(f"Odch_std: {np.std(data_test)}")
    
        
    
    