import subprocess
import sys
import time
import os

port = os.environ.get("PORT", "10000")

def run_api():
    # Roda o FastAPI na porta interna 8000
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])

def run_streamlit():
    # Dá um tempinho para a API subir e inicia o Streamlit na porta do Render
    time.sleep(3)
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port", port, "--server.address", "0.0.0.0"])

if __name__ == "__main__":
    import threading
    
    # Inicia a API em uma linha separada (background)
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Roda o Streamlit na linha principal
    run_streamlit()
