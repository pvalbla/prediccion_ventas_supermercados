from dagster import asset, Definitions
import pandas as pd
import dask.dataframe as dd
import os
import joblib
from sklearn.ensemble import RandomForestRegressor

# ==========================================
# 1. EXTRACCIÓN DE DATOS
# ==========================================

@asset
def raw_sales_data():
    """Carga y filtrado masivo con Dask (Aceleración Big Data)."""
    # Usamos Dask para no saturar la memoria
    path = os.path.join('data', 'train.csv')
    ddf = dd.read_csv(path, dtype={'StateHoliday': 'object'})
    
    # Filtramos tiendas cerradas antes de pasar a RAM
    ddf_open = ddf[ddf['Open'] != 0]
    
    return ddf_open.compute()

@asset
def raw_store_data():
    """Carga de los datos de las tiendas (Pandas tradicional)."""
    return pd.read_csv(os.path.join('data', 'store.csv'))


# ==========================================
# 2. TRANSFORMACIÓN Y LIMPIEZA
# ==========================================

@asset
def integrated_data(raw_sales_data, raw_store_data):
    """Cruce de datos y creación de columnas base."""
    # Unión
    df = pd.merge(raw_sales_data, raw_store_data, on='Store', how='left')
    
    # Fechas
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Year'] = df['Date'].dt.year
    
    # Mapeo
    dict_tiendas = {'a': 'Pequeña', 'b': 'Mediana', 'c': 'Grande', 'd': 'Extra'}
    df['StoreType_Name'] = df['StoreType'].map(dict_tiendas)
    
    # Ordenación
    df = df.sort_values(by=['Date', 'Sales'], ascending=[True, False])
    
    return df

@asset
def ml_ready_data(integrated_data):
    """Feature Engineering: Preparación final para el modelo."""
    df = integrated_data.copy()
    
    # Tratamiento de nulos
    mediana_distancia = df['CompetitionDistance'].median()
    df['CompetitionDistance'] = df['CompetitionDistance'].fillna(mediana_distancia)
    
    # One-Hot Encoding
    df = pd.get_dummies(df, columns=['StoreType', 'Assortment', 'StateHoliday'], drop_first=True)
    
    return df


# ==========================================
# 3. ENTRENAMIENTO Y EXPORTACIÓN
# ==========================================

@asset
def train_and_export_model(ml_ready_data):
    """Entrena el Random Forest y guarda el archivo .joblib"""
    df = ml_ready_data
    
    # Variables que sabemos que son importantes
    features = [
        'Store', 'DayOfWeek', 'Promo', 'Month', 'Day', 'Year', 
        'CompetitionDistance', 'StoreType_b', 'StoreType_c', 'StoreType_d',
        'Assortment_b', 'Assortment_c'
    ]
    
    # Nos aseguramos de coger solo las columnas que existen en el dataframe
    # (Por si alguna tienda tipo 'd' no está en un sample pequeño)
    actual_features = [f for f in features if f in df.columns]
    
    X = df[actual_features]
    y = df['Sales']
    
    # Entrenamos el modelo con los parámetros óptimos que encontraste
    model = RandomForestRegressor(
        n_estimators=40, 
        max_depth=35, 
        min_samples_leaf=30, 
        random_state=42, 
        n_jobs=-1
    )
    model.fit(X, y)
    
    # Guardamos el modelo en formato diccionario como hicimos en el notebook
    model_data = {
        'model': model,
        'features': actual_features
    }
    
    # Guardamos en la raíz del proyecto o en una carpeta models/
    joblib.dump(model_data, 'model_rossmann.joblib')
    
    return True # Dagster solo necesita saber que la tarea terminó con éxito

# ==========================================
# DEFINICIONES PARA DAGSTER
# ==========================================
defs = Definitions(
    assets=[
        raw_sales_data, 
        raw_store_data, 
        integrated_data, 
        ml_ready_data, 
        train_and_export_model
    ]
)