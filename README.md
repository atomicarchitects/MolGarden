# MolGarden

An interactive 3D molecule viewer and builder, with support for querying any 3D molecular generative model. Below is a demo with [Symphony](https://github.com/atomicarchitects/symphony):

<img width="1280" height="709" alt="symphony-demo-benzene-compressed" src="https://github.com/user-attachments/assets/4bf7aa28-722e-4ed3-b2e4-f7aba0bda094" />

Built on top of [JSmol](https://jmol.sourceforge.net/) for 3D visualization.

## Quick Start

### 1. Start the Backend

The backend corresponds to the model server, which will be queried for generation.

```bash
# Install dependencies (in your symphony environment)
pip install flask flask-cors

# Run with your trained checkpoint
python src/symphony/server.py \
    --checkpoint /path/to/checkpoint.ckpt \
    --device cuda \
    --port 5000
```

### 2. Serve the Frontend

```bash
# From the project root
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## How Generation Works

1. Click **Generate Step** to grow a molecule one atom at a time.
2. Enable **Auto-generate** to loop until the model emits a STOP token (molecule is complete).
3. Adjust inverse temperature parameters to control generation diversity:
   - **Focus τ** — controls which existing atom gets selected as the focus (anchor) for the new atom.
   - **Radial τ** — controls the distance of the new atom from the focus.
   - **Angular τ** — controls the direction of the new atom relative to the focus.
   - Higher values: more deterministic, lower values: more random.

## Other Features

- **Load structures** from PDB, Materials Project, and PubChem.
- **Upload files** in `.xyz`, `.pdb`, `.mol`, `.sdf`, `.cif` formats.
- **Manipulate atoms**: select, delete, expand selection.
- **Visualization controls**: display types, color schemes, isosurfaces, labels.
- **Export** as `.png`, `.xyz`, `.pdb`, `.mol`, `.sdf`, `.cif`.
