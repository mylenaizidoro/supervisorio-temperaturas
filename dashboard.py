import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Supervisório de Temperaturas", page_icon="🌡️", layout="wide")

st.title("🌡️ Painel de Monitoramento - Temperaturas CLP")
st.write("Acompanhamento em tempo real dos canais do CLP Delta DVP-12SE.")

status_placeholder = st.empty()
cards_placeholder = st.empty()
grafico_placeholder = st.empty()

API_GET_URL = "https://338bcf9f78c28e92-179-68-117-40.serveousercontent.com/temperaturas"

# Cabeçalho necessário para o Serveo liberar o acesso da API sem a página de aviso
HEADERS = {"serveo-skip-browser-warning": "true"}

while True:
    try:
        response = requests.get(API_GET_URL, headers=HEADERS)
        if response.status_code == 200:
            historico_bruto = response.json()
            
            if historico_bruto and isinstance(historico_bruto, list):
                dados_formatados = []
                for item in historico_bruto:
                    linha = {"timestamp": item.get("timestamp", "")}
                    for i in range(1, 18):
                        linha[f"Sensor {i}"] = item.get(f"sensor_{i}", 0.0)
                    dados_formatados.append(linha)
                
                df = pd.DataFrame(dados_formatados)
                
                status_placeholder.success(f"Última sincronização com a API: {df['timestamp'].iloc[-1]}")
                
                # Exibe os cards com os nomes "Sensor X"
                with cards_placeholder.container():
                    st.subheader("📊 Valores Atuais por Sensor")
                    ultima_linha = df.iloc[-1]
                    cols = st.columns(6)
                    for idx, col in enumerate(cols):
                        if idx < 17:
                            sensor_nome = f"Sensor {idx+1}"
                            val = ultima_linha[sensor_nome]
                            col.metric(label=sensor_nome, value=f"{val} °C")

                # Exibe o gráfico de linhas histórico
                with grafico_placeholder.container():
                    st.subheader("📈 Gráfico de Tendência dos Sensores")
                    df_plot = df.set_index("timestamp")
                    st.line_chart(df_plot)
            else:
                status_placeholder.warning("⚠️ A API conectou, mas o histórico de dados ainda está vazio.")
        else:
            status_placeholder.warning(f"⚠️ A API respondeu com o código de status: {response.status_code}")

    except Exception as e:
        status_placeholder.error(f"❌ Erro ao conectar com a API FastAPI: {e}")

    time.sleep(3)
