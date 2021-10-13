import glob
import os
from datetime import datetime, timedelta
from datetime import date
from datetime import datetime
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from datetime import date
from datetime import datetime
import time
import pandas as pd
import shutil
from selenium.webdriver.support.ui import Select




fechaAct = datetime.now()
fechaFin = fechaAct.replace(day = 1)
fechaFin = fechaFin - timedelta(days = 1)
fechaIni = fechaFin.replace(day = 1)
fechaIniR = fechaIni.strftime('%d-%m-%Y')
fechaFinR = fechaFin.strftime('%d-%m-%Y')
fechaFin = fechaFin.strftime('%Y-%m-%d')
fechaIni = fechaIni.strftime('%Y-%m-%d')
fecha_Inicial = fechaIni
fecha_Final = fechaFin



def renombrar(Nregistro):
    fichero = glob.glob("C:/Users/Nomezquy/Downloads/*.csv")
    ficheroDestino = f"C:/Users/Nomezquy/Desktop/DataLab/automatizacion_Merra/Solucion/documentos/Merra_{fechaIniR}_{fechaFinR}_{Nregistro}.csv"
    ultimoArchivo = max(fichero, key=os.path.getctime)
    archivoRenombrado = f"C:/Users/Nomezquy/Downloads/Merra_{fechaIniR}_{fechaFinR}_{Nregistro}.csv"
    os.rename(ultimoArchivo, archivoRenombrado)
    shutil.copyfile(archivoRenombrado,ficheroDestino)





def inicializarDriver(dr):
    driver = webdriver.Chrome(executable_path=r"C:\dchrome\chromedriver.exe")
    driver.get("http://www.soda-pro.com/web-services/meteo-data/merra")


def finalizarDriver(dr):
    dr.close()

def inicioSesion(driver,usuario,contrasena):
    campo_Usuario = driver.find_element_by_id("_58_login")
    campo_Usuario.send_keys(usuario)
    campo_Contraseña = driver.find_element_by_id("_58_password")
    campo_Contraseña.send_keys(contrasena)
    campo_Contraseña.send_keys(Keys.ENTER)
    time.sleep(3)

def cerrarSesion(driver):
    boton_CerrarSesion = driver.find_element_by_xpath("//*[@id='non-admin-dockbar']/a[2]")
    boton_CerrarSesion.click()

def generarConsulta(driver,latitud,longitud,fecha_Inicio,fecha_Final):
    #Mapeo de campos consulta

    campo_Lat = driver.find_element_by_id("latId")
    campo_Long = driver.find_element_by_id("lonId")
    campo_Finicial = driver.find_element_by_id("dateBegin")
    campo_Ffinal = driver.find_element_by_id("dateEnd")
    campo_Formato_Hora = driver.find_element_by_id("summarization")
    campo_Formato_Archivo = driver.find_element_by_id("outputFormat")
    boton_generar = driver.find_element_by_id("ext-gen70")


    #Ingresando valores
    campo_Lat.clear()
    campo_Lat.send_keys(latitud)
    campo_Long.clear()
    campo_Long.send_keys(longitud)
    campo_Finicial.clear()
    campo_Finicial.send_keys(fecha_Inicio)
    campo_Ffinal.clear()
    campo_Ffinal.send_keys(fecha_Final)
    campo_Step = driver.find_element_by_id("ext-gen82")
    campo_Step.click()
    seleccion_Step = driver.find_element_by_xpath("//*[@id='ext-gen88']/div[6]")
    seleccion_Step.click()
    campo_Format = driver.find_element_by_id("ext-gen86")
    campo_Format.click()
    seleccion_Format = driver.find_element_by_xpath("//*[@id='ext-gen91']/div[1]")
    seleccion_Format.click()
    boton_generar.click()
    time.sleep(5)
    boton_descargar = driver.find_element_by_id("responseLink")
    boton_descargar.click()
    time.sleep(2)

def insertarDb(collecion,Nregistro):
    ficheroFuente = f"C:/Users/Nomezquy/Desktop/DataLab/automatizacion_Merra/Solucion/documentos/Merra_{fechaIniR}_{fechaFinR}_{Nregistro}.csv"
    data = pd.read_csv(ficheroFuente,sep = ';', skiprows=25,header= None)
    x = 0
    i = 0
    valores = []
    while (x < data.shape[0]):
        while(i < 11):
            valores.insert(i,data.iloc[x][i])
            i += 1
        collecion.insert(
            {
                "Date" :valores[0],
                "UT time" : valores[1],
                "Temperature" :valores[2],
                "Relative Humidity" :valores[3],
                "Pressure" :valores[4],
                "Wind speed" :valores[5],
                "Wind direction" :valores[6],
                "Rainfall" :valores[7],
                "Snowfall" :valores[8],
                "Snow depth" :valores[9],
                "Short-wave irradiation" :valores[10]

            }
        )
        i = 0
        x +=1






