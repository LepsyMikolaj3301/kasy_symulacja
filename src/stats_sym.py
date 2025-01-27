"""
Program z funkcjami statystycznymi potrzebnymi do symulacji

Potrzeba statystyk dotyczacych:

! do opisania !

"""
import numpy as np
import util_klasy as uk


if __name__ == '__main__':
    
    LAM = .035
    TIME = 40_500
    # dane z testów:  
    data_test = [uk.exponential_test(LAM, TIME) for i in range(200)]
    
    print(data_test)
    
    print(f"Srednia: {np.mean(data_test)}")
    print(f"Odch_std: {np.std(data_test)}")
    
        
    
    