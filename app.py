from flask import Flask, request, jsonify, send_from_directory
import importlib.util
import os

app = Flask(__name__, static_folder='.')

# Ordner mit allen Reward-Function-Dateien
MODELS_DIR = "reward_functions"

def load_reward_function(filename):
    """Lädt reward_function(params) aus einer Python-Datei im MODELS_DIR."""
    filepath = os.path.join(MODELS_DIR, filename)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Modell-Datei '{filename}' nicht gefunden")
    spec = importlib.util.spec_from_file_location("reward_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "reward_function"):
        raise AttributeError(f"'{filename}' enthält keine reward_function(params)")
    return module.reward_function

@app.route('/')
def index():
    """Liefert die HTML-Seite."""
    return send_from_directory('.', 'index.html')

@app.route('/models', methods=['GET'])
def list_models():
    """Listet alle verfügbaren Reward-Modelle im MODELS_DIR."""
    try:
        files = [f for f in os.listdir(MODELS_DIR) if f.endswith(".py")]
        return jsonify(files)
    except FileNotFoundError:
        return jsonify([])

@app.route('/reward', methods=['POST'])
def get_reward():
    """Berechnet den Reward mit der ausgewählten Reward-Function."""
    data = request.json
    model_file = data.get("model")
    params = data.get("params", {})

    if not model_file:
        return jsonify({"error": "Kein Modell angegeben"}), 400

    try:
        reward_func = load_reward_function(model_file)
        reward = reward_func(params)
        return jsonify({"reward": float(reward)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Flask startet standardmäßig auf Port 5000
    app.run(debug=True)
