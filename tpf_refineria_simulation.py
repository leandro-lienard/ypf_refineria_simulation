from datetime import datetime, timedelta
import random
import pandas as pd 
import demanda_diaria as dd

global TPL, TPRBiodisiel, TPRDiesel_fosil


#DATOS
PROD_DIARIA = 75000 # TOCAR
DD = 0 #Demanda diaria

#CONTROL
CAPACIDAD_TANQUE_BIODIESEL =  200000 #NO TOCAR 
CAPACIDAD_TANQUE_DIESEL_F = 2000000  #NO TOCAR  diesel fosil en litros o 4000 m³
CAPACIDAD_TANQUE_PRODUCTO_FINAL =  500000 # NO TOCAR en litros

BIODIESEL_limit_TO_RESTOCK = 40000 # TOCAR
DIESELF_limit_TO_RESTOCK = 400000 # TOCAR    
#lo producido de la refineria del diesel fosil + biodiesel

#ESTADO #siempre asi 
ST_DIESEL_F = CAPACIDAD_TANQUE_DIESEL_F/2  #en litros  
ST_BIODIESEL = CAPACIDAD_TANQUE_BIODIESEL/2  #en litros
ST_PRODUCTO_F = 0   #en litros

#RESULTADO


#OTROS
TF = 10000 # en dias
DESP = 0.02
HV = 999999999999999999999999999


#CONTADORES
CDALEY = 0 #Contador de veces que se produjo combustible de acuerdo a la ley (97-3) 
CDNOALEY = 0 #Contador de veces que se produjo combustible no acuerdo a la ley (97-3) 
CLNOALEY = 0  #Contador de LITROS De combustible no acuerdo a la ley (97-3) 
CDDI = 0 #Cantidad de dias por produccion insuficiente
LT = 0 #Litros totales producidos de diesel para vender
DNOCDD = 0 #Dias que no se cumplio la demanada diaria 
PDR = 0
CDNP = 0 # Cantidad dias no produccion
CLALEY = 0
EXCEDENTE_PF = 0

#TEF
TPRDiesel_fosil = HV #tiempo proximo reposicicion diesel fosil
TPRBiodisiel = HV #tiempo proximo reposicicion biodiesel 

#TIEMPOS


#auxs
def llenar_tanque_diesel_f(day):
    global ST_DIESEL_F, TPRDiesel_fosil, CAPACIDAD_TANQUE_BIODIESEL
    ST_DIESEL_F = min(CAPACIDAD_TANQUE_DIESEL_F, ST_DIESEL_F + 400000) #se llena
    TPRDiesel_fosil = HV
    print("Dia: ", day, "Recarga de compusitble Diesel Fosil al maximo", CAPACIDAD_TANQUE_DIESEL_F)


def llenar_tanque_biodiesel(day):
    global ST_BIODIESEL, TPRBiodisiel
    ST_BIODIESEL = min(CAPACIDAD_TANQUE_DIESEL_F, ST_BIODIESEL + 400000) #se llena
    TPRBiodisiel = HV
    print("Dia: ", day, "Recarga de compusitble Biodiesel al maximo", CAPACIDAD_TANQUE_BIODIESEL)

def demanda_diaria(day):
    # if day % 365 < 90:
    return dd.get_demanda_diaria_temp_alta()
    # return dd.get_demanda_diaria_temp_baja()

def get_desperdicio():
    return 0.02

def produccion_alternativa(day):
    global ST_DIESEL_F, ST_BIODIESEL, CDNOALEY, CLNOALEY, CDNP, CLALEY, ST_PRODUCTO_F
    PDR = 0
    P_MAX_Diesel_F = ST_DIESEL_F/0.97 # PRODUCCION REBAJADA
    P_MAX_Biodiesel = ST_BIODIESEL/0.03 
    
    
    if(P_MAX_Diesel_F >= P_MAX_Biodiesel):
        print("DIA: ", day, "Se produjo diesel con 100% (NOALEY) con ST_DF:", round(ST_DIESEL_F), " ST_BD:", round(ST_BIODIESEL) )
        #produzco al 100% DF
        PDR = ST_DIESEL_F
        ST_DIESEL_F = 0
        CLNOALEY = CLNOALEY + PDR 
        CDNOALEY = CDNOALEY + 1
    else:
        print("DIA: ", day, "NO PRODUCCION con ST_DF:", round(ST_DIESEL_F), " ST_BD:", round(ST_BIODIESEL), "ST_PF", round(ST_PRODUCTO_F))
        
        #no produccion
        PDR = 0
        CDNP = CDNP + 1
    return PDR

# -------------------- INICIO SIMULACION ------------------------------------
def main():
    global TPRBiodisiel, TPRDiesel_fosil, ST_BIODIESEL, ST_DIESEL_F, ST_PRODUCTO_F, CDALEY, CDNOALEY, CLNOALEY 
    global CDDI, LT, DNOCDD, PDR, CLALEY, EXCEDENTE_PF
    
    T = 0
    while(T <= TF):
        T = T + 1 
        if(T == TPRDiesel_fosil):
            llenar_tanque_diesel_f(day=T)
        if(T == TPRBiodisiel):
            llenar_tanque_biodiesel(day=T)
        DD = demanda_diaria(day=T)
           
        # logica de produccion    
        if(ST_DIESEL_F > PROD_DIARIA * 0.93): 
            if(ST_BIODIESEL > PROD_DIARIA * 0.07):
                ST_DIESEL_F = ST_DIESEL_F - (PROD_DIARIA * 0.93) #
                ST_BIODIESEL = ST_BIODIESEL - (PROD_DIARIA * 0.07)
                CDALEY = CDALEY + 1
                CLALEY = CLALEY + PROD_DIARIA
                PDR = PROD_DIARIA
                print("DIA: ", T, " se produjo diesel con 93-7(ALEY) con ST_DF:", round(ST_DIESEL_F), " ST_BD:", round(ST_BIODIESEL), "DD:", DD)
            elif(ST_DIESEL_F >= PROD_DIARIA):
                #PRODUZCO AL 100%
                ST_DIESEL_F = ST_DIESEL_F - PROD_DIARIA
                CDNOALEY = CDNOALEY + 1
                CLNOALEY = CLNOALEY + PROD_DIARIA
                PDR = PROD_DIARIA
            else:
                PDR = produccion_alternativa(day=T)
        else:
            PDR = produccion_alternativa(day=T)
        #
        desp = get_desperdicio()
        produccion_final = PDR - (PDR * desp)
        LT = LT + PDR        
        if(produccion_final + ST_PRODUCTO_F >= DD):
            ST_PRODUCTO_F = ST_PRODUCTO_F + produccion_final - DD
            if(ST_PRODUCTO_F  > CAPACIDAD_TANQUE_PRODUCTO_FINAL):
                EXCEDENTE_PF += ST_PRODUCTO_F - CAPACIDAD_TANQUE_PRODUCTO_FINAL
                ST_PRODUCTO_F = CAPACIDAD_TANQUE_PRODUCTO_FINAL
        else:
            DNOCDD = DNOCDD + 1 #no cumplio demanda diaria
            ST_PRODUCTO_F = 0
            CDDI = CDDI + 1
        
        if((ST_DIESEL_F < DIESELF_limit_TO_RESTOCK) & (TPRDiesel_fosil == HV)):
            TPRDiesel_fosil = T + 5 # REPOSICIONES TARDAN 5 Dias    
        
        if((ST_BIODIESEL < BIODIESEL_limit_TO_RESTOCK) & (TPRBiodisiel == HV)):
            TPRBiodisiel = T + 5
         
    #RESULTADOS FINALES    
    PDNBP = (CDNOALEY/T) * 100
    PDNOCDD = (CDDI/T) * 100
    PLPNOALEY = (CDNOALEY/LT) * 100
    PDPI = (CDDI/T) * 100

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
    print("Porcentaje Dias produccion acuerdo la norma (93-7)", round(CDALEY/T* 100, 4), "%")
    print("Porcentaje Dias produccion alternativa (100-0) ", round(CDNOALEY/T * 100, 4), "%")
    print("* Porcentaje Dias No Produccion 0 :( ", round(CDNP/T * 100, 4), "%")
    
    # print("Porcentaje de Dias no cumplio con Demanda Diaria(PDNOCDD)", round(PDNOCDD, 2), "%")
    # print("Porcentaje Litros producidos Acuerdo a la norma (93-7) ", CLALEY , round(CLALEY/LT* 100, 2), "%")
    # print("Porcentaje Litros producidos No Acuerdo a la norma (100-0) ", CLNOALEY , round(CLNOALEY/LT * 100, 2), "%")
    
    # print("Promedio Litros totales producidos mensual ", round(LT/T*30, 0), "lts", "(", LT ,")")
    # print("* Promedio Litros Acuerdo a la Ley producidos mensual ", round(CLALEY/T*30, 0), "lts", "(", CLALEY ,")")
    print("* Promedio Litros No Acuerdo a la Ley mensual ", round(CLNOALEY/T*30, 0), "lts", "(", CLNOALEY ,")")
    print("* Promedio Litros excedentes mensual", round(EXCEDENTE_PF/T*30, 0), "lts", "(", EXCEDENTE_PF ,")")
    
    
    print("* Promedio Dias Demanda insatisfecha (producido + stock reserva) ", round(PDPI, 2), "%")
        
        





    # f = Fitter(df_arrivals_in_mins, distributions=['gamma', 'rayleigh', 'uniform'])
    # print(f.fit())
    # print(f.summary())
    # print(f.get_best())
    # print(f.get)

if __name__ == '__main__':
    main()