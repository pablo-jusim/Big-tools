from flask import Flask, request, jsonify
from flask_cors import CORS
from motor_inferencia import MotorInferencia

app = Flask(__name__)
CORS(app)  # Permite conexión desde tu chatbot (Netlify u otros dominios).

# Cargar el motor de inferencia
motor = MotorInferencia("base_conocimiento.json")

@app.route("/api/diagnostico", methods=["POST"])
def diagnostico():
    data = request.get_json()
    descripcion = data.get("descripcion", "").strip()

    if not descripcion:
        return jsonify({"error": "Debe enviarse una descripción del problema."}), 400

    resultado = motor.diagnosticar(descripcion)
    return jsonify(resultado)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "mensaje": "API del motor experto automotriz funcionando correctamente."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
