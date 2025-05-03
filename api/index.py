from flask import Flask, jsonify, request
from gradio_client import Client
import json

app = Flask(__name__)

def sanitize_output(data):
    if isinstance(data, dict):
        return {k: sanitize_output(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_output(item) for item in data]
    elif isinstance(data, bool):
        return str(data)
    return data

@app.route('/', methods=['GET'])
def generate_image():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        client = Client("NihalGazi/FLUX-Pro-Unlimited")
        result = client.predict(
            prompt=prompt,
            width=float(request.args.get('width', 1280)),
            height=float(request.args.get('height', 1280)),
            seed=float(request.args.get('seed', 0)),
            randomize=request.args.get('randomize', 'true').lower() == 'true',
            api_name="/predict"
        )

        # Convert Gradio response to JSON-safe format
        sanitized = sanitize_output(result)
        return jsonify(sanitized)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
