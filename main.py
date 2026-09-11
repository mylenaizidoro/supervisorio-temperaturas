from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import io
import csv

app = FastAPI()

# Memória temporária para guardar as últimas leituras da Máquina de Solda (aumentado para 100 registros)
historico_temperaturas: List[Dict[str, Any]] = []
MAX_HISTORICO = 100

class LeituraPayload(BaseModel):
    timestamp: str
    sensor_1: float = 0.0
    sensor_2: float = 0.0
    sensor_3: float = 0.0
    sensor_4: float = 0.0
    sensor_5: float = 0.0
    sensor_6: float = 0.0
    sensor_7: float = 0.0
    sensor_8: float = 0.0
    sensor_9: float = 0.0
    sensor_10: float = 0.0
    sensor_11: float = 0.0
    sensor_12: float = 0.0
    sensor_13: float = 0.0
    sensor_14: float = 0.0
    sensor_15: float = 0.0
    sensor_16: float = 0.0
    sensor_17: float = 0.0

@app.post("/temperaturas")
def receber_temperaturas(dados: LeituraPayload):
    registro = dados.dict()
    historico_temperaturas.append(registro)
    if len(historico_temperaturas) > MAX_HISTORICO:
        historico_temperaturas.pop(0)
    return {"status": "sucesso", "registros_salvos": len(historico_temperaturas)}

@app.get("/temperaturas")
def obter_temperaturas():
    if not historico_temperaturas:
        return []
    return historico_temperaturas

# Rota para baixar os dados em formato Excel (CSV compatível)
@app.get("/baixar-excel")
def baixar_excel():
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';') # Ponto e vírgula funciona melhor no Excel em português
    
    # Cabeçalho da planilha
    cabecalho = ["Timestamp"] + [f"Sensor {i} (°C)" for i in range(1, 18)]
    writer.writerow(cabecalho)
    
    # Adicionar as linhas do histórico (da mais recente para a mais antiga ou ordem cronológica)
    for reg in historico_temperaturas:
        linha = [reg.get("timestamp", "")]
        for i in range(1, 18):
            linha.append(reg.get(f"sensor_{i}", 0.0))
        writer.writerow(linha)
    
    output.seek(0)
    response = StreamingResponse(
        iter([output.getvalue().encode('utf-8-sig')]), # utf-8-sig ajuda o Excel a ler os acentos perfeitamente
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=historico_temperaturas_solda.csv"
    return response

# Rota da Tela Inicial com os Botões das Máquinas
@app.get("/", response_class=HTMLResponse)
def tela_inicial():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>COPLAC - Central de Supervisório</title>
        <style>
            body { 
                background-color: #0e1117; 
                color: #fafafa; 
                font-family: sans-serif; 
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                justify-content: center; 
                height: 100vh; 
                margin: 0; 
            }
            .container { 
                text-align: center; 
                background: #262730; 
                padding: 40px; 
                border-radius: 12px; 
                border: 1px solid #46485f; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                max-width: 520px;
                width: 90%;
            }
            .logo-coplac { 
                font-family: 'Georgia', serif; 
                font-size: 38px; 
                font-weight: bold; 
                font-style: italic; 
                color: #cc2929; 
                letter-spacing: 2px; 
                margin-bottom: 5px; 
            }
            .sub-logo { font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 25px; }
            h1 { color: #fafafa; font-size: 20px; margin-bottom: 10px; }
            p { color: #a3a8b8; margin-bottom: 30px; font-size: 14px; }
            .btn-grupo { display: flex; flex-direction: column; gap: 15px; }
            .btn-app { 
                background-color: #cc2929; 
                color: white; 
                padding: 16px 20px; 
                font-size: 15px; 
                font-weight: bold; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                text-decoration: none; 
                display: block; 
                transition: background 0.3s;
            }
            .btn-app:hover { background-color: #e63939; }
            .btn-secundario { background-color: #363846; border: 1px solid #46485f; }
            .btn-secundario:hover { background-color: #46485f; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-coplac">COPLAC</div>
            <div class="sub-logo">Automation Systems</div>
            <h1>Central de Automação Industrial</h1>
            <p>Selecione o equipamento desejado para monitoramento:</p>
            <div class="btn-grupo">
                <a href="/painel" class="btn-app">🌡️ DADOS DE TEMPERATURA MÁQUINA DE SOLDA</a>
                <a href="/ph02-dash" class="btn-app btn-secundario">⚙️ PH02 - DASH (EM BREVE)</a>
                <a href="/ph03-isolador" class="btn-app btn-secundario">⚡ PH03 - ISOLADOR T CROSS (EM BREVE)</a>
            </div>
        </div>
    </body>
    </html>
    """

# Rota do Painel da Máquina de Solda (com Cards, Tabela de Histórico e Botão Excel)
@app.get("/painel", response_class=HTMLResponse)
def painel_visual():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>COPLAC - Supervisório Máquina de Solda</title>
        <style>
            body { background-color: #0e1117; color: #fafafa; font-family: sans-serif; padding: 20px; }
            .header-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid #262730; padding-bottom: 15px; }
            .logo-coplac { font-family: 'Georgia', serif; font-size: 26px; font-weight: bold; font-style: italic; color: #cc2929; letter-spacing: 1px; }
            h1 { color: #fafafa; margin: 0; font-size: 20px; }
            .acoes-topo { display: flex; gap: 10px; align-items: center; }
            .btn-voltar { background-color: #46485f; color: white; padding: 10px 16px; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
            .btn-voltar:hover { background-color: #5c5f78; }
            .btn-excel { background-color: #217346; color: white; padding: 10px 16px; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; display: flex; align-items: center; gap: 6px; }
            .btn-excel:hover { background-color: #2ea043; }
            
            .card-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 12px; margin-top: 15px; }
            .card { background-color: #262730; border-radius: 8px; padding: 10px; text-align: center; border: 1px solid #46485f; }
            .card h3 { margin: 0; font-size: 13px; color: #a3a8b8; }
            .card p { margin: 6px 0 0 0; font-size: 18px; font-weight: bold; color: #00ffcc; }
            
            .secao-historico { margin-top: 35px; background: #262730; padding: 20px; border-radius: 8px; border: 1px solid #46485f; }
            .secao-historico h2 { font-size: 16px; margin-top: 0; color: #fafafa; margin-bottom: 15px; }
            .tabela-wrapper { max-height: 300px; overflow-y: auto; border-radius: 4px; }
            table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }
            th, td { padding: 10px; border-bottom: 1px solid #363846; }
            th { background-color: #1e1f26; color: #ffa500; position: sticky; top: 0; z-index: 1; }
            tr:hover { background-color: #2e303b; }
        </style>
    </head>
    <body>
        <div class="header-bar">
            <div>
                <div class="logo-coplac">COPLAC</div>
                <h1>🌡️ Temperaturas - Máquina de Solda</h1>
            </div>
            <div class="acoes-topo">
                <a href="/baixar-excel" class="btn-excel">📊 Baixar em Excel</a>
                <a href="/" class="btn-voltar">⬅ Voltar ao Menu</a>
            </div>
        </div>

        <div id="timestamp" style="font-weight: bold; color: #ffa500; margin-bottom: 10px;">Aguardando dados...</div>
        
        <!-- Cards dos 17 Canais em Tempo Real -->
        <div class="card-container" id="grid-sensores"></div>

        <!-- Tabela de Histórico Recente -->
        <div class="secao-historico">
            <h2>📜 Histórico de Leituras Recentes</h2>
            <div class="tabela-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>C1</th><th>C2</th><th>C3</th><th>C4</th><th>C5</th>
                            <th>C6</th><th>C7</th><th>C8</th><th>C9</th><th>C10</th>
                            <th>C11</th><th>C12</th><th>C13</th><th>C14</th><th>C15</th>
                            <th>C16</th><th>C17</th>
                        </tr>
                    </thead>
                    <tbody id="tabela-corpo">
                        <tr><td colspan="18" style="text-align: center; color: #888;">Carregando histórico...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <script>
            async function atualizarDados() {
                try {
                    let response = await fetch('/temperaturas');
                    let data = await response.json();
                    if (data.length > 0) {
                        let ultimo = data[data.length - 1];
                        document.getElementById('timestampถาน').innerText = "Última Atualização: " + (ultimo.timestamp || 'N/A');
                        document.getElementById('timestamp').innerText = "Última Atualização: " + (ultimo.timestamp || 'N/A');
                        
                        // Atualiza os Cards dos 17 canais
                        let grid = document.getElementById('grid-sensores');
                        grid.innerHTML = '';
                        for (let i = 1; i <= 17; i++) {
                            let valor = ultimo['sensor_' + i] || 0.0;
                            let card = document.createElement('div');
                            card.className = 'card';
                            card.innerHTML = `<h3>Canal ${i}</h3><p>${valor.toFixed(1)} °C</p>`;
                            grid.appendChild(card);
                        }

                        // Atualiza a Tabela de Histórico (invertida para mostrar os mais recentes primeiro)
                        let corpoTabela = document.getElementById('tabela-corpo');
                        corpoTabela.innerHTML = '';
                        let dadosInvertidos = [...data].reverse();
                        
                        dadosInvertidos.forEach(row => {
                            let tr = document.createElement('tr');
                            let html = `<td><b>${row.timestamp || ''}</b></td>`;
                            for (let i = 1; i <= 17; i++) {
                                let val = row['sensor_' + i] !== undefined ? row['sensor_' + i].toFixed(1) : '0.0';
                                html += `<td>${val}°C</td>`;
                            }
                            tr.innerHTML = html;
                            corpoTabela.appendChild(tr);
                        });
                    }
                } catch (e) {
                    console.log("Erro ao buscar dados", e);
                }
            }
            setInterval(atualizarDados, 3000);
            atualizarDados();
        </script>
    </body>
    </html>
    """

# Rotas auxiliares para as outras máquinas
@app.get("/ph02-dash", response_class=HTMLResponse)
def ph02_dash():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8"><title>COPLAC - PH02 Dash</title>
        <style>
            body { background-color: #0e1117; color: #fafafa; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .container { text-align: center; background: #262730; padding: 40px; border-radius: 12px; border: 1px solid #46485f; max-width: 450px; width: 90%; }
            .logo-coplac { font-family: 'Georgia', serif; font-size: 28px; font-weight: bold; font-style: italic; color: #cc2929; margin-bottom: 5px; }
            h1 { font-size: 22px; margin-bottom: 10px; } p { color: #a3a8b8; margin-bottom: 30px; font-size: 15px; }
            .btn-voltar { background-color: #46485f; color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; font-size: 14px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-coplac">COPLAC</div>
            <h1>⚙️ PH02 - Dash</h1>
            <p>Painel em fase de estruturação e integração de dados.</p>
            <a href="/" class="btn-voltar">⬅ Voltar ao Menu</a>
        </div>
    </body>
    </html>
    """

@app.get("/ph03-isolador", response_class=HTMLResponse)
def ph03_isolador():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8"><title>COPLAC - PH03 Isolador</title>
        <style>
            body { background-color: #0e1117; color: #fafafa; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .container { text-align: center; background: #262730; padding: 40px; border-radius: 12px; border: 1px solid #46485f; max-width: 450px; width: 90%; }
            .logo-coplac { font-family: 'Georgia', serif; font-size: 28px; font-weight: bold; font-style: italic; color: #cc2929; margin-bottom: 5px; }
            h1 { font-size: 22px; margin-bottom: 10px; } p { color: #a3a8b8; margin-bottom: 30px; font-size: 15px; }
            .btn-voltar { background-color: #46485f; color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; font-size: 14px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-coplac">COPLAC</div>
            <h1>⚡ PH03 - Isolador T Cross</h1>
            <p>Painel em fase de estruturação e integração de dados.</p>
            <a href="/" class="btn-voltar">⬅ Voltar ao Menu</a>
        </div>
    </body>
    </html>
    """
