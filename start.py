import subprocess
import os

port = os.environ.get("PORT", "10000")

# Inicia o FastAPI em background na porta 8000 interna
fastapi_process = subprocess.Popen(
    ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
)

# Inicia o Streamlit usando a porta principal do Render
streamlit_process = subprocess.Popen(
    ["streamlit", "run", "dashboard.py", "--server.port", str(port), "--server.address", "0.0.0.0"]
)

fastapi_process.wait()
streamlit_process.wait()
