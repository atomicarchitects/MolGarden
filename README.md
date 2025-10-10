# MolView

A simple 3D molecule viewer, built on top of JSMol

![Example UI of MolView](ui.png)

## Setup

### Frontend
```bash
python -m http.server 8000
```
and then navigate to http://localhost:8000/.

### Backend (For Materials Project Only)

To query the Materials Project, you need to start a proxy server that will query OPTIMADE (no API key required) for you.

```bash
uv venv
source .venv/bin/activate
uv pip install optimade flask flask-cors numpy
python backend/mp_proxy.py
```

You can then enter the Materials Project entry that you wish to visualize in the UI.
