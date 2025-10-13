from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    current_geometry = data.get('geometry', '').strip()

    atoms = []
    coords = []

    # Parse current geometry if provided
    if current_geometry:
        lines = current_geometry.strip().split('\n')
        num_atoms = int(lines[0])
        
        for i in range(2, 2 + num_atoms):
            parts = lines[i].split()
            atoms.append(parts[0])
            coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
        
        print(f"Received {num_atoms} atoms")

    prompt = data.get('prompt', None)
    print(f"Received prompt: {prompt}")

    # Call the model with current geometry as context
    # new_atoms, new_coords = your_model.generate(
    #     current_atoms=atoms,
    #     current_coords=coords,
    #     prompt=prompt
    # )

    # For demonstration, we'll just add a random atom.
    next_atom = np.random.choice(['C', 'H', 'O', 'N'], size=1).tolist()
    next_coord = (2 * np.random.rand(3)).tolist()

    atoms.append(next_atom)
    coords.append(next_coord)
    
    # Format as XYZ
    num_atoms = len(atoms)
    xyz_lines = [str(num_atoms), "Generated molecule"]
    
    for atom, coord in zip(atoms, coords):
        xyz_lines.append(f"{atom} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}")
    
    xyz_string = "\n".join(xyz_lines)
    return jsonify({'xyz': xyz_string})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)