#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
import datetime


def ine_request(ine_code):
    resultados = 999
    path_template = 'http://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{cod_serie}?nult={n_ult_datos}'
    path = path_template.format(cod_serie=ine_code, n_ult_datos=resultados)
    json_request = requests.get(path).json()
    
    return json_request

df_codigos = pd.read_excel('ine_codes.xlsx')
codigos = df_codigos['ine_code'].tolist()

anyo_lista = list()
mes_lista = list()
variable_lista = list()
valor_lista = list()

for codigo in codigos:
    datos = ine_request(codigo)
    
    nombre_variable = datos['Nombre']
    for dato in datos['Data']:
        fecha = datetime.date.fromtimestamp(dato['Fecha'] // 1000)
        anyo = fecha.year
        mes = fecha.month
        valor = dato['Valor']

        anyo_lista.append(anyo)
        mes_lista.append(mes)
        variable_lista.append(nombre_variable)
        valor_lista.append(valor)

df = pd.DataFrame({
        'Año' : anyo_lista,
        'Mes' : mes_lista,
        'Dato' : variable_lista,
        'Población' : valor_lista
    })

df.to_excel('tabla_ine.xlsx', index=False)