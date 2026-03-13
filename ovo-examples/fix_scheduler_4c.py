# Fix 4c: use local_conda instead of nextflow
import json

path = "executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    src = cell.get("source", [])
    if not isinstance(src, list):
        src = [src]
    for i, line in enumerate(src):
        if "scheduler_key=" in line and "nextflow" in line:
            src[i] = line.replace('"nextflow"', '"local_conda"')
        if "Cuando Nextflow termine" in line:
            src[i] = line.replace("Cuando Nextflow termine", "Cuando los workflows terminen")
    cell["source"] = src

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Patched: scheduler_key='nextflow' -> 'local_conda' in 4c")
