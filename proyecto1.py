# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 13:32:54 2025

# @author: Marlon.za
# """
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from numpy import radians,sin,cos,pi

df=pd.read_csv('Copia de SolarArrayProduction.csv',sep=";", header=None, skiprows=1,names=["fechaHora","elect p1","elect p2"])
df["fechaHora"] = df["fechaHora"].astype(str).str.strip()

# 2️⃣ Convertir a datetime, probando año con 2 y con 4 dígitos
def parse_date(x):
    for fmt in ("%m/%d/%y %H:%M", "%m/%d/%Y %H:%M"):
        try:
            return pd.to_datetime(x, format=fmt)
        except:
            continue
    return pd.NaT


fecha_d= input("Ingrese la fecha (YYYY-MM-DD): ")
fecha=pd.to_datetime(fecha_d)
d= fecha.dayofyear
lat= float(input("Ingrese la latitud (ej. 42.28): "))    #la latitud
lat=radians(lat)
lon=lon = float(input("Ingrese la longitud (ej. 14.6): "))
inclinacion = float(input("Ingrese la inclinación del panel (ej. 30): "))
acimut_panel = float(input("Ingrese el acimut del panel (0=Norte, 180=Sur): "))


area_pan=270    #area del panel 
eficiencia=0.18
dec = 23.45*cos(360/365*(d-172))  #declinacion del sol segun el dia




df["fechaHora"] = df["fechaHora"].apply(parse_date)
# df["hora_flo"] = df["fechaHora"].dt.hour + df["fechaHora"].dt.minute/60

# Quitar espacios y reemplazar coma por punto en los datos numéricos
df["elect p1"] = df["elect p1"].astype(str).str.replace(" ", "").str.replace(",", ".").astype(float)
df["elect p2"] = df["elect p2"].astype(str).str.replace(" ", "").str.replace(",", ".").astype(float)
# Agrupar por día y sumar producción
# produccion_dia = df.groupby(df["fechaHora"].dt.date)[["elect p1","elect p2"]].sum()

fecha_objetivo = "2018-06-20"
filtro = df[df["fechaHora"].dt.date == pd.to_datetime(fecha).date()]
hora_f= filtro["fechaHora"].dt.hour + filtro["fechaHora"].dt.minute / 60
 

dec=radians(dec)

t = pd.date_range(f"{fecha} 00:00", f"{fecha} 23:59", freq="15min")
t_float= t.hour + t.minute/60+t.second/3600
lts=(t_float-1)+(lon/60)
H = radians(15 * (lts - 12)) #angulo horario solar 
sungle=(sin(dec)*sin(lat)) + (cos(dec)*cos(lat))*cos(H) # angulo solar 
altura = np.arcsin(sungle)

s_in=1.4883*0.7**((sungle)**-0.678) #irradiancia 

altura = np.arcsin(sungle)         # radianes
altura_grados = np.degrees(altura) 


produccion=area_pan*sungle*s_in #produccion simulada 
produccion=pd.Series(produccion)
produccion_dia = produccion.sum()

if not filtro.empty:
    
    # Graficar elect p1 y elect p2 durante ese día
    plt.figure(figsize=(10,5))
    plt.plot(hora_f, filtro["elect p1"], label="panel 1")
    plt.plot(hora_f, filtro["elect p2"], label="panel 2")
    plt.plot(t_float, produccion, label="simulada")
    plt.title(f"fecha: {fecha_d}")
    plt.suptitle(" potencia simulada vs potencia paneles reales")
    plt.xlabel("Hora")
    plt.ylabel("Producción W")
    plt.legend()
    plt.grid(True)
    
    plt.xticks(np.arange(0, 25, 1))
    
    plt.show()

#grafico altura solar 

plt.figure(figsize=(10,5))
plt.plot(t_float,altura_grados,color="red")
plt.title("Angulo de altitud solar vs Hora del dia")
plt.suptitle(f"fecha: {fecha_d}")
plt.xlabel("Hora")
plt.ylabel("angulo altitud solar")
plt.grid(True)

plt.xticks(np.arange(0, 25, 1))

plt.show

#grafico angulo horario
H=15 * (lts - 12)
plt.figure(figsize=(10,5))
plt.plot(t_float,H)
plt.title("Angulo horario H vs. hora del día")
plt.xlabel("Hora")
plt.ylabel("Producción W")
plt.grid(True)

plt.xticks(np.arange(0, 25, 1))

plt.show

#grafico de produccion
plt.figure(figsize=(10,5))
plt.plot(t_float,produccion,color="purple")
plt.title("produccion simulada vs Hora del dia")
plt.suptitle(f"fecha: {fecha_d}")
plt.xlabel("Hora")
plt.ylabel("Producción W")
plt.grid(True)
plt.xticks(np.arange(0, 25, 1))
plt.show


