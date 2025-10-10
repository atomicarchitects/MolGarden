# MolView

A simple 3D molecule viewer, built on top of [JSMol](https://jmol.sourceforge.net/).
Interfaces with the Protein Data Bank (PDB), Materials Project and PubChem.
Also supports saving screenshots.

![Example UI of MolView](ui.png)

## How to run locally?

```bash
git clone https://github.com/atomicarchitects/MolView.git
cd MolView
python -m http.server 8000
```

and then navigate to http://localhost:8000/.

### For Materials Project

To query the Materials Project, you need to start a proxy server that will query OPTIMADE (no API key required) for you.

```bash
uv venv
source .venv/bin/activate
uv pip install optimade flask flask-cors numpy
python backend/mp_proxy.py
```

You can then enter the Materials Project entry that you wish to visualize in the UI.
