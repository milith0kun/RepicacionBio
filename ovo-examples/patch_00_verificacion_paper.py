# -*- coding: utf-8 -*-
"""Inserta celda de verificación vs paper (como verify_paper_data) en notebook 00."""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

markdown_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 5c. Verificación vs paper (módulo de verificación OVO)\n",
        "\n",
        "Comparación sistemática con los valores del paper (paper_extracted.txt): total aceptados 361, conteos por pool (ogc, jov, xeh, zuk, avz, mmo, bbc, qki, rsj). Si tienes los CSVs del Paso 1, esta celda replica la lógica de `verify_paper_data.py`."
    ]
}

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Verificación OVO vs paper (como verify_paper_data)\n",
        "if tiene_datos and designs is not None and 'accepted' in designs.columns:\n",
        "    print('='*70)\n",
        "    print('VERIFICACION SISTEMATICA: DATOS OVO vs PAPER')\n",
        "    print('='*70)\n",
        "    total_aceptados = int(designs['accepted'].sum())\n",
        "    total_diseños = len(designs)\n",
        "    print(f'Total diseños: {total_diseños} | Aceptados: {total_aceptados} (paper: 361 para pools del paper)')\n",
        "    paper_pools = ['ogc','jov','xeh','zuk','avz','mmo','bbc','qki','rsj']\n",
        "    paper_esperado = {'ogc': (4800, 13), 'jov': (1200, 0), 'xeh': (5000, 275), 'zuk': (5000, 1),\n",
        "                     'avz': (4000, 5), 'mmo': (4000, 1), 'bbc': (4000, 3), 'qki': (450, 37), 'rsj': (108, 13)}\n",
        "    print('\\nPor pool (total generados, aceptados) vs paper:')\n",
        "    for pid in paper_pools:\n",
        "        sub = designs[designs['pool_id'] == pid]\n",
        "        if len(sub) == 0: continue\n",
        "        tot, acc = len(sub), int(sub['accepted'].sum())\n",
        "        exp_tot, exp_acc = paper_esperado.get(pid, (None, None))\n",
        "        ok = (exp_tot is None) or (tot == exp_tot and acc == exp_acc)\n",
        "        sym = '[OK]' if ok else '[!]'\n",
        "        print(f'  {sym} {pid}: total={tot}, aceptados={acc} (paper: total={exp_tot}, aceptados={exp_acc})')\n",
        "    print('\\n' + '='*70)\n",
        "else:\n",
        "    print('Sin datos OVO o sin columna accepted; ejecuta Paso 1 y carga diseños.')"
    ]
}

# Encontrar el índice de la celda "## 6. Gráficos" para insertar antes
idx_insert = None
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "## 6. Gráficos" in src and "como Notebook 02" in src:
        idx_insert = i
        break

if idx_insert is not None:
    nb["cells"].insert(idx_insert, code_cell)
    nb["cells"].insert(idx_insert, markdown_cell)
    print("Celdas de verificacion vs paper insertadas antes de seccion 6.")
else:
    print("No se encontro seccion 6.")

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook guardado.")
