from datetime import datetime, timedelta
import random
import pandas as pd 

global TPL, TPRBiodisiel, TPRDiesel_fosil


#DATOS
PROD_DIARIA = 100000 # en litros
DD = 0 #Demanda diaria

#CONTROL
DIESELF_limit_TO_RESTOCK = 80000 # en litros    
BIODIESEL_limit_TO_RESTOCK = 10000 # en litros 

CAPACIDAD_TANQUE_DIESEL_F = 4000000  #diesel fosil en litros
CAPACIDAD_TANQUE_BIODIESEL =  1000000
#lo producido de la refineria del diesel fosil + biodiesel
CAPACIDAD_TANQUE_PRODUCTO_FINAL =  4000000 # en litros

#ESTADO 
ST_DIESEL_F = CAPACIDAD_TANQUE_DIESEL_F/2  #en litros
ST_BIODIESEL = CAPACIDAD_TANQUE_BIODIESEL/2  #en litros
ST_PRODUCTO_F = 0   #en litros

#RESULTADO


#OTROS
TF = 10000 # en dias
DESP = 0
HV = 999999999999999999999999999


#CONTADORES
CDALEY = 0 #Contador de veces que se produjo combustible de acuerdo a la ley (97-3) 
CDNOALEY = 0 #Contador de veces que se produjo combustible no acuerdo a la ley (97-3) 
CLNOALEY = 0  #Contador de LITROS De combustible no acuerdo a la ley (97-3) 
CDPI = 0 #Cantidad de dias por produccion insuficiente
LT = 0 #Litros totales producidos de diesel para vender
DNOCDD = 0 #Dias que no se cumplio la demanada diaria 
PDR = 0

#TEF
TPRDiesel_fosil = HV #tiempo proximo reposicicion diesel fosil
TPRBiodisiel = HV #tiempo proximo reposicicion biodiesel 

#TIEMPOS


#auxs
def llenar_tanque_diesel_f(day):
    global ST_DIESEL_F, TPRDiesel_fosil
    ST_DIESEL_F = CAPACIDAD_TANQUE_DIESEL_F #se llena
    TPRDiesel_fosil = HV
    print("Dia: ", day, "Recarga de compusitble Diesel Fosil al maximo", CAPACIDAD_TANQUE_DIESEL_F)


def llenar_tanque_biodiesel(day):
    global ST_BIODIESEL, TPRBiodisiel
    ST_BIODIESEL = CAPACIDAD_TANQUE_BIODIESEL #se llena
    TPRBiodisiel = HV
    print("Dia: ", day, "Recarga de compusitble Biodiesel al maximo", CAPACIDAD_TANQUE_BIODIESEL)

def demanda_diaria():
    dd = random.randint(40000, 120000) # ENTRE 900.000 y 1.100.000 
    return dd

def get_desperdicio():
    return 0.02
# -------------------- INICIO SIMULACION ------------------------------------
def main():
    global TPRBiodisiel, TPRDiesel_fosil, ST_BIODIESEL, ST_DIESEL_F, ST_PRODUCTO_F, CDALEY, CDNOALEY, CLNOALEY, CDPI, LT, DNOCDD, PDR
    
    T = 0
    while(T <= TF):
        T = T + 1 
        if(T == TPRDiesel_fosil):
            llenar_tanque_diesel_f(day=T)
        if(T == TPRBiodisiel):
            llenar_tanque_biodiesel(day=T)
        DD = demanda_diaria()
           
        # logica de produccion    
        if(ST_DIESEL_F > PROD_DIARIA * 0.93): 
            if(ST_BIODIESEL > PROD_DIARIA * 0.07):
                ST_DIESEL_F = ST_DIESEL_F - (PROD_DIARIA * 0.93) #
                ST_BIODIESEL = ST_BIODIESEL - (PROD_DIARIA * 0.07)
                CDALEY = CDALEY + 1
                PDR = PROD_DIARIA
                print("DIA: ", T, " se produjo diesel con 97-3(ALEY) con ST_DF:", round(ST_DIESEL_F), " ST_BD:", round(ST_BIODIESEL) )
            elif((ST_DIESEL_F > PROD_DIARIA * 0.97) & (ST_BIODIESEL > PROD_DIARIA * 0.03)):
                ST_DIESEL_F = ST_DIESEL_F - (PROD_DIARIA * 0.97) #
                ST_BIODIESEL = ST_BIODIESEL - (PROD_DIARIA * 0.03)
                CDNOALEY = CDNOALEY + 1
                CLNOALEY = CLNOALEY + PROD_DIARIA
                PDR = PROD_DIARIA
            else:
                CDPI = CDPI + 1  
                if(ST_DIESEL_F > 0):
                    print("DIA: ", T, " se produjo diesel con 93-7(NOALEY) con ST_DF:", round(ST_DIESEL_F), " ST_BD:", round(ST_BIODIESEL) )

                    if()
                    PDR = round(ST_BIODIESEL / 0.07)
                    diesel_f_a_usar = max(PDR - ST_BIODIESEL, 0)
                    CDNOALEY = CDNOALEY + 1
                    CLNOALEY = CLNOALEY + PDR
                    if(ST_DIESEL_F > diesel_f_a_usar):
                        PDR = ST_DIESEL_F / 0.93
                        biodiesel_a_usar = PDR - ST_DIESEL_F
                        ST_DIESEL_F = 0     
                        ST_BIODIESEL = ST_BIODIESEL - biodiesel_a_usar
                        
                    else:
                        ST_DIESEL_F  = ST_DIESEL_F - diesel_f_a_usar
                        ST_BIODIESEL = 0
                else:
                    PDR = 0
        else:
            CDPI = CDPI + 1  
            if(ST_DIESEL_F > 0):
                print("DIA: ", T, " se produjo diesel con 93-7(NOALEY) con ST_DF:", round(ST_DIESEL_F), " ST_BD:", round(ST_BIODIESEL) )

                PDR = round(ST_BIODIESEL / 0.07)
                diesel_f_a_usar = max(PDR - ST_BIODIESEL, 0)
                
                CDNOALEY = CDNOALEY + 1
                CLNOALEY = CLNOALEY+ PDR
                if( ST_DIESEL_F > diesel_f_a_usar):
                    PDR = ST_DIESEL_F / 0.93
                    biodiesel_a_usar = PDR - ST_DIESEL_F
                    ST_DIESEL_F = 0     
                    ST_BIODIESEL = ST_BIODIESEL - biodiesel_a_usar
                    
                else:
                    ST_DIESEL_F  = ST_DIESEL_F - diesel_f_a_usar
                    ST_BIODIESEL = 0
            else:
                PDR = 0
        
        #
        desp = get_desperdicio()
        produccion_final = PDR - (PDR * desp)
        LT = LT + produccion_final        
        if(produccion_final + ST_PRODUCTO_F >= DD):
            ST_PRODUCTO_F =  min(ST_DIESEL_F + produccion_final - DD, CAPACIDAD_TANQUE_PRODUCTO_FINAL)
        else:
            DNOCDD = DNOCDD + 1 #no cumplio demanda diaria
            ST_PRODUCTO_F = 0
        
        if((ST_DIESEL_F < DIESELF_limit_TO_RESTOCK) & (TPRBiodisiel == HV)):
            TPRDiesel_fosil = T + 5 # REPOSICIONES TARDAN 1 DIA
        
        if((ST_BIODIESEL < BIODIESEL_limit_TO_RESTOCK) & (TPRBiodisiel == HV)):
            TPRBiodisiel = T + 5
         
    #RESULTADOS FINALES    
    PDNBP = (CDNOALEY/T) * 100
    PDNOCDD = (DNOCDD/T) * 100
    PLPNOALEY = (CDNOALEY/LT) * 100
    PDPI = (CDPI/T) * 100

    print("")
    print("--------------------SUMMARY-------------------")
    print("")
    
    print("Con variables de control: ") 
    
    print("Capacidad de tanque Biodiesel: ", CAPACIDAD_TANQUE_BIODIESEL)
    print("Capacidad de tanque Diesel fosil: ", CAPACIDAD_TANQUE_DIESEL_F)
    print("Capacidad de tanque Diesel producto final: ", CAPACIDAD_TANQUE_PRODUCTO_FINAL)
    
    print("cantidad de litros limite para pedir un restock de biodisel", BIODIESEL_limit_TO_RESTOCK)
    print("cantidad de litros limite para pedir un restock de diesel fosil", DIESELF_limit_TO_RESTOCK)

    print("")
    print("Resultados:")
    print("Porcentaje Dias No acuerdo a la norma (93-7) (PLPNOALEY)", round(PDNBP, 4), "%")
    print("Porcentaje de Dias no cumplio con Demanda Diaria(PDNOCDD)", round(PDNOCDD, 2), "%")
    print("Promedio Litros producidos No acuerdo a la norma (93-7) (PLPNOALEY) ", round(PLPNOALEY, 4))
    print("Promedio Dias con produccion insuficiente ", PDPI)
        
        





    # f = Fitter(df_arrivals_in_mins, distributions=['gamma', 'rayleigh', 'uniform'])
    # print(f.fit())
    # print(f.summary())
    # print(f.get_best())
    # print(f.get)

if __name__ == '__main__':
    main()