import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns

def plot_dau_wau_mau(dau, wau, mau):
    """
    Grafica DAU, WAU y MAU en subgráficos.
    """
    fig, ax = plt.subplots(1, 3, figsize=(19, 5))
    ax[0].plot(dau)
    ax[0].set(title='DAU', xlabel='Fecha', ylabel='Visitantes')
    ax[1].plot(wau)
    ax[1].set(title='WAU', xlabel='Semana', ylabel='Visitantes')
    ax[2].plot(mau)
    ax[2].set(title='MAU', xlabel='Mes', ylabel='Visitantes')
    fig.autofmt_xdate(rotation=30)
    plt.show()

def plot_sesiones_por_dia(sesiones_por_usuario):
    """
    Grafica el número de sesiones por día.
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=sesiones_por_usuario, x=sesiones_por_usuario.index, y='n_sesion', marker='o')
    plt.title('Número de Sesiones por Día')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Sesiones')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_duracion_sesion(df_visits):
    """
    Grafica la distribución de la duración de las sesiones.
    """
    plt.figure(figsize=(12, 6))
    sns.histplot(df_visits['duracion_sesion_seg'], bins=50, kde=True)
    plt.title('Distribución de la Duración de las Sesiones')
    plt.xlabel('Duración de la Sesión (segundos)')
    plt.ylabel('Frecuencia')
    plt.show()

def plot_frecuencia_regreso(category_counts):
    """
    Grafica la distribución de la frecuencia de regreso de los usuarios.
    """
    plt.figure(figsize=(10, 6))
    category_counts.plot(kind='bar', color='skyblue')
    plt.title('Frecuencia de Regreso de los Usuarios', fontsize=16)
    plt.xlabel('Categoría de Frecuencia de Regreso', fontsize=12)
    plt.ylabel('Número de Usuarios', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_conversion_categoria(conversion_counts):
    """
    Grafica la distribución de las conversiones entre la primera sesión y la primera compra.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x=conversion_counts.index, y=conversion_counts.values, palette='viridis')

    # Añadir títulos y etiquetas
    plt.title('Tiempo hasta la Primera Compra desde la Primera Sesión', fontsize=16)
    plt.xlabel('Categoría de Conversión', fontsize=12)
    plt.ylabel('Número de Usuarios', fontsize=12)

    # Mostrar el gráfico
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Funciones adicionales para los gráficos
def plot_ventas_por_mes(pedidos_totales_por_mes):
    """
    Grafica los pedidos totales por mes.
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=pedidos_totales_por_mes, x='buy_ts', y='n_pedidos', color='skyblue')
    plt.title('Total de Pedidos por Mes', fontsize=16)
    plt.xlabel('Mes', fontsize=12)
    plt.ylabel('Número de Pedidos', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_ticket_promedio(ticket_promedio):
    """
    Grafica el ticket promedio por usuario.
    """
    plt.figure(figsize=(12, 6))
    sns.histplot(ticket_promedio['revenue'], bins=30, kde=True, color='skyblue')
    plt.title('Distribución del Ticket Promedio por Usuario', fontsize=16)
    plt.xlabel('Valor Promedio de Compra ($)', fontsize=12)
    plt.ylabel('Frecuencia', fontsize=12)
    plt.tight_layout()
    plt.show()

def plot_ltv(ltv_pivot):
    """
    Visualiza el Lifetime Value (LTV) por cohorte de usuarios.
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(ltv_pivot, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=.5, linecolor='black')
    plt.title('LTV por Cohorte', fontsize=16)
    plt.xlabel('Mes desde la Primera Compra', fontsize=12)
    plt.ylabel('Mes de la Primera Compra (Cohorte)', fontsize=12)
    plt.show()

def plot_gastos_por_fuente(gastos_por_mes_fuente):
    """
    Grafica los gastos totales por fuente a lo largo del tiempo.
    """
    # Crear gráfico para mostrar gastos por fuente
    fig, ax = plt.subplots(figsize=(14, 7))
    for fuente in gastos_por_mes_fuente['source_id'].unique():
        fuente_data = gastos_por_mes_fuente[gastos_por_mes_fuente['source_id'] == fuente]
        ax.plot(fuente_data['mes'].astype(str), fuente_data['costs'], label=fuente)

    ax.set_title('Gastos por Fuente a lo Largo del Tiempo')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Gastos ($)')
    ax.legend(title='Fuente')
    plt.xticks(rotation=45)
    plt.show()


def plot_romi(romi):
    """
    Grafica el Return on Marketing Investment (ROMI) por fuente.
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=romi, x='mes', y='romi', hue='source_id')
    plt.title('Return on Marketing Investment (ROMI) por Fuente')
    plt.xlabel('Mes')
    plt.ylabel('ROMI')
    plt.legend(title='Fuente')
    plt.xticks(rotation=45)
    plt.show()
    

def plot_cac(cac):
    """
    Grafica el Customer Acquisition Cost (CAC) por fuente.
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=cac, x='mes', y='cac', hue='source_id', marker='o')
    plt.title('Customer Acquisition Cost (CAC) por Fuente y Mes')
    plt.xlabel('Mes')
    plt.ylabel('CAC ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


