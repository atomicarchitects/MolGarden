import torch
import torch_geometric.transforms
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

import symphony.model
from symphony.data import AtomTypeTokenizer
from atomic_datasets import QM9

# Load your pre-trained model here
checkpoint_dir = "/home/ameyad/symphony-torch/outputs/train/dev/runs/2025-10-13_15-52-12/checkpoints/"
model = symphony.model.Symphony.load_from_checkpoint(f"{checkpoint_dir}/last.ckpt")
model.eval()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Molecule Generation API is running."

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    # Handle preflight request
    if request.method == 'OPTIONS':
        return '', 204


    data = request.json
    current_geometry = data.get('geometry', '').strip()
    
    atom_types = []
    coords = []
    
    # Parse current geometry if provided
    if current_geometry:
        lines = current_geometry.strip().split('\n')
        num_atoms = int(lines[0])
        
        for i in range(2, 2 + num_atoms):
            parts = lines[i].split()
            atom_types.append(parts[0])
            coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
        
        print(f"Received {num_atoms} atoms")
        
        prompt = data.get('prompt', None)
        print(f"Received prompt: {prompt}")
        
        pos = torch.tensor(coords, dtype=torch.float32)
        tokenizer = AtomTypeTokenizer(QM9.atom_types())
        species = tokenizer(atom_types)
        graph = torch_geometric.data.Data(
            pos=pos,
            species=species,
            conditioning=None,
            conditioning_valid=False,
            atomic_number_map=None,
            dataset_label=None,  # Changed from self.label() - 'self' doesn't exist here
            transform=None,  # Changed from self.transform
        )
        add_edges_fn = torch_geometric.transforms.RadiusGraph(r=10.0, loop=False)
        graph = add_edges_fn(graph)
        graph["num_graphs"] = 1
        graph["batch"] = torch.zeros(graph["pos"].shape[0], dtype=torch.long)
        graph = graph.to(model.device)
        
        with torch.inference_mode():
            pred = model.sample(graph)

        if pred["stop"]:
            print("Generation stopped by model.")
            new_graph = graph
        else:
            print("Appending new atom to the graph.")
            new_graph = symphony.utils.append_predictions_to_graph(graph, pred)
        
        atom_types = tokenizer.to_atom_types(new_graph.species.cpu().numpy().tolist())
        coords = new_graph.pos.cpu().numpy().tolist()
    
    else:
        atom_types = ['C']
        coords = [[0.0, 0.0, 0.0]]
    
    # Format as XYZ
    num_atoms = len(atom_types)
    xyz_lines = [str(num_atoms), "Generated molecule"]
    
    for atom_type, coord in zip(atom_types, coords):
        xyz_lines.append(f"{atom_type} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}")
    
    xyz_string = "\n".join(xyz_lines)
    return jsonify({'xyz': xyz_string})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)