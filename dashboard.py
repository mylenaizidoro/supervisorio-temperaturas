import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Supervisório Industrial", page_icon="🌡️", layout="wide")

# Inicializa o estado para controlar qual máquina foi selecionada
if "maquina_selecionada" not in st.session_state:
    st.session_state.maquina_selecionada = None

API_GET_URL = "https://eight-planes-cut.loca.lt/temperaturas"
HEADERS = {"serveo-skip-browser-warning": "true"}

# --- TELA INICIAL: ESCOLHA DA MÁQUINA ---
if st.session_state.maquina_selecionada is None:
    st.title("🏭 Central de Supervisão - Células Industriais")
    st.write("Selecione abaixo a máquina que deseja monitorar em tempo real:")
    
    st.markdown("---")
    
    # Botões organizados em pilha vertical com largura total
    if st.button("🔥 Máquina de Solda - Temperaturas", use_container_width=True):
        st.session_state.maquina_selecionada = "Máquina de Solda - Temperaturas"
        st.rerun()
        
    if st.button("📊 PH02 - Dash", use_container_width=True):
        st.session_state.maquina_selecionada = "PH02 - Dash"
        st.rerun()
        
    if st.button("🛡️ PH09 - Isolant Plancher", use_container_width=True):
        st.session_state.maquina_selecionada = "PH09 - Isolant Plancher"
        st.rerun()
        
    if st.button("⚙️ PH20 - XDF", use_container_width=True):
        st.session_state.maquina_selecionada = "PH20 - XDF"
        st.rerun()
        
    if st.button("🔧 PH03 - Isolador Tcross", use_container_width=True):
        st.session_state.maquina_selecionada = "PH03 - Isolador Tcross"
        st.rerun()

# --- TELA DE DETALHES: O PAINEL DE TEMPERATURAS ---
else:
    # Botão para voltar à seleção de máquinas
    if st.button("⬅️ Voltar para a Seleção de Máquinas"):
        st.session_state.maquina_selecionada = None
        st.rerun()

    st.title(f"🔥 Supervisório - {st.session_state.maquina_selecionada}")
    st.write("Acompanhamento em tempo real dos canais do CLP Delta DVP-12SE.")

    status_placeholder = st.empty()
    cards_placeholder = st.empty()
    grafico_placeholder = st.empty()

    try:
        response = requests.get(API_GET_URL, headers=HEADERS, timeout=15)
        
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
                
                with cards_placeholder.container():
                    st.subheader("📊 Valores Atuais por Sensor")
                    ultima_linha = df.iloc[-1]
                    cols = st.columns(6)
                    for idx, col in enumerate(cols):
                        if idx < 17:
                            sensor_nome = f"Sensor {idx+1}"
                            val = ultima_linha[sensor_nome]
                            col.metric(label=sensor_nome, value=f"{val} °C")

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
