from flask import Flask, jsonify, request
from gradio_client import Client
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def generate_image():
    try:
        # Get parameters from query string
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        width = float(request.args.get('width', 1280))
        height = float(request.args.get('height', 1280))
        seed = float(request.args.get('seed', 0))
        randomize = request.args.get('randomize', 'true').lower() == 'true'

        # Initialize Gradio client
        client = Client("NihalGazi/FLUX-Pro-Unlimited")
        
        # Generate image
        result = client.predict(
            prompt=prompt,
            width=width,
            height=height,
            seed=seed,
            randomize=randomize,
            api_name="/predict"
        )

        # Convert result to JSON-serializable format
        if isinstance(result, dict):
            return jsonify({k: str(v) if isinstance(v, (list, dict)) else v for k, v in result.items()})
        return jsonify({"result": str(result)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
