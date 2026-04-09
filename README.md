# Predicción de ventas en supermercados

## 1. Definición del Problema

**Enunciado del problema:**
El objetivo de este proyecto es predecir la demanda semanal de productos en distintas sucursales de una cadena de supermercados (Retail), basándonos en datos históricos de ventas, características de la tienda, festivos y condiciones meteorológicas.

**Contexto y justificación:**
Una gestión ineficiente del inventario en el sector retail provoca pérdidas millonarias, ya sea por exceso de stock (costes de almacenamiento y caducidad) o por rotura de stock (pérdida de ventas y clientes insatisfechos). Utilizar Machine Learning para predecir las ventas permite optimizar la cadena de suministro de forma proactiva. Además, este proyecto automatiza el flujo de datos para que las predicciones se actualicen de manera continua.

**Selección del conjunto de datos (Multifuente):**
Para este análisis, integraremos datos de tres fuentes distintas:
1. **Datos de ventas (CSV):** Histórico de ventas diarias, promociones e identificadores de productos extraídos de Kaggle.
2. **Datos de sucursales (Excel):** Metadatos de las tiendas (tipo de tienda, tamaño, surtido).
3. **Datos meteorológicos y temporales (API/JSON):** Uso de una API pública (ej. Open-Meteo) para incorporar el clima y calendarios de festivos, evaluando su impacto en la demanda.

**Objetivos específicos:**
* Desarrollar un pipeline automatizado de ingesta y limpieza de datos usando Dagster.
* Realizar un Análisis Exploratorio de Datos (EDA) integrando scripts de R para visualizaciones estadísticas avanzadas.
* Entrenar y evaluar modelos de Machine Learning (Scikit-Learn) para predecir las ventas numéricas.
* Desplegar una aplicación web interactiva interactiva con Streamlit para la visualización de resultados y toma de decisiones empresariales.