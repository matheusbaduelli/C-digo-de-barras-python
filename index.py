from flask import Flask, request, send_file, abort
import barcode
from barcode.writer import ImageWriter
import io

app = Flask(__name__)

# 👉 GET na raiz do projeto
@app.route("/", methods=["GET"])
def home():
    return "API funcionando", 200


# 👉 Endpoint para gerar código de barras
@app.route("/barcode", methods=["GET"])
def gerar_barcode():
    texto = request.args.get("text")

    if not texto:
        abort(400, "Parâmetro 'text' é obrigatório")

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

