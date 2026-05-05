# 📈 Retail Sales Forecasting: Rossmann Analytics

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Orchestrator](https://img.shields.io/badge/Orchestrator-Dagster-252031.svg)](https://dagster.io/)
[![Deep Learning](https://img.shields.io/badge/Deep%20Learning-PyTorch-EE4C2C.svg)](https://pytorch.org/)

👉 **[Accede a la Demo en Vivo aquí](https://c2qhmuvymsjzvx6fnbb4fu.streamlit.app/)**

---

## 🎯 Objetivo del Proyecto y Problema que Resuelve

El **objetivo** de este proyecto es construir una solución integral de Ciencia de Datos y MLOps capaz de predecir las ventas diarias de las tiendas Rossmann. 

El **problema que resuelve** es la dificultad de estimar la demanda en el sector retail debido a factores volátiles como promociones, festivos, y la distancia a los competidores. La aplicación interactiva permite a los gerentes de las tiendas simular escenarios (ej. abrir una tienda nueva cerca de la competencia o activar una promoción) para anticipar los ingresos y optimizar el inventario o el personal.
  
---

## 🚀 Características Principales (Requisitos Avanzados)

Para este proyecto se han implementado técnicas avanzadas que van más allá del Machine Learning estándar:

1.  **📊 Integración Multilenguaje (R + Python):** Uso de scripts de **R** (`ggplot2`) integrados en el flujo de Python para visualizaciones estadísticas de alta calidad.
2.  **🐘 Big Data con Dask:** Procesamiento eficiente de datasets de gran escala (+1M de filas) optimizando el uso de memoria.
3.  **🔄 Orquestación con Dagster:** Pipeline de datos automatizado y profesional, asegurando la integridad y trazabilidad de los datos.
4.  **🧠 Deep Learning (PyTorch):** Experimento comparativo utilizando redes neuronales profundas para evaluar la precisión frente a modelos clásicos.

---

## 🛠️ Stack Tecnológico

| Fase | Herramientas |
| :--- | :--- |
| **Orquestación** | `Dagster` |
| **Procesamiento** | `Pandas`, `Dask`, `Numpy` |
| **Visualización** | `Seaborn`, `R (ggplot2)` |
| **Machine Learning** | `Scikit-Learn (Random Forest)` |
| **Deep Learning** | `PyTorch` |
| **Despliegue** | `Streamlit` |

---

## 📂 Estructura del Proyecto
```bash
├── main.py                 # Aplicación web de Streamlit (Punto de entrada principal)
├── data/                   # Datasets (CSV, Parquet, Excel)
├── notebooks/
│   ├── 01_exploracion.ipynb # EDA, Integración con R y Dask
│   └── 02_entrenamiento.ipynb # Modelado, PyTorch y Comparativa
├── src/
│   ├── dagster_pipeline.py # Código de orquestación
│   └── assets.py           # Definición de activos de datos
├── pyproject.toml          # Configuración de dependencias locales para uv
├── requirements.txt        # Dependencias ligeras para Streamlit Cloud
├── model_rossmann.joblib   # Modelo final entrenado
└── README.md               # Documentación
```

## 📈 Resultados del Modelo

Se realizó una comparativa técnica exhaustiva para seleccionar el algoritmo con mejor desempeño para el negocio:

* **🤖 Random Forest (Modelo Final):** Logró un Error Medio Absoluto (MAE) de **~851.37 €**. Es el modelo más robusto, capturando eficazmente la estacionalidad y el efecto de las promociones.
* **🧠 Deep Learning (PyTorch):** Tras un proceso de optimización con mini-batches y ajuste de arquitectura, se alcanzó un MAE de **~1771.53 €**. 

**Conclusión técnica:** Aunque la red neuronal muestra una curva de aprendizaje positiva, el **Random Forest** demuestra una superioridad clara en la gestión de datos tabulares y variables categóricas (como el tipo de tienda o surtido), justificando su elección para la aplicación en producción.

## 💻 Instalación y Reproducibilidad

El proyecto está configurado para utilizar `uv` como gestor de dependencias ultrarrápido, garantizando un entorno aislado y reproducible tal y como se solicita en los requisitos de entrega.

Sigue estos pasos para replicar el entorno y ejecutar el proyecto:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/pvalbla/prediccion_ventas_supermercados.git](https://github.com/pvalbla/prediccion_ventas_supermercados.git)
cd prediccion_ventas_supermercados
```

### 2. Crear el entorno e instalar dependencias con `uv`
```bash
uv venv --python 3.11
uv sync
```

### 3. Ejecutar la Aplicación Interactiva
```bash
streamlit run main.py
```

### 4. (Opcional) Ejecutar el Orquestador
Para visualizar la orquestación de datos:
```bash
dagster dev
```
