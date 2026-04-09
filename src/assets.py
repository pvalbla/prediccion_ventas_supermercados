from dagster import asset, Definitions
import pandas as pd
import os

@asset
def raw_sales_data():
    """Carga de los datos de ventas (Punto 2)."""
    return pd.read_csv(os.path.join('data', 'train.csv'), low_memory=False, nrows=100000)

@asset
def raw_store_data():
    """Carga de los datos de las tiendas (Punto 2)."""
    return pd.read_csv(os.path.join('data', 'store.csv'))

@asset
def integrated_data(raw_sales_data, raw_store_data):
    """Cruce, Transformación y Mapeo (Puntos 3, 4 y 5)."""
    # Unión
    df = pd.merge(raw_sales_data, raw_store_data, on='Store', how='left')
    # Fecha
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    # Mapeo
    dict_tiendas = {'a': 'Pequeña', 'b': 'Mediana', 'c': 'Grande', 'd': 'Extra'}
    df['StoreType_Name'] = df['StoreType'].map(dict_tiendas)
    # Ordenación
    df = df.sort_values(by=['Date', 'Sales'], ascending=[True, False])
    return df

# Esto le dice a Dagster qué mostrar en la web
defs = Definitions(assets=[raw_sales_data, raw_store_data, integrated_data])