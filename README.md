# Nombre del Proyecto: Análisis de Marketing Showz

## Resumen
Este repositorio contiene el análisis de los datos de marketing de Showz, enfocado en entender el comportamiento de los usuarios y el rendimiento de las ventas. El proyecto utiliza diversas técnicas de procesamiento de datos, visualización e informes para generar información a partir de los datos crudos, incluidos los registros de visitas de usuarios, pedidos y costos de marketing.

## Estructura del Proyecto

- `data/`
  - `raw/` - Archivos de datos crudos que se importan al proyecto.
  - `interim/` - Archivos temporales antes de ser procesados.
  - `processed/` - Archivos de datos procesados y limpiados para análisis.

- `notebooks/` - Jupyter notebooks utilizados para el análisis.
  - `PSet4_Showz_Marketing.ipynb` - Notebook principal con todo el análisis y visualizaciones.
  - `PSet4_Backup.ipynb` - Respaldo del análisis anterior para comparación.

- `reports/`
  - `figures/` - Gráficos y visualizaciones generados durante el análisis. Todos los gráficos generados durante el análisis se guardan en esta carpeta, lo que permite la visualización de las métricas clave en cualquier momento.
  - `executive_summary.md` - Archivo markdown que resume los hallazgos clave del análisis.

- `src/`
  - `data_prep.py` - Funciones para cargar y limpiar los datos.
  - `metrics.py` - Funciones para calcular métricas clave como DAU, WAU, MAU, etc.
  - `viz.py` - Funciones para visualizar los resultados y generar gráficos.

- `.gitignore` - Archivos que deben ser ignorados por Git (por ejemplo, `__pycache__`, `.DS_Store`, etc.)
- `requirements.txt` - Dependencias de Python necesarias para ejecutar el proyecto.
- `README.md` - Documentación del proyecto.

## Cómo Empezar

### Dependencias

Puedes instalar las bibliotecas necesarias ejecutando el siguiente comando:

```bash
pip install -r requirements.txt
pip install -r requirements.txt
