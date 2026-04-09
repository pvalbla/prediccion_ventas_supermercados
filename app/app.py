import streamlit as st
import pandas as pd
import joblib
import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Predicador de Ventas Rossmann", page_icon="📈")

st.title("📈 Predicción de Ventas Rossmann")
st.markdown("Introduce los datos de la tienda para obtener una predicción inteligente.")

# 1. Cargamos el modelo y los datos de las tiendas
@st.cache_resource
def load_model():
    # Nota: Asegúrate de que la ruta coincide con tu carpeta
    return joblib.load('notebooks/model_rossmann.joblib')

@st.cache_data
def load_store_info():
    # Cargamos el CSV de tiendas para tener los datos de competencia y tipos
    return pd.read_csv('data/store.csv')

# Inicializamos datos
data_model = load_model()
model = data_model['model']
features_entrenamiento = data_model['features']
df_stores = load_store_info()

# 2. Interfaz de usuario (Sidebar)
st.sidebar.header("Configuración de la Tienda")

tienda_id = st.sidebar.number_input("Número de Tienda", min_value=1, max_value=1115, value=1)
fecha = st.sidebar.date_input("Fecha de predicción", datetime.date(2026, 4, 10))
promo = st.sidebar.checkbox("¿Tiene promoción hoy?", value=True)

# Extraemos datos de la fecha
dia_semana = fecha.weekday() + 1  # Lunes=1, Domingo=7
mes = fecha.month
dia = fecha.day
año = fecha.year

# 3. Lógica para obtener datos reales de la tienda seleccionada
def get_inputs_tienda(id_tienda):
    # Buscamos la fila de la tienda
    store_row = df_stores[df_stores['Store'] == id_tienda].iloc[0]
    
    # Manejo de nulos en CompetitionDistance (usamos la mediana como en tu notebook)
    distancia = store_row['CompetitionDistance']
    if pd.isna(distancia):
        distancia = df_stores['CompetitionDistance'].median()
        
    # Mapeo de One-Hot Encoding (StoreType y Assortment)
    # Según tu entrenamiento: StoreType_b, StoreType_c, StoreType_d, Assortment_b, Assortment_c
    return {
        'CompetitionDistance': distancia,
        'StoreType_b': 1 if store_row['StoreType'] == 'b' else 0,
        'StoreType_c': 1 if store_row['StoreType'] == 'c' else 0,
        'StoreType_d': 1 if store_row['StoreType'] == 'd' else 0,
        'Assortment_b': 1 if store_row['Assortment'] == 'b' else 0,
        'Assortment_c': 1 if store_row['Assortment'] == 'c' else 0,
    }

# 4. Botón de Predicción
if st.button("Calcular Ventas Estimadas"):
    # Obtenemos los datos técnicos de la tienda
    info_tecnica = get_inputs_tienda(tienda_id)
    
    # Construimos el diccionario con el ORDEN EXACTO de tus features
    datos_finales = {
        'Store': tienda_id,
        'DayOfWeek': dia_semana,
        'Promo': 1 if promo else 0,
        'Month': mes,
        'Day': dia,
        'Year': año,
        'CompetitionDistance': info_tecnica['CompetitionDistance'],
        'StoreType_b': info_tecnica['StoreType_b'],
        'StoreType_c': info_tecnica['StoreType_c'],
        'StoreType_d': info_tecnica['StoreType_d'],
        'Assortment_b': info_tecnica['Assortment_b'],
        'Assortment_c': info_tecnica['Assortment_c']
    }
    
    # Convertimos a DataFrame
    input_df = pd.DataFrame([datos_finales])
    
    # Realizamos la predicción
    prediccion = model.predict(input_df)[0]
    
    # Mostramos resultados
    st.balloons()
    st.success(f"### 💰 Predicción: {prediccion:.2f} €")
    
    # Feedback visual de los datos usados
    with st.expander("Ver detalles del cálculo"):
        st.write(f"Tienda tipo: **{df_stores[df_stores['Store']==tienda_id]['StoreType'].values[0]}**")
        st.write(f"Distancia competencia: **{info_tecnica['CompetitionDistance']}m**")
        st.dataframe(input_df)

# Contexto estadístico fijo
st.info(f"Nota: El modelo tiene una precisión del 89.19% con un error medio de 634€.")