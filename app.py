from flask import Flask, request, jsonify
from flask_cors import CORS
from sistema_experto.motor_inferencia import MotorDiagnostico

app = Flask(__name__)
CORS(app)  # Permite conexión desde cualquier origen.

# --- Inicialización del Sistema Experto ---
# Se instancia el motor UNA SOLA VEZ cuando la aplicación arranca.
# Asegúrate de que 'base_conocimiento_completa.json' esté en la misma carpeta.
motor = MotorDiagnostico("base_hidrolavadora.json")

@app.route("/api/diagnostico", methods=["POST"])
def diagnostico_conversacional():
    """
    Endpoint principal para el diagnóstico.
    Maneja tanto el inicio de la conversación como los turnos subsiguientes.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "La solicitud debe ser en formato JSON."}), 400

    # Determinar si es el inicio de una conversación o un turno intermedio.
    if 'descripcion' in data:
        # INICIO DE LA CONVERSACIÓN
        descripcion = data['descripcion'].strip()
        if not descripcion:
            return jsonify({"error": "La 'descripcion' no puede estar vacía."}), 400
        
        # El motor inicia el diagnóstico y devuelve la primera pregunta/solución y el estado.
        resultado = motor.iniciar_diagnostico(descripcion)
        return jsonify(resultado)

    elif 'estado' in data and 'respuesta' in data:
        # TURNO INTERMEDIO DE LA CONVERSACIÓN
        estado = data['estado']
        respuesta = data['respuesta'].lower()

        if respuesta not in ['si', 'no']:
            return jsonify({"error": "La 'respuesta' debe ser 'si' o 'no'."}), 400
        if not isinstance(estado, dict):
             return jsonify({"error": "El 'estado' debe ser un objeto JSON válido."}), 400

        # El motor procesa la respuesta y devuelve el siguiente paso.
        resultado = motor.procesar_respuesta(estado, respuesta)
        return jsonify(resultado)

    else:
        # Si la solicitud no tiene el formato esperado.
        return jsonify({
            "error": "Solicitud inválida. Debe contener 'descripcion' (para iniciar) o 'estado' y 'respuesta' (para continuar)."
        }), 400

@app.route("/", methods=["GET"])
def index():
    """Página de bienvenida para confirmar que la API está funcionando."""
    return jsonify({
        "mensaje": "API del Sistema Experto de Diagnóstico para Hidrolavadoras funcionando."
    })

if __name__ == "__main__":
    # Ejecutar en modo de producción usaría un servidor como Gunicorn o Waitress.
    # Para desarrollo, el servidor de Flask es suficiente.
    app.run(host="0.0.0.0", port=5000)
