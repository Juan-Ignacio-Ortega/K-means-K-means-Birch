import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DB = pd.read_csv('Mall_Customers.csv')

print('Cantidad de datos por atributo =', str(len(DB['Age'])) + '.')
DB.head()

def Normaliza(DB):
    DB = DB.to_numpy()

    Atributos = DB[0]
    NoAtributos = len(Atributos)
    Instancias = DB.T[0]
    NoInstancias = len(Instancias)

    MaximoDeAtributos = []
    MinimoDeAtributos = []
    for idx, element in enumerate(Atributos):
      CaractMax = max(DB.T[idx])
      CaractMin = min(DB.T[idx])
      MaximoDeAtributos.append(CaractMax)
      MinimoDeAtributos.append(CaractMin)

    DBNorm = []
    MaximoNormalizado = 1
    MinimoNormalizado = 0
    RangoNormalizado = MaximoNormalizado - MinimoNormalizado
    for idx, element in enumerate(Atributos):
      CaractNorm = []
      if str(type(Atributos[idx]))[8 : -2] != 'str':
        RangodeDatos = MaximoDeAtributos[idx] - MinimoDeAtributos[idx]
        for idx2, element2 in enumerate(Instancias):
          if str(DB.T[idx][idx2]) != 'nan':
            D = DB.T[idx][idx2] - MinimoDeAtributos[idx]
            DPct = D / RangodeDatos
            dNorm = RangoNormalizado * DPct
            Normalizado = MinimoNormalizado + dNorm
            CaractNorm.append(Normalizado)
          else:
            CaractNorm.append(DB.T[idx][idx2])
      else:
        for idx2, element2 in enumerate(Instancias):
          CaractNorm.append(DB.T[idx][idx2])
      DBNorm.append(CaractNorm)
    return(DBNorm)

DB_Norm = Normaliza(DB)

X = np.array(DB_Norm[3])
Y = np.array(DB_Norm[2])

plt.scatter(X, Y, color = 'lightblue', label = 'Datos')
plt.title('Ingreso Anual (k$) vs Edad')
plt.xlabel('Ingreso Anual (k$)')
plt.ylabel('Edad')
plt.legend()
plt.show()

def data2point(X, Y):
    puntos = []
    for idx, x in enumerate(X):
        puntos.append((x, Y[idx]))
    return(puntos)

puntos = data2point(X, Y)

def distACentrsXpunto(Centrs, DaXpuntos):
    dist = []
    for element in Centrs:
        distXData = []
        for DaXpunto in DaXpuntos:
            distData = ((element[0] - DaXpunto[0])**2 + (element[1] - DaXpunto[1])**2)**0.5
            distXData.append(distData)
        dist.append(distXData)
    return(dist)

def CentrsPP(NumDcentrs, PuntosIn):
    First_Centr = (rd.random(), rd.random())
    
    Centrs = [First_Centr]
    for NumCent in range(1, NumDcentrs, 1):
        Dists = distACentrsXpunto(Centrs, PuntosIn)
        Minpunto = Dists[0]
        for CentN in Dists:
            for idx, distN in enumerate(CentN):
                if distN < Minpunto[idx]:
                    Minpunto[idx]  = distN
        distmin = max(Minpunto)
        Minpunto = np.array(Minpunto)
        posMinpunto = np.where(Minpunto == distmin)
        Centrs.append(PuntosIn[posMinpunto[0][0]])
    
    return(Centrs)

Centrs = CentrsPP(9, puntos)

Xp = []
Yp = []
for element in Centrs:
    Xp.append(element[0])
    Yp.append(element[1])

plt.scatter(X, Y, color = 'lightblue', label = 'Datos')
plt.scatter(Xp, Yp, color = 'red', label = 'Centroides')
plt.title('Ingreso Anual (k$) vs Edad')
plt.xlabel('Ingreso Anual (k$)')
plt.ylabel('Edad')
plt.legend()
plt.show()

idxCentrs = len(Centrs)

Centrs4KM = []
for idxCentr in range(1, (idxCentrs+1)):
    Centrs4KM_par = []
    for idx, K in enumerate(range(1, idxCentr + 1)):
        Centrs4KM_par.append(Centrs[idx])
    Centrs4KM.append(Centrs4KM_par)

dist_glob = []
for Centr in Centrs4KM:
    dist = distACentrsXpunto(Centr, puntos)
    dist_glob.append(dist)

def Dato2CentrX(D2Xpuntos, dist):
    MinimIdx = []
    for idx, D2Xpunto in enumerate(D2Xpuntos):
        inim = []
        for element in dist:
            inim.append(element[idx])
        minimo = min(inim)
        MinIdx = inim.index(minimo)
        MinimIdx.append(MinIdx)
    return(MinimIdx)

minimf_glob = []
for dist in dist_glob:
    MinimIdx = Dato2CentrX(puntos, dist)
    minimf_glob.append(MinimIdx)

minimf_glob = np.array(minimf_glob)

WCSS = []
for idx1, Centr in enumerate(Centrs4KM):
    sumD = 0
    for idx2, K in enumerate(Centr):
        pos = np.where(minimf_glob[idx1] == idx2)
        for element in pos[0]:
            sumD += (((puntos[element][0] - K[0])**2 + (puntos[element][1] - K[1])**2)**0.5)**2
    WCSS.append(sumD)

idxClusts  = idxCentrs = len(Centrs)
    
plt.plot(range(1, (idxClusts+1)), WCSS, color = 'lightblue', label = 'WCSS según la cantidad de K considerados', linewidth = 3)
plt.scatter(5, WCSS[4], color = 'red', linewidth = 5)
plt.title('Número de clúster vs WCSS')
plt.xlabel('Número de clúster (K)')
plt.ylabel('Within-Cluster Sum-of-Squares (WCSS)')
plt.legend()
plt.show()

import random as rd
import matplotlib.pyplot as plt
import numpy as np
from IPython import display
from sklearn.cluster import KMeans

def CentrsPP(NumDcentrs, PuntosIn):
    First_Centr = (rd.random(), rd.random())
    
    Centrs = [First_Centr]
    for NumCent in range(1, NumDcentrs, 1):
        Dists = distACentrsXpunto(Centrs, PuntosIn)
        Minpunto = Dists[0]
        for CentN in Dists:
            for idx, distN in enumerate(CentN):
                if distN < Minpunto[idx]:
                    Minpunto[idx]  = distN
        distmin = max(Minpunto)
        Minpunto = np.array(Minpunto)
        posMinpunto = np.where(Minpunto == distmin)
        Centrs.append(PuntosIn[posMinpunto[0][0]])
    
    return(Centrs)

Centroides = CentrsPP(5, puntos)

Xp = []
Yp = []
for element in Centroides:
    Xp.append(element[0])
    Yp.append(element[1])

plt.scatter(X, Y, color = 'lightblue', label = 'Datos')
plt.scatter(Xp, Yp, color = 'red', label = 'Centroides')
plt.title('Ingreso Anual (k$) vs Edad')
plt.xlabel('Ingreso Anual (k$)')
plt.ylabel('Edad')
plt.legend()
plt.show()

def Centrs_aleat(NumDCentrs):
    idxCentrs = range(1, NumDCentrs + 1)

    Centrs = []
    for K in idxCentrs:
        Centrs.append((rd.random(), rd.random()))
    return(Centrs)

def Centrs_promedio(Datos):
    Centrs = []
    for K in Datos:
        sumaX = 0
        sumaY = 0
        for data in K:
            sumaX += data[0]
            sumaY += data[1]
        X = sumaX / len(K)
        Y = sumaY / len(K)
        Centrs.append((X, Y))
    return(Centrs)

def distACentrsXpunto(Centrs, DaXpuntos):
    dist = []
    for element in Centrs:
        distXData = []
        for DaXpunto in DaXpuntos:
            distData = ((element[0] - DaXpunto[0])**2 + (element[1] - DaXpunto[1])**2)**0.5
            distXData.append(distData)
        dist.append(distXData)
    return(dist)

def Dato2CentrX(D2Xpuntos, dist):
    MinimIdx = []
    for idx, D2Xpunto in enumerate(D2Xpuntos):
        inim = []
        for element in dist:
            inim.append(element[idx])
        minimo = min(inim)
        MinIdx = inim.index(minimo)
        MinimIdx.append(MinIdx)
    return(MinimIdx)

def AgrupDatos(Centroides, CentroideXDato, ADPuntos):
    PuntosDCentr = []
    for idx, Centroide in enumerate(Centroides):
        PuntosDColorX = []
        positions = np.where(CentroideXDato == idx)
        for position in positions[0]:
            PuntosDColorX.append(ADPuntos[position])
        PuntosDCentr.append(PuntosDColorX)
    return(PuntosDCentr)

def Predict(data):
    distancias = distACentrsXpunto(Centroides, data)
    CentroideXDato = Dato2CentrX(data, distancias)
    Pertenencias = []
    for element in CentroideXDato:
        Pertenencias.append(element + 1)
    Pertenencia = np.array(Pertenencias)
    return(Pertenencia)

distancias = distACentrsXpunto(Centroides, puntos)

CentroideXDato = Dato2CentrX(puntos, distancias)

CentroideXDato = np.array(CentroideXDato)

PuntosDCentr = AgrupDatos(Centroides, CentroideXDato, puntos)

Centroides = Centrs_promedio(PuntosDCentr)

Centroides_anterior = 0

while Centroides_anterior != Centroides:
    Centroides_anterior = Centroides
    distancias = distACentrsXpunto(Centroides_anterior, puntos)
    CentroideXDato = Dato2CentrX(puntos, distancias)
    CentroideXDato = np.array(CentroideXDato)
    PuntosDCentr = AgrupDatos(Centroides_anterior, CentroideXDato)
    Centroides = Centrs_promedio(PuntosDCentr)
    Xp = []
    Yp = []
    for element in Centroides:
        Xp.append(element[0])
        Yp.append(element[1])

    Colors = ['yellow', 'orange', 'lightblue', 'purple', 'lightgreen']

    for idx, Puntos in enumerate(PuntosDCentr):
        XColor = []
        YColor = []
        for element in Puntos:
            XColor.append(element[0])
            YColor.append(element[1])
        plt.scatter(XColor, YColor, color = Colors[idx], label = 'Datos de Centroide ' + str(idx + 1))

    plt.scatter(Xp, Yp, color = 'red', label = 'Centroides')
    plt.title('Ingreso Anual (k$) vs Edad')
    plt.xlabel('Ingreso Anual (k$)')
    plt.ylabel('Edad')
    plt.legend()
    display.clear_output(wait=True)
    plt.pause(1)

plt.show()

for idx, Centroide in enumerate(Centroides):
    print('El centroide', str(idx + 1), 'tiene coordenadas', str(Centroide) + '.')

puntos = data2point(X, Y)

kmeans = KMeans(n_clusters=5, init='k-means++', n_init=1, random_state=0).fit(puntos)
CentroideXDato = kmeans.labels_
Centroides = kmeans.cluster_centers_
PuntosDCentr = AgrupDatos(Centroides, CentroideXDato, puntos)

Xp = []
Yp = []
for element in Centroides:
    Xp.append(element[0])
    Yp.append(element[1])

Colors = ['yellow', 'orange', 'lightblue', 'purple', 'lightgreen']

for idx, Puntos in enumerate(PuntosDCentr):
    XColor = []
    YColor = []
    for element in Puntos:
        XColor.append(element[0])
        YColor.append(element[1])
    plt.scatter(XColor, YColor, color = Colors[idx], label = 'Datos de Centroide ' + str(idx + 1))
    
plt.scatter(Xp, Yp, color = 'red', label = 'Centroides')
plt.title('Ingreso Anual (k$) vs Edad')
plt.xlabel('Ingreso Anual (k$)')
plt.ylabel('Edad')
plt.legend()
plt.show()

for idx, Centroide in enumerate(Centroides):
    print('El centroide', str(idx + 1), 'tiene coordenadas', str(Centroide) + '.')