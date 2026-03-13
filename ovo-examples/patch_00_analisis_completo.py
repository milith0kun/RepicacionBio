# -*- coding: utf-8 -*-
"""Añade al notebook 00 el análisis completo OVO (predicciones generadas/filtradas, verificación, descriptores)."""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Encontrar celda que tiene designs_path, tiene_datos, groupby aceptados
analisis_extra = [
    "    # Analisis completo OVO: cuantas predicciones, cuantas filtradas (como tesis)\n",
    "    jobs_path = os.path.join(RESULTS_DIR, 'ovo_publication_examples_1_jobs.csv')\n",
    "    jobs = None\n",
    "    if OVO_HOME and os.path.isdir(OVO_HOME):\n",
    "        try:\n",
    "            from ovo.core.logic import design_logic, project_logic\n",
    "            proj = project_logic.get_or_create_project('OVO Publication Examples 1')\n",
    "            jobs = design_logic.get_design_jobs_table(proj.id)\n",
    "            if ('Pool', 'name') in jobs.columns: jobs = jobs.sort_values(by=('Pool', 'name'))\n",
    "        except Exception: pass\n",
    "    if jobs is None and os.path.isfile(jobs_path):\n",
    "        jobs = pd.read_csv(jobs_path, index_col=0, header=[0, 1])\n",
    "    print('\\n--- PREDICCIONES GENERADAS Y FILTRADO (OVO, como tesis) ---')\n",
    "    resumen = designs.groupby('pool_id').agg(total=('pool_id','count'), aceptados=('accepted','sum')).reset_index()\n",
    "    resumen['tasa_%'] = (resumen['aceptados']/resumen['total']*100).round(2)\n",
    "    if jobs is not None and not jobs.empty and ('Workflow','type') in jobs.columns:\n",
    "        resumen['workflow'] = resumen['pool_id'].map(lambda p: jobs.loc[p,('Workflow','type')] if p in jobs.index else '')\n",
    "    print(resumen.to_string(index=False))\n",
    "    print('Total generados:', int(resumen['total'].sum()), '| Aceptados (filtrado):', int(resumen['aceptados'].sum()))\n",
    "    print('\\n--- VERIFICACION OVO (umbrales paper) ---')\n",
    "    if jobs is not None:\n",
    "        for pid in resumen['pool_id']:\n",
    "            if pid in jobs.index and ('Pool','name') in jobs.columns:\n",
    "                nom = str(jobs.loc[pid,('Pool','name')])[:60]\n",
    "                print(pid, nom)\n",
    "    print('\\n--- DESCRIPTORES (medias por pool, ProteinQC-style) ---')\n",
    "    for col in ['AF2 PAE','AF2 pLDDT','AF2 Design RMSD','AF2 Native Motif RMSD','AF2 iPAE','Rosetta ddG']:\n",
    "        if col in designs.columns:\n",
    "            print(designs.groupby('pool_id')[col].mean().round(4).to_string(), '\\n')\n",
    "    resumen.to_csv(os.path.join(RESULTS_DIR, 'resumen_ovo_predicciones_filtrado.csv'), index=False)\n",
    "    print('Resumen guardado en results/resumen_ovo_predicciones_filtrado.csv')\n",
]

for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "designs_path = os.path.join(RESULTS_DIR" in src and "print(designs.groupby('pool_id').agg({'accepted': 'sum'})" in src:
        # Añadir después del print(groupby) el bloque de análisis completo
        lines = c["source"]
        new_lines = lines + analisis_extra
        c["source"] = new_lines
        print("Celda", i, "actualizada con analisis completo OVO.")
        break
else:
    print("No se encontro la celda.")

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook guardado.")
