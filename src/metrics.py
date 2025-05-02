import pandas as pd

def calcular_dau_wau_mau(df_visits):
    """
    Calcula DAU (Usuarios Activos Diarios), WAU (Usuarios Activos Semanales) y MAU (Usuarios Activos Mensuales)
    y devuelve los resultados en un diccionario.
    """
    # Crear nuevas columnas para el mes, semana y fecha de la sesión
    df_visits['sesion_mes'] = pd.to_datetime(df_visits['start_ts'].dt.strftime('%Y-%m-01'))
    df_visits['sesion_semana'] = df_visits['start_ts'].dt.isocalendar().week
    df_visits['sesion_fecha'] = df_visits['start_ts'].dt.date

    # Calcular DAU, WAU, MAU
    dau = df_visits.groupby('sesion_fecha').agg({'uid': 'nunique'})
    wau = df_visits.groupby('sesion_semana').agg({'uid': 'nunique'})
    mau = df_visits.groupby('sesion_mes').agg({'uid': 'nunique'})

    return dau, wau, mau


def calcular_sesiones_por_dia(df_visits):
    """
    Calcula el número de sesiones por día.
    Un usuario puede tener más de una sesión.
    """
    # Calcular sesiones por usuario y día
    sesiones_por_usuario = df_visits.groupby('sesion_fecha').agg({'uid': ['count', 'nunique']})
    sesiones_por_usuario.columns = ['n_sesion', 'n_usuarios']
    return sesiones_por_usuario


def calcular_duracion_sesion(df_visits):
    """
    Calcula la duración de cada sesión.
    """
    # Verificar que las columnas 'start_ts' y 'end_ts' estén presentes
    if 'end_ts' not in df_visits.columns or 'start_ts' not in df_visits.columns:
        raise ValueError("Las columnas 'start_ts' o 'end_ts' no están presentes en df_visits")
    
    # Asegurarse de que las columnas estén en datetime
    df_visits['start_ts'] = pd.to_datetime(df_visits['start_ts'], errors='coerce')
    df_visits['end_ts'] = pd.to_datetime(df_visits['end_ts'], errors='coerce')

    # Verificar si hay valores nulos después de la conversión
    if df_visits['start_ts'].isna().sum() > 0 or df_visits['end_ts'].isna().sum() > 0:
        raise ValueError("Hay valores nulos en 'start_ts' o 'end_ts' después de la conversión")

    # Calcular la duración de la sesión en segundos
    df_visits['duracion_sesion_seg'] = (df_visits['end_ts'] - df_visits['start_ts']).dt.seconds
    
    # Retornar las columnas necesarias
    return df_visits[['sesion_fecha', 'uid', 'duracion_sesion_seg']]


def calcular_frecuencia_regreso(df_visits):
    """
    Calcula la frecuencia con la que los usuarios regresan al sitio web.
    """
    # Ordenar el DataFrame por Uid y Start_Ts
    visits_dif = df_visits.sort_values(['uid', 'start_ts']).copy()

    # Agrupar por Uid y calcular la diferencia entre el tiempo de inicio de sesiones consecutivas
    visits_dif['time_since_last_visit'] = visits_dif.groupby('uid')['start_ts'].diff()

    # Convertir la diferencia de tiempo en días
    visits_dif['days_since_last_visit'] = visits_dif['time_since_last_visit'].dt.days

    # Categorizar la frecuencia de regreso
    bins = [0, 1, 7, 30, 90, 365, float('inf')]
    labels = ['Mismo día', 'Dentro de la semana', 'Dentro del mes', 'Dentro de 3 meses', 'Dentro del año', 'Más de un año']
    visits_dif['return_frequency_category'] = pd.cut(visits_dif['days_since_last_visit'], bins=bins, labels=labels, right=False)

    # Imprimir las categorías de frecuencia de regreso
    print("\nCategorías de frecuencia de regreso:")
    print(visits_dif['return_frequency_category'].value_counts().sort_index())

    return visits_dif['return_frequency_category'].value_counts().sort_index()


def calcular_tiempo_hasta_compra(df_visits, df_orders):
    """
    Calcula el tiempo entre la primera sesión y la primera compra de un usuario.
    """
    # Calcular la primera sesión de cada usuario
    primeras_sesiones = df_visits.groupby('uid').agg({'start_ts': 'min'}).reset_index()
    primeras_sesiones.rename(columns={'start_ts': 'fecha_primera_sesion'}, inplace=True)

    # Asegurarse de que tenemos la fecha de la primera compra de cada usuario
    primeras_compras = df_orders.groupby('uid').agg({'buy_ts': 'min'}).reset_index()

    # Unir la información de la primera compra con el DataFrame de visitas (primeras sesiones)
    df_compras = pd.merge(primeras_compras, primeras_sesiones, on='uid', how='inner')

    # Calcular el tiempo entre la primera sesión y la primera compra
    df_compras['dias_hasta_compra'] = (df_compras['buy_ts'] - df_compras['fecha_primera_sesion']).dt.days

    # Clasificar a los usuarios según el tiempo hasta la primera compra (Conversion 0d, 1d, etc.)
    df_compras['conversion'] = pd.cut(df_compras['dias_hasta_compra'], bins=[-1, 0, 1, 7, 30, 365, float('inf')],
                                      labels=['Conversion 0d', 'Conversion 1d', 'Conversion 1w', 'Conversion 1m', 'Conversion 1y', 'Conversion >1y'])

    return df_compras

def calcular_pedidos_por_mes(df_orders):
    """
    Cuenta cuántos pedidos se hicieron por usuario durante un mes específico y calcula el total de pedidos por mes.
    """
    # Agrupar por mes y usuario, contando los pedidos
    pedidos_por_mes = df_orders.groupby([df_orders['buy_ts'].dt.to_period('M'), 'uid']).size().reset_index(name='n_pedidos')
    
    # Mostrar las primeras filas para verificar
    print("Pedidos por mes y usuario:")
    print(pedidos_por_mes.head())

    # Agrupar los pedidos por mes para obtener el total de pedidos por mes
    pedidos_totales_por_mes = pedidos_por_mes.groupby('buy_ts')['n_pedidos'].sum().reset_index()

    # Mostrar los resultados finales
    print("Total de pedidos por mes:")
    print(pedidos_totales_por_mes.head())
    
    return pedidos_totales_por_mes


def calcular_ticket_promedio(df_orders):
    """
    Calcula el tamaño promedio de compra por usuario.
    """
    ticket_promedio = df_orders.groupby('uid').agg({'revenue': 'mean'}).reset_index()
    return ticket_promedio


def calcular_ltv(df_orders):
    """
    Calcula el Lifetime Value (LTV) por cohorte de usuarios.
    """
    # Definir Cohortes (basado en la primera compra)
    first_purchase_date = df_orders.groupby('uid')['buy_ts'].min().reset_index()
    first_purchase_date['cohort_month'] = first_purchase_date['buy_ts'].dt.to_period('M')

    # Combinar la información de la cohorte con la tabla de órdenes
    df_orders_merged = pd.merge(df_orders, first_purchase_date[['uid', 'cohort_month']], on='uid')

    # Calcular el período relativo de cada orden dentro de la cohorte
    df_orders_merged['order_month'] = df_orders_merged['buy_ts'].dt.to_period('M')
    df_orders_merged['period_number'] = (df_orders_merged['order_month'] - df_orders_merged['cohort_month']).apply(lambda x: x.n)

    # Calcular los Ingresos por Cohorte a lo Largo del Tiempo
    cohort_revenue = df_orders_merged.groupby(['cohort_month', 'period_number'])['revenue'].sum().reset_index()

    # Calcular el LTV Promedio por Usuario en Cada Cohorte
    cohort_size = df_orders_merged.groupby('cohort_month')['uid'].nunique().reset_index()
    cohort_revenue = pd.merge(cohort_revenue, cohort_size, on='cohort_month')
    cohort_revenue['ltv'] = cohort_revenue['revenue'] / cohort_revenue['uid']

    # Pivotear la tabla para una mejor visualización del LTV por cohorte a lo largo del tiempo
    ltv_pivot = cohort_revenue.pivot_table(index='cohort_month', columns='period_number', values='ltv')

    # Imprimir la tabla LTV por Cohorte
    print("LTV por Cohorte:")
    ltv_pivot

    return ltv_pivot

def calculate_cac(df_orders, df_costs, df_visits):
    """
    Calcula el Customer Acquisition Cost (CAC) por fuente y mes.
    """
    # Unir df_orders con df_visits para obtener el 'source_id' de cada usuario
    df_orders = pd.merge(df_orders, df_visits[['uid', 'source_id']], on='uid', how='left')
    
    # Convertir la fecha de compra a periodo mensual
    df_orders['mes'] = df_orders['buy_ts'].dt.to_period('M')
    
    # Calcular el número de compradores únicos por fuente y mes
    compradores_por_fuente_mes = df_orders.groupby(['source_id', 'mes'])['uid'].nunique().reset_index(name='num_compradores')
    
    # Calcular los gastos totales por mes y fuente
    gastos_por_mes_fuente = df_costs.groupby(['mes', 'source_id']).agg({'costs': 'sum'}).reset_index()
    
    # Unir los datos de gastos con los compradores
    gastos_y_compradores = pd.merge(gastos_por_mes_fuente, compradores_por_fuente_mes, on=['source_id', 'mes'], how='left')
    
    # Calcular el CAC por fuente
    gastos_y_compradores['cac'] = gastos_y_compradores['costs'] / gastos_y_compradores['num_compradores']
    
    return gastos_y_compradores


def calculate_romi(df_orders, df_costs, df_visits):
    """
    Calcula el Return on Marketing Investment (ROMI) por fuente y mes.
    """
    # Calcular los ingresos por fuente y mes
    ingresos_por_fuente = df_orders.groupby(['source_id', 'mes'])['revenue'].sum().reset_index()
    
    # Calcular los gastos por mes y fuente
    gastos_por_mes_fuente = df_costs.groupby(['mes', 'source_id']).agg({'costs': 'sum'}).reset_index()
    
    # Unir los datos de ingresos y gastos
    romi = pd.merge(gastos_por_mes_fuente, ingresos_por_fuente, on=['source_id', 'mes'], how='left')
    
    # Calcular el ROMI
    romi['romi'] = (romi['revenue'] - romi['costs']) / romi['costs']
    
    return romi

