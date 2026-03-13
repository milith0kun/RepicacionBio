# -*- coding: utf-8 -*-
"""Cambia la celda 4b para usar proyecto 'Nuevas proteinas flujo' y exportar nuevas_proteinas_*.csv"""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

old_2 = "        # Paso 2: Cargar proyecto y listar pools\n"
old_project = "        project = db.Project.get(name='OVO Publication Examples 1')\n"
old_rounds = "        round_ids = list(db.Round.select_values(\"id\", project_id=project.id))\n"

new_2 = "        # Paso 2: Proyecto de ESTE flujo (Nuevas proteinas), no el del paper\n"
new_project = "        from ovo.core.logic import project_logic\n"
new_project2 = "        project, _ = project_logic.get_or_create_project_round('Nuevas proteinas flujo', 'Round 1')\n"
new_rounds = "        round_ids = list(db.Round.select_values(\"id\", project_id=project.id))\n"

for i, c in enumerate(nb["cells"]):
    if c.get("cell_type") != "code":
        continue
    src = c.get("source", [])
    if not isinstance(src, list):
        src = [src]
    text = "".join(src)
    if "OVO_HOME_4b" not in text or "db.Project.get(name='OVO Publication Examples 1')" not in text:
        continue
    new_src = []
    for line in src:
        s = line
        if old_2 in s and "Paso 2" in s:
            s = s.replace(old_2, new_2)
            s = s.replace(old_project, new_project + new_project2)
        if "jobs.to_csv(os.path.join(RESULTS_DIR, 'ovo_publication_examples_1_jobs.csv'))" in s:
            s = s.replace("'ovo_publication_examples_1_jobs.csv'", "'nuevas_proteinas_jobs.csv'")
        if "print(\"Paso 4: jobs exportados a CSV.\")" in s:
            s = s.replace("Paso 4: jobs exportados a CSV.", "Paso 4: jobs exportados a nuevas_proteinas_jobs.csv.")
        if "designs.to_csv(os.path.join(RESULTS_DIR, 'ovo_examples_all.csv.gz'))" in s:
            s = s.replace("'ovo_examples_all.csv.gz'", "'nuevas_proteinas_designs.csv.gz'")
        if "print(\"Paso 7: tabla exportada a ovo_examples_all.csv.gz\")" in s:
            s = s.replace("ovo_examples_all.csv.gz", "nuevas_proteinas_designs.csv.gz")
        if "print(len(pool_ids), 'pools', pool_ids)" in s:
            s = s.replace("'pools', pool_ids", "'pools (Nuevas proteinas flujo):', pool_ids")
        new_src.append(s)
    nb["cells"][i]["source"] = new_src
    print("Celda 4b actualizada: proyecto 'Nuevas proteinas flujo', export a nuevas_proteinas_*.csv")
    break

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Guardado.")
