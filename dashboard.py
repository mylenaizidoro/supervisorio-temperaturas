import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Supervisório Industrial", page_icon="🌡️", layout="wide")

# Inicializa o estado para controlar se entrou ou não na máquina
if "maquina_selecionada" not in st.session_state:
    st.session_state.maquina_selecionada = False

# URL atualizada com o seu túnel ativo
API_GET_URL = "https://eight-bushes-attack.loca.lt/temperaturas"
HEADERS = {"serveo-skip-browser-warning": "true"}

# --- TELA INICIAL: ESCOLHA DA MÁQUINA ---
if not st.session_state.maquina_selecionada:
    st.title("🏭 Central de Supervisão - Células Industriais")
    st.write("Selecione abaixo a máquina que deseja monitorar em tempo real:")
    
    st.markdown("---")
    
    # Criando colunas para deixar o botão em destaque
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        # O botão que você pediu
        if st.button("🔥 Máquina de Solda - Temperaturas", use_container_width=True):
            st.session_state.maquina_selecionada = True
            st.rerun()

# --- TELA DE DETALHES: O PAINEL DE TEMPERATURAS ---
else:
    # Botão para voltar à seleção de máquinas
    if st.button("⬅️ Voltar para a Seleção de Máquinas"):
        st.session_state.maquina_selecionada = False
        st.rerun()

    st.title("🔥 Supervisório - Máquina de Solda (Temperaturas)")
    st.write("Acompanhamento em tempo real dos canais do CLP Delta DVP-12SE.")

    status_placeholder = st.empty()
    cards_placeholder = st.empty()
    grafico_placeholder = st.empty()

    # Loop de atualização em tempo real dos dados da API
    try:
        response = requests.get(API_GET_URL, headers=HEADERS, timeout=5)
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
                
                # Exibe os cards com os valores atuais
                with cards_placeholder.container():
                    st.subheader("📊 Valores Atuais por Sensor")
                    ultima_linha = df.iloc[-1]
                    cols = st.columns(6)
                    for idx, col in enumerate(cols):
                        if idx < 17:
                            sensor_nome = f"Sensor {idx+1}"
                            val = ultima_linha[sensor_nome]
                            col.metric(label=sensor_nome, value=f"{val} °C")

                # Exibe as opções de gráficos em abas (Linhas e Barras)
                with grafico_placeholder.container():
                    st.subheader("📈 Análise Gráfica dos Sensores")
                    
                    aba_linhas, aba_barras = st.tabs(["📈 Gráfico de Linhas (Tendência)", "📊 Gráfico de Barras (Comparativo)"])
                    
                    df_plot = df.set_index("timestamp")
                    
                    with aba_linhas:
                        st.line_chart(df_plot)
                        
                    with aba_barras:
                        df_barras = ultima_linha.drop("timestamp")
                        st.bar_chart(df_barras)
            else:
                status_placeholder.warning("⚠️ A API conectou, mas o histórico de dados ainda está vazio.")
        else:
            status_placeholder.warning(f"⚠️ A API respondeu com o código de status: {response.status_code}")

    except Exception as e:
        status_placeholder.error(f"❌ Erro ao conectar com a API FastAPI: {e}")
