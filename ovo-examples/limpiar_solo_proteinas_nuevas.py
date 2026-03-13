# -*- coding: utf-8 -*-
"""
Limpia el notebook 00: solo considera proteínas nuevas cargadas.
- 4b: proyecto "Nuevas proteinas flujo", export a nuevas_proteinas_*.csv
- Sección 5: solo carga nuevas_proteinas_designs o OVO "Nuevas proteinas flujo". Sin fallback al paper.
"""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# --- Celda 11: 4b - usar proyecto Nuevas proteinas flujo y exportar nuevas_proteinas_*.csv ---
cell_11_new = '''# Solo proteínas nuevas: proyecto "Nuevas proteinas flujo" (no datos del paper)
OVO_HOME_4b = os.environ.get("OVO_HOME")
if not OVO_HOME_4b or not os.path.isdir(OVO_HOME_4b):
    for base in [os.getcwd(), os.path.join(os.getcwd(), ".."), os.path.join(os.getcwd(), "..", "..")]:
        for name in ["ovo_home", "ovo-home", ".ovo"]:
            p = os.path.join(base, name)
            if os.path.isdir(p):
                OVO_HOME_4b = os.path.abspath(p)
                break
        if OVO_HOME_4b:
            break

tiene_datos = False
designs = None
jobs = None

if OVO_HOME_4b and os.path.isdir(OVO_HOME_4b):
    os.environ["OVO_HOME"] = OVO_HOME_4b
    print("OVO_HOME:", OVO_HOME_4b)
    try:
        from ovo import db
        from ovo.core.logic import project_logic, design_logic, descriptor_logic
        print("Módulos OVO importados.")
        # Proyecto de ESTE flujo (solo proteínas nuevas)
        project, _ = project_logic.get_or_create_project_round("Nuevas proteinas flujo", "Round 1")
        round_ids = list(db.Round.select_values("id", project_id=project.id))
        pool_ids = list(db.Pool.select_values("id", round_id__in=round_ids))
        print(len(pool_ids), "pools (Nuevas proteinas flujo):", pool_ids)
        jobs = design_logic.get_design_jobs_table(project.id)
        if jobs is not None and not jobs.empty and ("Pool", "name") in jobs.columns:
            jobs = jobs.sort_values(by=("Pool", "name"))
        if jobs is not None and not jobs.empty:
            display(jobs)
            jobs.to_csv(os.path.join(RESULTS_DIR, "nuevas_proteinas_jobs.csv"))
            print("Jobs exportados a nuevas_proteinas_jobs.csv")
        designs = db.Design.select_dataframe(pool_id__in=pool_ids) if pool_ids else pd.DataFrame()
        print("Paso 5: diseños cargados:", len(designs))
        if len(designs) > 0:
            display(designs.head())
            desc_table = descriptor_logic.get_wide_descriptor_table(pool_ids=pool_ids)
            designs = designs.join(desc_table)
            print("Paso 6: descriptores unidos. Columnas:", designs.shape[1])
            designs.to_csv(os.path.join(RESULTS_DIR, "nuevas_proteinas_designs.csv.gz"))
            print("Paso 7: tabla exportada a nuevas_proteinas_designs.csv.gz")
            tiene_datos = True
        else:
            print("Sin diseños aún. Genera diseños con tus proteínas (workflows OVO) y vuelve a ejecutar 4b.")
    except Exception as e:
        print("Error ejecutando pasos OVO:", e)
        import traceback
        traceback.print_exc()
else:
    print("OVO_HOME no definido. Solo se usarán CSVs de proteínas nuevas (nuevas_proteinas_*.csv) si existen.")
'''

# --- Celda 12: markdown sección 5 ---
cell_12_new = [
    "## 5. Flujo de análisis (solo proteínas nuevas)\n",
    "\n",
    "Se cargan **únicamente** los diseños de las proteínas que seleccionaste y descargaste en este flujo (`nuevas_proteinas_designs.csv.gz` o proyecto OVO **Nuevas proteinas flujo**). No se usan datos del paper. Si aún no hay diseños, se muestra resumen por proteína en conclusiones.\n",
]

# --- Celda 13: código que solo carga proteínas nuevas ---
cell_13_new = '''# Solo proteínas nuevas: CSV de este flujo o proyecto OVO "Nuevas proteinas flujo"
import os
import pandas as pd
try:
    RESULTS_DIR
except NameError:
    RESULTS_DIR = os.path.join(os.getcwd(), "nuevas_proteinas_flujo", "results")
_np_designs = os.path.join(RESULTS_DIR, "nuevas_proteinas_designs.csv.gz")
_np_jobs = os.path.join(RESULTS_DIR, "nuevas_proteinas_jobs.csv")

tiene_datos = False
designs = None
jobs_path = _np_jobs

try:
    _ya = designs is not None and len(designs) > 0
except NameError:
    _ya = False

if _ya:
    tiene_datos = True
    jobs_path = _np_jobs
    print("Usando datos ya cargados (sección 4b):", len(designs), "diseños")
elif os.path.isfile(_np_designs):
    designs = pd.read_csv(_np_designs, index_col=0, low_memory=False)
    tiene_datos = True
    print("Diseños de proteínas nuevas (nuevas_proteinas_designs):", len(designs), "diseños")
else:
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
    if OVO_HOME and os.path.isdir(OVO_HOME):
        try:
            from ovo import db
            from ovo.core.logic import project_logic, descriptor_logic, design_logic
            proj = project_logic.get_or_create_project("Nuevas proteinas flujo")
            round_ids = list(db.Round.select_values("id", project_id=proj.id))
            pool_ids = list(db.Pool.select_values("id", round_id__in=round_ids))
            designs = db.Design.select_dataframe(pool_id__in=pool_ids) if pool_ids else pd.DataFrame()
            if len(designs) > 0:
                desc = descriptor_logic.get_wide_descriptor_table(pool_ids=pool_ids)
                designs = designs.join(desc)
                tiene_datos = True
                print("Diseños desde OVO (Nuevas proteinas flujo):", len(designs), "diseños")
        except Exception as e:
            print("Error cargando desde OVO:", e)
    if not tiene_datos:
        designs = None
        print("No hay diseños de proteínas nuevas. Ejecuta 4b con OVO_HOME o genera diseños con tus proteínas.")

if tiene_datos and designs is not None and len(designs) > 0:
    n_aceptados = int(designs["accepted"].sum()) if "accepted" in designs.columns else 0
    print("Aceptados:", n_aceptados)
    print(designs.groupby("pool_id").agg({"accepted": "sum"}).rename(columns={"accepted": "aceptados"}))
    jobs = None
    if os.path.isfile(jobs_path):
        try:
            jobs = pd.read_csv(jobs_path, index_col=0, header=[0, 1])
        except Exception:
            pass
    if jobs is None and "OVO_HOME" in dir() and OVO_HOME and os.path.isdir(OVO_HOME):
        try:
            from ovo.core.logic import design_logic, project_logic
            proj = project_logic.get_or_create_project("Nuevas proteinas flujo")
            jobs = design_logic.get_design_jobs_table(proj.id)
            if jobs is not None and ("Pool", "name") in jobs.columns:
                jobs = jobs.sort_values(by=("Pool", "name"))
        except Exception:
            pass
    print("\\n--- PREDICCIONES (solo proteínas nuevas) ---")
    resumen = designs.groupby("pool_id").agg(total=("pool_id", "count"), aceptados=("accepted", "sum")).reset_index()
    resumen["tasa_%"] = (resumen["aceptados"] / resumen["total"] * 100).round(2)
    if jobs is not None and not jobs.empty and ("Workflow", "type") in jobs.columns:
        resumen["workflow"] = resumen["pool_id"].map(lambda p: jobs.loc[p, ("Workflow", "type")] if p in jobs.index else "")
    print(resumen.to_string(index=False))
    print("Total generados:", int(resumen["total"].sum()), "| Aceptados:", int(resumen["aceptados"].sum()))
    for col in ["AF2 PAE", "AF2 pLDDT", "AF2 Design RMSD", "AF2 Native Motif RMSD", "AF2 iPAE", "Rosetta ddG"]:
        if col in designs.columns:
            print(designs.groupby("pool_id")[col].mean().round(4).to_string(), "\\n")
    resumen.to_csv(os.path.join(RESULTS_DIR, "resumen_ovo_predicciones_filtrado.csv"), index=False)
    print("Resumen guardado en results/resumen_ovo_predicciones_filtrado.csv")
'''

def to_source_lines(s):
    return [line + "\n" for line in s.split("\n")[:-1]] + ([s.split("\n")[-1] + "\n"] if s.split("\n")[-1].strip() else [])

nb["cells"][11]["source"] = to_source_lines(cell_11_new)
nb["cells"][12]["source"] = cell_12_new
nb["cells"][13]["source"] = to_source_lines(cell_13_new)

# Intro: solo proteínas nuevas
for i, c in enumerate(nb["cells"]):
    if c.get("cell_type") != "markdown":
        continue
    src = c.get("source", [])
    text = "".join(src) if isinstance(src, list) else src
    if "# Flujo completo: selección" in text and "paper OVO" in text:
        new_src = []
        for line in src:
            if "Basado en el flujo" in line or "paper OVO" in line:
                line = line.replace("Basado en el flujo de los notebooks 01, 02 y 03 del paper OVO.", "Solo se consideran las proteínas nuevas que cargues aquí (no se usan datos del paper).")
            new_src.append(line)
        nb["cells"][i]["source"] = new_src
        print("Intro actualizado.")
        break

# Lista curada: quitar paper
for i, c in enumerate(nb["cells"]):
    if c.get("cell_type") != "markdown":
        continue
    text = "".join(c.get("source", []))
    if "Lista curada" in text and "paper OVO" in text:
        new_src = []
        for line in c.get("source", []):
            new_src.append(line.replace("(paper OVO y guía 2025–2026)", "(criterios terapéuticos y estructurales)"))
        nb["cells"][i]["source"] = new_src
        print("Lista curada actualizada.")
        break

# --- Celdas 14 y 15: reemplazar 5c "vs paper" por verificación solo proteínas nuevas ---
if len(nb["cells"]) > 15:
    md_5c = "".join(nb["cells"][14].get("source", []))
    if "5c" in md_5c and "paper" in md_5c.lower():
        nb["cells"][14]["source"] = [
            "## 5c. Verificación con umbrales OVO (solo proteínas nuevas)\n",
            "\n",
            "Resumen de aceptados por pool según los criterios OVO. No se compara con el paper.\n",
        ]
        nb["cells"][15]["source"] = [
            "# Verificación OVO: solo proteínas nuevas (sin comparar con paper)\n",
            "if tiene_datos and designs is not None and 'accepted' in designs.columns:\n",
            "    total = len(designs)\n",
            "    aceptados = int(designs['accepted'].sum())\n",
            "    print('Total diseños (proteínas nuevas):', total, '| Aceptados (umbrales OVO):', aceptados)\n",
            "    print(designs.groupby('pool_id').agg(total=('accepted', 'count'), aceptados=('accepted', 'sum')))\n",
            "else:\n",
            "    print('Sin datos de diseños de proteínas nuevas para verificar.')\n",
        ]
        print("Sección 5c: solo verificación OVO (sin paper).")

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook guardado. Solo proteínas nuevas.")
