# data_prep.py

import pandas as pd

def cargar_datos():
    """
    Carga los archivos CSV de las tres tablas (visits, orders, costs) y devuelve los DataFrames.
    """
    df_visits = pd.read_csv('../data/raw/visits_log_us.csv')
    df_orders = pd.read_csv('../data/raw/orders_log_us.csv')
    df_costs = pd.read_csv('../data/raw/costs_us.csv')

    return df_visits, df_orders, df_costs

def ajustar_tipos(df_visits, df_orders, df_costs):
    """
    Ajusta los tipos de datos de las columnas para fechas y identificadores.
    """
    df_orders.columns = [columna.lower().replace(' ', '_') for columna in df_orders.columns]
    df_visits.columns = [columna.lower().replace(' ', '_') for columna in df_visits.columns]
    df_costs.columns = [columna.lower().replace(' ', '_') for columna in df_costs.columns]

    # Convertir las columnas de fechas a datetime
    df_visits['start_ts'] = pd.to_datetime(df_visits['start_ts'])
    df_visits['end_ts'] = pd.to_datetime(df_visits['end_ts'])
    df_orders['buy_ts'] = pd.to_datetime(df_orders['buy_ts'])
    df_costs['dt'] = pd.to_datetime(df_costs['dt'])

    return df_visits, df_orders, df_costs

def exploracion_inicial(df):
    """
    Realiza una exploración inicial de los datos: muestra primeras filas, estructura, duplicados y valores faltantes.
    """
    print('-'*30 + 'Primeras filas' + '-'*30)
    print(df.head(10))  # Muestra las primeras filas
    print('-'*30 + 'Estructura de la tabla' + '-'*30)
    print(df.info())  # Muestra la estructura del DataFrame (tipos de datos, etc.)
    print('-'*30 + 'Duplicados' + '-'*30)
    print(df.duplicated().sum())  # Muestra el número de filas duplicadas
    print('-'*30 + 'Ausentes' + '-'*30)
    print(df.isna().sum())  # Muestra el número de valores faltantes

def limpiar_datos(df_visits, df_orders, df_costs):
    """
    Realiza la limpieza de datos verificando duplicados y valores faltantes.
    """
    print("Exploración de 'df_visits'")
    exploracion_inicial(df_visits)

    print("\nExploración de 'df_orders'")
    exploracion_inicial(df_orders)

    print("\nExploración de 'df_costs'")
    exploracion_inicial(df_costs)


