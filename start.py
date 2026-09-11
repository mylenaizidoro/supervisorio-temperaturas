import subprocess
import os

port = os.environ.get("PORT", "10000")

# Inicia o FastAPI (API) em background na porta interna 8000
api_process = subprocess.Popen(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])

# Inicia o Streamlit (Painel) na porta principal do Render
streamlit_process = subprocess.Popen(["streamlit", "run", "dashboard.py", "--server.port", port, "--server.address", "0.0.0.0"])

api_process.wait()
streamlit_process.wait()
