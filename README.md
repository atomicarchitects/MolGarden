# MolView

A simple 3D molecule viewer, built on top of [JSMol](https://jmol.sourceforge.net/).
Interfaces with the Protein Data Bank (PDB), Materials Project and PubChem.
Also supports saving screenshots.

![Example MolView UI](ui.png)

## How to run locally?

```bash
git clone https://github.com/atomicarchitects/MolView.git
cd MolView
python -m http.server 8000
```

and then navigate to http://localhost:8000/.

### For Materials Project

We have a setup a proxy server via Google Cloud Run to query the Materials Project via OPTIMADE (no API key required).

If you want to run your own proxy server, check out https://github.com/ameya98/mp-proxy.
```bash
git clone https://github.com/ameya98/mp-proxy.git
cd mp-proxy
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python mp-proxy/proxy.py
```
Then, update `MP_PROXY_SERVER` in `index.html` to match the proxy server URL (eg. http://localhost:5001).
You can then query the Materials Project with MolView.
