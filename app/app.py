import streamlit as st
import pandas as pd
import joblib
import datetime

# Configuración de la página (layout="wide" para que el simulador respire)
st.set_page_config(page_title="Predictor de Ventas Rossmann", page_icon="📈", layout="wide")

st.title("📈 Predictor de Ventas Rossmann")

# 1. Cargamos el modelo y los datos de las tiendas
@st.cache_resource
def load_model():
    return joblib.load('notebooks/model_rossmann.joblib')

@st.cache_data
def load_store_info():
    return pd.read_csv('data/store.csv')

# Inicializamos datos
data_model = load_model()
model = data_model['model']
df_stores = load_store_info()

# 2. Interfaz de usuario (Sidebar)
st.sidebar.header("⚙️ Configuración")

# EL INTERRUPTOR MÁGICO
modo_simulador = st.sidebar.toggle("🧪 Activar Modo Simulador Avanzado")
st.sidebar.markdown("---")

# AJUSTE ECONÓMICO (Inflación)
st.sidebar.subheader("💰 Ajuste Económico")
tasa_inflacion = st.sidebar.slider("Inflación Anual Estimada (%)", 0.0, 10.0, 3.0) / 100
st.sidebar.markdown("---")

# 3. Lógica de Interfaz según el Modo
if not modo_simulador:
    # --- MODO NORMAL (Básico) ---
    st.markdown("Selecciona una tienda existente para obtener una predicción basada en sus datos reales.")
    
    tienda_id = st.sidebar.number_input("Número de Tienda", min_value=1, max_value=1115, value=1)
    fecha = st.sidebar.date_input(
        "Fecha de predicción", 
        value=datetime.date(2015, 6, 15), # Fecha por defecto (Últimos datos conocidos)
        min_value=datetime.date(2013, 1, 1), 
        max_value=datetime.date(2036, 12, 31) 
    )
    promo = st.sidebar.checkbox("¿Tiene promoción hoy?", value=True)
    
    # Extraemos info real del CSV
    store_row = df_stores[df_stores['Store'] == tienda_id].iloc[0]
    distancia = store_row['CompetitionDistance'] if pd.notnull(store_row['CompetitionDistance']) else df_stores['CompetitionDistance'].median()
    tipo_tienda = store_row['StoreType']
    surtido = store_row['Assortment']

else:
    # --- MODO SIMULADOR (Dios) ---
    st.markdown("### 🧪 Laboratorio de Simulación")
    st.info("Inventa tu propio escenario. ¿Qué pasaría si montas una tienda gigante con la competencia pegada a la puerta?")
    
    # Usamos columnas para que no quede una lista kilométrica
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tienda_id = st.number_input("ID Tienda (Ficticio)", value=9999)
        fecha = st.date_input(
            "Fecha Simulada", 
            value=datetime.date(2026, 4, 10), # Por defecto en el futuro para impresionar
            min_value=datetime.date(2013, 1, 1),
            max_value=datetime.date(2036, 12, 31)
        )
        promo = st.checkbox("Activar Promoción Extraordinaria", value=True)
        
    with col2:
        distancia = st.number_input("Distancia a la Competencia (metros)", min_value=0, value=150, step=50)
        
        # Nombres basados en el análisis real de datos de Rossmann
        tipo_sel = st.selectbox(
            "Tipo de Tienda (Modelo)", 
            [
                "a (Estándar - Mayoría de tiendas)", 
                "b (Alto tráfico - Ej. Estación/Aeropuerto)", 
                "c (Barrio/Pequeña)", 
                "d (Hipermercado/Afueras)"
            ]
        )
        tipo_tienda = tipo_sel[0] # Se queda con la letra 'a', 'b', 'c' o 'd'
        
    with col3:
        # Definición oficial de Kaggle
        surtido_sel = st.selectbox(
            "Nivel de Surtido", 
            [
                "a (Básico)", 
                "b (Extra)", 
                "c (Extendido)"
            ]
        )
        surtido = surtido_sel[0] # Se queda con la 'a', 'b' o 'c'

# 4. Extracción de Fecha (Común a ambos modos)
dia_semana = fecha.weekday() + 1
mes = fecha.month
dia = fecha.day
año = fecha.year

st.markdown("---")

# 5. Botón y Predicción
if st.button("🚀 Calcular Ventas Estimadas", type="primary", use_container_width=True):
    
    # Construimos el diccionario con el ORDEN EXACTO de tus 12 features
    datos_finales = {
        'Store': tienda_id,
        'DayOfWeek': dia_semana,
        'Promo': 1 if promo else 0,
        'Month': mes,
        'Day': dia,
        'Year': año,
        'CompetitionDistance': distancia,
        'StoreType_b': 1 if tipo_tienda == 'b' else 0,
        'StoreType_c': 1 if tipo_tienda == 'c' else 0,
        'StoreType_d': 1 if tipo_tienda == 'd' else 0,
        'Assortment_b': 1 if surtido == 'b' else 0,
        'Assortment_c': 1 if surtido == 'c' else 0
    }
    
    # Convertimos a DataFrame
    input_df = pd.DataFrame([datos_finales])
    
    # Predicción base del modelo
    prediccion_base = model.predict(input_df)[0]
    
    # LÓGICA DE INFLACIÓN COMPUESTA
    año_actual = fecha.year
    años_diferencia = max(0, año_actual - 2015) # Calcula los años pasados desde el dataset original
    multiplicador_inflacion = (1 + tasa_inflacion) ** años_diferencia
    prediccion_ajustada = prediccion_base * multiplicador_inflacion
    
    # Resultados visuales
    st.balloons()
    st.success(f"## 💰 Ventas Estimadas: {prediccion_ajustada:.2f} €")
    
    # Mensaje aclaratorio si se aplica inflación
    if años_diferencia > 0 and tasa_inflacion > 0:
        st.caption(f"📈 *Nota: Se ha aplicado un ajuste acumulado del {((multiplicador_inflacion-1)*100):.1f}% por inflación ({tasa_inflacion*100:.0f}% anual) desde 2015.*")
    
    # Demostración del "Iceberg" para el profesor
    with st.expander("🔍 Ver la radiografía de datos (Las 12 variables reales que lee la IA)"):
        st.write("Aunque en la interfaz solo ves unos pocos controles, la IA procesa esta matriz exacta:")
        st.dataframe(input_df)

st.info("Nota: El modelo base (2015) tiene una precisión del 89.19% con un error medio de 634€.")