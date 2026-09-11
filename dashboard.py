import streamlit as st
import requests
import pandas as pd
import time

# Configuração da página
st.set_page_config(
    page_title="Supervisório de Temperaturas - CLP",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ Painel de Monitoramento - Temperaturas CLP")
st.markdown("Acompanhamento em tempo real dos canais do CLP Delta DVP-12SE.")

# URL interna onde o FastAPI está rodando no mesmo container do Render
API_URL_INTERNA = "http://127.0.0.1:8000/temperaturas"

def buscar_dados():
    try:
        response = requests.get(API_URL_INTERNA, timeout=3)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

# Tenta buscar os dados com tratamento de espera
dados = buscar_dados()

if not dados:
    st.warning("⚠️ Aguardando conexão com a API de temperaturas ou nenhum dado enviado ainda. Verifique se o leitor do CLP está rodando na fábrica.")
else:
    # Pega o último registro enviado pelo CLP
    ultimo_registro = dados[-1]
    
    st.subheader(f"Última Atualização: {ultimo_registro.get('timestamp', 'N/A')}")
    
    # Exibe os sensores em cartões organizados
    colunas = st.columns(4)
    for i in range(1, 18):
        nome_sensor = f"sensor_{i}"
        valor = ultimo_registro.get(nome_sensor, 0.0)
        
        with colunas[(i - 1) % 4]:
            st.metric(label=f"Canal {i}", value=f"{valor} °C")

# Atualiza a página automaticamente a cada 5 segundos
time.sleep(5)
st.rerun()
