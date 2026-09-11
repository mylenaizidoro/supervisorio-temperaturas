from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# Memória temporária para guardar as últimas leituras
historico_temperaturas: List[Dict[str, Any]] = []
MAX_HISTORICO = 50

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

@app.get("/", response_class=HTMLResponse)
def painel_visual():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Supervisório de Temperaturas - CLP</title>
        <style>
            body { background-color: #0e1117; color: #fafafa; font-family: sans-serif; padding: 20px; }
            h1 { color: #ff4b4b; }
            .card-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; margin-top: 20px; }
            .card { background-color: #262730; border-radius: 8px; padding: 12px; text-align: center; border: 1px solid #46485f; }
            .card h3 { margin: 0; font-size: 14px; color: #a3a8b8; }
            .card p { margin: 8px 0 0 0; font-size: 20px; font-weight: bold; color: #00ffcc; }
            .status { margin-top: 15px; font-style: italic; color: #888; }
        </style>
    </head>
    <body>
        <h1>🌡️ Painel de Monitoramento - Temperaturas CLP</h1>
        <p>Acompanhamento em tempo real dos canais do CLP Delta DVP-12SE.</p>
        <div id="timestamp" style="font-weight: bold; color: #ffa500; margin-bottom: 10px;">Aguardando dados...</div>
        <div class="card-container" id="grid-sensores"></div>

        <script>
            async function atualizarDados() {
                try {
                    let response = await fetch('/temperaturas');
                    let data = await response.json();
                    if (data.length > 0) {
                        let ultimo = data[data.length - 1];
                        document.getElementById('timestamp').innerText = "Última Atualização: " + (ultimo.timestamp || 'N/A');
                        
                        let grid = document.getElementById('grid-sensores');
                        grid.innerHTML = '';
                        
                        for (let i = 1; i <= 17; i++) {
                            let valor = ultimo['sensor_' + i] || 0.0;
                            let card = document.createElement('div');
                            card.className = 'card';
                            card.innerHTML = `<h3>Canal ${i}</h3><p>${valor.toFixed(1)} °C</p>`;
                            grid.appendChild(card);
                        }
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
