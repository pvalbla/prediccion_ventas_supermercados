import streamlit as st
import pandas as pd
import joblib
import datetime

st.set_page_config(page_title="Predictor de Ventas Rossmann", page_icon="📈", layout="wide")

st.title("📈 Predictor de Ventas Rossmann")

# Cargamos el modelo y los datos de las tiendas
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

# Sidebar
st.sidebar.header("⚙️ Configuración")

modo_simulador = st.sidebar.toggle("🧪 Activar Modo Simulador Avanzado")
st.sidebar.markdown("---")

# ajuste de inflación
st.sidebar.subheader("💰 Ajuste Económico")
tasa_inflacion = st.sidebar.slider("Inflación Anual Estimada (%)", 0.0, 10.0, 3.0) / 100
st.sidebar.markdown("---")

# Interfaz según el Modo
if not modo_simulador:
    # MODO NORMAL
    st.markdown("Selecciona una tienda existente para obtener una predicción basada en sus datos reales.")
    
    tienda_id = st.sidebar.number_input("Número de Tienda", min_value=1, max_value=1115, value=1)
    fecha = st.sidebar.date_input(
        "Fecha de predicción", 
        value=datetime.date(2015, 6, 15), # Fecha por defecto (Últimos datos conocidos)
        min_value=datetime.date(2013, 1, 1), 
        max_value=datetime.date(2036, 12, 31) 
    )
    promo = st.sidebar.checkbox("¿Tiene promoción hoy?", value=True)
    
    tienda_filtrada = df_stores[df_stores['Store'] == tienda_id]
    
    if tienda_filtrada.empty:
        st.warning(f"⚠️ La tienda número {tienda_id} no existe en la base de datos. Por favor, prueba con otro número o activa el 'Modo Simulador'.")
        st.stop()
        
    store_row = tienda_filtrada.iloc[0]
    distancia = store_row['CompetitionDistance'] if pd.notnull(store_row['CompetitionDistance']) else df_stores['CompetitionDistance'].median()
    tipo_tienda = store_row['StoreType']
    surtido = store_row['Assortment']

else:
    # MODO SIMULADOR
    st.markdown("### 🧪 Laboratorio de Simulación")
    st.info("Inventa tu propio escenario. ¿Qué pasaría si montas una tienda gigante con la competencia pegada a la puerta?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tienda_id = st.number_input("ID Tienda (Ficticio)", value=9999)
        fecha = st.date_input(
            "Fecha Simulada", 
            value=datetime.date(2026, 5, 14), # Por defecto en el futuro
            min_value=datetime.date(2013, 1, 1),
            max_value=datetime.date(2036, 12, 31)
        )
        promo = st.checkbox("Día de Promoción Activa", value=True)
        
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

# Extracción de Fecha
dia_semana = fecha.weekday() + 1
mes = fecha.month
dia = fecha.day
año = fecha.year

st.markdown("---")

# Botón y Predicción
if st.button("🚀 Calcular Ventas Estimadas", type="primary", use_container_width=True):
    
    # Construimos el diccionario con el ORDEN EXACTO de las 12 features
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
    
    # LÓGICA DE INFLACIÓN 
    año_actual = fecha.year
    años_diferencia = max(0, año_actual - 2015)
    multiplicador_inflacion = (1 + tasa_inflacion) ** años_diferencia
    prediccion_ajustada = prediccion_base * multiplicador_inflacion
    
    st.balloons()
    
    # Panel de métricas destacadas
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.metric(label="💰 Ventas Base (2015)", value=f"{prediccion_base:,.2f} €")
    with res_col2:
        st.metric(label="📈 Ajuste por Inflación", value=f"+ {((multiplicador_inflacion-1)*100):.1f} %")
    with res_col3:
        st.metric(label="🚀 PROYECCIÓN FINAL", value=f"{prediccion_ajustada:,.2f} €", delta="Estimación")

    st.markdown("---")
    
    # Visualización
    st.subheader("📊 Radiografía de la Decisión")
    st.write("¿Qué factores considera el modelo más importantes a nivel global para calcular las ventas?")
    
    # Extraemos las importancias directamente del Random Forest
    importancias = model.feature_importances_
    df_grafico = pd.DataFrame({
        'Variable': [
            'ID Tienda', 'Día Semana', 'Promoción', 'Mes', 'Día', 'Año', 
            'Distancia Competencia', 'Tienda Tipo B', 'Tienda Tipo C', 'Tienda Tipo D',
            'Surtido B', 'Surtido C'
        ],
        'Importancia (%)': importancias * 100
    }).sort_values(by='Importancia (%)', ascending=True)
    
    # Gráfico
    st.bar_chart(df_grafico, x='Variable', y='Importancia (%)', color="#1f77b4", height=350)

    # Demostración de los datos en bruto
    with st.expander("🔍 Ver matriz de datos (Input matemático de la IA)"):
        st.write("Para conseguir esta predicción, el modelo ha procesado esta fila de 12 variables exactas:")
        st.dataframe(input_df)

st.info("Nota metodológica: El modelo base Random Forest tiene una precisión del 80.75% (R²) con un error medio de 845.32 € en el set de validación.")