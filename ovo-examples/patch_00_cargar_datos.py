# -*- coding: utf-8 -*-
"""Hace que el notebook 00 busque datos en rutas conocidas y detecte OVO_HOME."""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Código nuevo: buscar CSV y OVO_HOME en varias rutas
nuevo_inicio = r'''# Buscar CSV de diseños y jobs en varias rutas (Paso 1 o datos del paper)
candidatos_results = [
    RESULTS_DIR,
    os.environ.get("OVO_RESULTS_DIR"),
    os.path.join(os.getcwd(), "jupyter_notebooks_example", "data", "results"),
    os.path.join(os.getcwd(), "..", "jupyter_notebooks_example", "data", "results"),
    os.path.join(os.getcwd(), "..", "..", "jupyter_notebooks_example", "data", "results"),
    os.path.join(os.getcwd(), "ovo-examples", "jupyter_notebooks_example", "data", "results"),
]
data_dir = None
for d in candidatos_results:
    if d and os.path.isdir(d):
        p = os.path.join(d, "ovo_examples_all.csv.gz")
        if os.path.isfile(p):
            data_dir = os.path.abspath(d)
            break
designs_path = os.path.join(data_dir, "ovo_examples_all.csv.gz") if data_dir else os.path.join(RESULTS_DIR, "ovo_examples_all.csv.gz")
jobs_path = os.path.join(data_dir, "ovo_publication_examples_1_jobs.csv") if data_dir else os.path.join(RESULTS_DIR, "ovo_publication_examples_1_jobs.csv")

# OVO_HOME: variable de entorno o rutas típicas (para backend OVO)
OVO_HOME = os.environ.get("OVO_HOME")
if not OVO_HOME or not os.path.isdir(OVO_HOME):
    for base in [os.getcwd(), os.path.join(os.getcwd(), ".."), os.path.join(os.getcwd(), "..", "..")]:
        for name in ["ovo_home", "ovo-home", ".ovo"]:
            p = os.path.join(base, name)
            if os.path.isdir(p):
                OVO_HOME = os.path.abspath(p)
                break
        if OVO_HOME:
            break
    if not OVO_HOME:
        OVO_HOME = None

if os.path.isfile(designs_path):
'''

# Encontrar la celda y reemplazar desde "designs_path = " hasta "if os.path.isfile(designs_path):"
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "designs_path = os.path.join(RESULTS_DIR, 'ovo_examples_all.csv.gz')" in src and "Sin CSV ni OVO_HOME" in src:
        lines = c["source"]
        # Encontrar índice de la primera línea y de "if os.path.isfile(designs_path):"
        start_idx = None
        end_idx = None
        for j, line in enumerate(lines):
            if "designs_path = os.path.join(RESULTS_DIR" in line and start_idx is None:
                start_idx = j
            if "if os.path.isfile(designs_path):" in line:
                end_idx = j
                break
        if start_idx is not None and end_idx is not None:
            new_lines = [line + "\n" for line in nuevo_inicio.strip().split("\n")]
            new_lines[-1] = new_lines[-1].rstrip("\n") if new_lines[-1].endswith("\n\n") else new_lines[-1]
            c["source"] = lines[:start_idx] + new_lines + lines[end_idx:]
            print("Celda de carga de datos actualizada: búsqueda en rutas conocidas y OVO_HOME.")
        break

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook guardado.")
