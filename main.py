## Importamos librerias necesarias para la ejecución.
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from datetime import date
from datetime import datetime
import time
import funciones

#Inicializamos variables
usuario = "pruebas.dnomezquy@gmail.com"  # Usuario ingreso página
contrasena = "Pruebas123" # Contraseña ingreso página
fechaInicio = "2021-08-01"#funciones.fecha_Inicial
fechaFin = "2021-08-30"#funciones.fecha_Final
driver = webdriver.Chrome(executable_path=r"C:\dchrome\chromedriver.exe")


##inicializamos DB para consulta de datos.
cliente = MongoClient()
db = cliente.merra
coll_Fuente = db.fuente
coll_Resultados = db.resultados
grillas = coll_Fuente.find()


driver.get("http://www.soda-pro.com/web-services/meteo-data/merra")
funciones.inicioSesion(driver,usuario,contrasena)

grillaActual = 1
for grilla  in grillas:
    grilla = coll_Fuente.find_one({'GRILLA': str(grillaActual)})
    latitud = grilla["LAT"]
    longitud = grilla["LONG"]
    funciones.generarConsulta(driver,latitud,longitud,fechaInicio,fechaFin)
    funciones.renombrar(grillaActual)#fechaInicio,fechaFin)
    funciones.insertarDb(coll_Resultados,grillaActual)
    grillaActual += 1


funciones.finalizarDriver(driver)
