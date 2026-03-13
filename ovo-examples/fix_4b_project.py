# -*- coding: utf-8 -*-
import json
path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)
old = "        project = db.Project.get(name='OVO Publication Examples 1')\n"
new1 = "        from ovo.core.logic import project_logic\n"
new2 = "        project, _ = project_logic.get_or_create_project_round('Nuevas proteinas flujo', 'Round 1')\n"
for i, c in enumerate(nb["cells"]):
    if c.get("cell_type") != "code":
        continue
    src = c.get("source", [])
    if not isinstance(src, list):
        src = [src]
    for j, line in enumerate(src):
        if old in line or "OVO Publication Examples 1" in line and "Project.get" in line:
            src[j] = new1
            src.insert(j + 1, new2)
            print("Replaced project line in cell", i)
            break
    else:
        continue
    break
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Done")
