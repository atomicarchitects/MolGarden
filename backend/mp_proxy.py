from flask import Flask, Response
from flask_cors import CORS
import requests
from optimade.adapters import Structure
from optimade.adapters.structures.cif import get_cif

app = Flask(__name__)
CORS(app)

@app.route('/mp/<mp_id>')
def get_structure(mp_id):
    print(f"Received request for: {mp_id}")
    
    try:
        # Get JSON data from OPTIMADE API
        url = f'https://optimade.materialsproject.org/v1/structures/{mp_id}'
        response = requests.get(url)
        
        if response.status_code != 200:
            return {'error': 'Structure not found'}, 404
        
        data = response.json()

        # Convert to CIF using optimade-python-tools
        structure = Structure(data['data'])
        cif_content = get_cif(structure)
        
        print(f"Successfully converted {mp_id} to CIF")
        return Response(cif_content, mimetype='text/plain')
        
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return {'error': ve}, 400


if __name__ == '__main__':
    print("Starting proxy server on http://localhost:5001")
    app.run(port=5001, debug=True)