import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Gestor Financiero 💰", layout="wide")

# Inicializar datos en memoria (sin persistencia)
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# --- Funciones de cálculo ---
def get_balance():
    ingresos = sum(t['amount'] for t in st.session_state.transactions if t['type'] == 'ingreso')
    gastos = sum(t['amount'] for t in st.session_state.transactions if t['type'] == 'gasto')
    return ingresos - gastos

# --- Sidebar (Formulario) ---
with st.sidebar:
    st.header("➕ Nueva Transacción")
    transaction_type = st.selectbox("Tipo:", ["ingreso", "gasto"], index=0)
    name = st.text_input("Concepto:")
    amount = st.number_input("Monto ($):", min_value=0.0, step=0.01)
    if st.button("Agregar"):
        if name and amount > 0:
            new_transaction = {
                "name": name,
                "amount": amount,
                "type": transaction_type,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.transactions.append(new_transaction)
            st.success("¡Transacción agregada!")
        else:
            st.error("⚠️ Completa todos los campos.")

# --- Dashboard Principal ---
st.title("📊 Gestor Financiero Personal")

# Métricas rápidas
ingresos_totales = sum(t['amount'] for t in st.session_state.transactions if t['type'] == 'ingreso')
gastos_totales = sum(t['amount'] for t in st.session_state.transactions if t['type'] == 'gasto')
saldo = get_balance()

col1, col2, col3 = st.columns(3)
col1.metric("Ingresos Totales", f"${ingresos_totales:,.2f}")
col2.metric("Gastos Totales", f"${gastos_totales:,.2f}")
col3.metric("Saldo Actual", f"${saldo:,.2f}", delta_color="inverse" if saldo < 0 else "normal")

# --- Gráficos ---
if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    
    # Gráfico de historial
    st.subheader("Historial de Transacciones")
    fig = px.line(df, x="date", y="amount", color="type", markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Análisis por categoría
    st.subheader("Desglose por Categoría")
    analysis_type = st.selectbox("Tipo a analizar:", ["gastos", "ingresos"],index=0)
    filtered_df = df[df["type"] == analysis_type[:-1]]  # Remove 's' at the end
    if not filtered_df.empty:
        fig2 = px.pie(filtered_df, names="name", values="amount", title=f"Distribución de {analysis_type}")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No hay transacciones registradas aún.")

# --- Tabla de transacciones ---
st.subheader("📝 Lista Completa")
if st.session_state.transactions:
    st.dataframe(df, hide_index=True)