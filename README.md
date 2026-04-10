# 📈 Retail Sales Forecasting: Rossmann Analytics

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Orchestrator](https://img.shields.io/badge/Orchestrator-Dagster-252031.svg)](https://dagster.io/)
[![Deep Learning](https://img.shields.io/badge/Deep%20Learning-PyTorch-EE4C2C.svg)](https://pytorch.org/)

Este proyecto implementa una solución integral de **Ciencia de Datos y Machine Learning** para la predicción de ventas en una cadena de supermercados (Rossmann). Cubre desde la orquestación de datos masivos hasta el despliegue de una aplicación web interactiva.

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
├── app/
│   └── app.py              # Aplicación web de Streamlit
├── data/                   # Datasets (CSV, Parquet, Excel)
├── notebooks/
│   ├── 01_exploracion.ipynb # EDA, Integración con R y Dask
│   └── 02_entrenamiento.ipynb # Modelado, PyTorch y Comparativa
├── src/
│   ├── dagster_pipeline.py # Código de orquestación
│   └── assets.py           # Definición de activos de datos
├── model_rossmann.joblib   # Modelo final entrenado
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación

## 📈 Resultados del Modelo

Se realizó una comparativa técnica exhaustiva para seleccionar el algoritmo con mejor desempeño para el negocio:

* **🤖 Random Forest (Modelo Final):** Logró un Error Medio Absoluto (MAE) de **~634.65 €**. Es el modelo más robusto, capturando eficazmente la estacionalidad y el efecto de las promociones.
* **🧠 Deep Learning (PyTorch):** Tras un proceso de optimización con mini-batches y ajuste de arquitectura, se alcanzó un MAE de **~1809.79 €**. 

**Conclusión técnica:** Aunque la red neuronal muestra una curva de aprendizaje positiva, el **Random Forest** demuestra una superioridad clara en la gestión de datos tabulares y variables categóricas (como el tipo de tienda o surtido), justificando su elección para la aplicación en producción.

## 💻 Instalación y Uso

Sigue estos pasos para replicar el entorno y ejecutar el proyecto:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/nombre-del-repo.git
   cd nombre-del-repo

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt

3. **Ejecutar la App de Streamlit:**
   ```bash
   streamlit run app/app.py