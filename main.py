from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# Lista para armazenar o histórico recente das temperaturas na memória
historico_temperaturas: List[Dict[str, Any]] = []
MAX_HISTORICO = 100  # Mantém os últimos 100 registros

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
    # Converte os dados recebidos para dicionário
    registro = dados.dict()
    
    # Adiciona ao histórico
    historico_temperaturas.append(registro)
    
    # Limita o tamanho do histórico para não encher a memória
    if len(historico_temperaturas) > MAX_HISTORICO:
        historico_temperaturas.pop(0)
        
    return {"status": "sucesso", "registros_salvos": len(historico_temperaturas)}

@app.get("/temperaturas")
def obter_temperaturas():
    return historico_temperaturas
