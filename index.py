from flask import Flask, request, send_file, abort
import barcode
from barcode.writer import ImageWriter
import io

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "API funcionando", 200

@app.route("/api", methods=["GET"])
def api_home():
    return "API funcionando", 200

@app.route("/api/barcode", methods=["GET"])
def gerar_barcode():
    texto = request.args.get("text")

    if not texto:
        return {"error": "Parâmetro 'text' é obrigatório"}, 400

    try:
        code = barcode.get("code128", texto, writer=ImageWriter())
        
        buffer = io.BytesIO()
        code.write(buffer)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="image/png",
            as_attachment=False,
            download_name="barcode.png"
        )
    except Exception as e:
        return {"error": str(e)}, 500
