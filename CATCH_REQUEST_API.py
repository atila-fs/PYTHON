#!/usr/bin/env python3

from flask import Flask, request
from datetime import datetime
import logging

# Configuração de log
logging.basicConfig(
    filename='/var/log/catcher.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
history = []

@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def catch_all(path):
    try:
        data = {
            "timestamp": datetime.now().isoformat(),
            "path": "/" + path,
            "method": request.method,
            "headers": dict(request.headers),
            "args": request.args.to_dict(),
            "body": request.get_data(as_text=True) or "",  # evita erro em GET
        }
        history.append(data)
        print(f"[{data['timestamp']}] {data['method']} {data['path']}")
        return {
            "status": "received",
            "path": data["path"],
            "count": len(history)
        }, 200
    except Exception as e:
        logger.error(f"Erro ao processar requisição para /{path}: {e}")
        return {"error": "Erro interno ao processar a requisição"}, 500

@app.route('/history', methods=["GET"])
def show_history():
    return {
        "requests": history[-50:]
    }, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)