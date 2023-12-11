import random
from scipy.stats import truncnorm
from scipy.stats import dweibull


temp_baja = {'truncnorm': {'a': -0.401155164127462,
  'b': 52.7471338869295,
  'loc': 3.966592571578986,
  'scale': 7.395124973475845}}


temp_alta = {'dweibull': {'c': 2.247048292620673,
  'loc': 47.00547382992568,
  'scale': 17.526201091952437}}
#auxs
def get_cant_pedidos_x_dia_temp_baja():
    # Generate random numbers from the truncated normal distribution
    return truncnorm.ppf(random.random(), a= temp_baja['truncnorm']['a'],
                               b= temp_baja['truncnorm']['b'],
                               loc=temp_baja['truncnorm']['loc'],
                               scale=temp_baja['truncnorm']['scale']
                               )
    
def get_cant_pedidos_x_dia_temp_alta():
    # Generate random numbers from the truncated normal distribution
    return dweibull.ppf(random.random(), c= temp_alta['dweibull']['c'],
                               loc=temp_alta['dweibull']['loc'],
                               scale=temp_alta['dweibull']['scale']
                               )
    
def get_tam_pedido():
    return random.randint(1000, 2000)
    
def get_demanda_diaria_temp_baja():
    cant_pedidos = get_cant_pedidos_x_dia_temp_baja()
    demanda_diaria = 0 
    for i in range(int(cant_pedidos)):
        demanda_diaria = demanda_diaria + get_tam_pedido()
    return demanda_diaria

def get_demanda_diaria_temp_alta():
    cant_pedidos = get_cant_pedidos_x_dia_temp_alta()
    demanda_diaria = 0 
    for i in range(int(cant_pedidos)):
        demanda_diaria = demanda_diaria + get_tam_pedido()
    return demanda_diaria

# -------------------- INICIO SIMULACION ------------------------------------
def main():
    print(get_demanda_diaria_temp_baja())
    print(get_demanda_diaria_temp_alta())


if __name__ == '__main__':
    main()