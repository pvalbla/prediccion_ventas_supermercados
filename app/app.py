import streamlit as st
import pandas as pd
import joblib
import datetime

# Configuración de la página
st.set_page_config(page_title="Predicador de Ventas Rossmann", page_icon="📈")

st.title("📈 Predicción de Ventas Rossmann")
st.markdown("Introduce los datos de la tienda para obtener una predicción inteligente.")

# 1. Cargamos el modelo "congelado"
@st.cache_resource
def load_model():
    return joblib.load('notebooks/model_rossmann.joblib')

data = load_model()
model = data['model']
features = data['features']

# 2. Interfaz de usuario (Sidebar)
st.sidebar.header("Configuración de la Tienda")

tienda = st.sidebar.number_input("Número de Tienda", min_value=1, max_value=1115, value=1)
fecha = st.sidebar.date_input("Fecha de predicción", datetime.date(2026, 4, 10))
promo = st.sidebar.checkbox("¿Tiene promoción hoy?", value=True)

# Extraemos datos de la fecha
dia_semana = fecha.weekday() + 1  # Lunes=1, Domingo=7
mes = fecha.month
dia = fecha.day
año = fecha.year
es_finde = 1 if dia_semana >= 6 else 0

# 3. Preparamos los datos para el modelo
# Creamos un DataFrame con una sola fila
input_data = pd.DataFrame([[
    tienda, dia_semana, 1 if promo else 0, mes, dia, año,
    5000, 0, 0, 0, 0, 0  # Valores por defecto para competencia y tipos (simplificado)
]], columns=features)

# 4. Botón de Predicción
if st.button("Calcular Ventas Estimadas"):
    prediccion = model.predict(input_data)[0]
    
    st.balloons()
    st.success(f"### 💰 Predicción: {prediccion:.2f} €")
    
    # Un poco de contexto estadístico
    st.info(f"Nota: El modelo tiene una precisión del 89.19% con un error medio de 634€.")