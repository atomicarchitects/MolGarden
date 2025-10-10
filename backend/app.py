from flask import Flask, request, jsonify
from flask_cors import CORS
import torch

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load your PyTorch model here
# model = torch.load('your_model.pt')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict next atom given current molecule structure
    
    Request JSON format:
    {
        "atoms": [
            {"element": "C", "x": 0.0, "y": 0.0, "z": 0.0},
            ...
        ]
    }
    
    Response JSON format:
    {
        "element": "N",
        "x": 1.2,
        "y": 0.5,
        "z": -0.3,
        "stop": false
    }
    OR
    {
        "stop": true
    }
    """
    data = request.json
    atoms = data['atoms']
    
    # TODO: Process atoms and run through your PyTorch model
    # prediction = model.predict(atoms)
    
    # Example response (replace with your model output)
    return jsonify({
        "element": "N",
        "x": 1.5,
        "y": 0.5,
        "z": 0.0,
        "stop": False
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
