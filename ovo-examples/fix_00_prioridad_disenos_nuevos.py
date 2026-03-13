# -*- coding: utf-8 -*-
"""
Hace que el Colab 00 cargue PRIMERO los diseños nuevos (nuevas_proteinas / proyecto Nuevas proteinas flujo)
y solo si no hay, use los datos del paper. Así verás muchos más diseños cuando generes con 4c.
"""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Nueva lógica de carga para la celda de sección 5
nuevo_source = [
    "# PRIORIDAD 1: Diseños de ESTE flujo (nuevas proteínas), no del paper\n",
    "_np_designs = os.path.join(RESULTS_DIR, 'nuevas_proteinas_designs.csv.gz')\n",
    "_np_jobs = os.path.join(RESULTS_DIR, 'nuevas_proteinas_jobs.csv')\n",
    "if os.path.isfile(_np_designs):\n",
    "    designs = pd.read_csv(_np_designs, index_col=0, low_memory=False)\n",
    "    tiene_datos = True\n",
    "    jobs_path = _np_jobs\n",
    "    data_dir = RESULTS_DIR\n",
    "    print('Diseños de ESTE flujo (nuevas_proteinas_designs):', len(designs), 'diseños')\n",
    "else:\n",
    "    try:\n",
    "        _ya_tiene = designs is not None and len(designs) > 0\n",
    "    except NameError:\n",
    "        _ya_tiene = False\n",
    "    if _ya_tiene:\n",
    "        tiene_datos = True\n",
    "        data_dir = RESULTS_DIR\n",
    "        jobs_path = _np_jobs if os.path.isfile(_np_jobs) else os.path.join(RESULTS_DIR, 'ovo_publication_examples_1_jobs.csv')\n",
    "        print('Usando datos ya cargados en memoria (sección 4b):', len(designs), 'diseños')\n",
    "    else:\n",
    "        # PRIORIDAD 2: Backend OVO proyecto NUEVAS PROTEÍNAS (no el del paper)\n",
    "        OVO_HOME = os.environ.get('OVO_HOME')\n",
    "        if not OVO_HOME or not os.path.isdir(OVO_HOME):\n",
    "            for base in [os.getcwd(), os.path.join(os.getcwd(), '..'), os.path.join(os.getcwd(), '..', '..')]:\n",
    "                for name in ['ovo_home', 'ovo-home', '.ovo']:\n",
    "                    p = os.path.join(base, name)\n",
    "                    if os.path.isdir(p):\n",
    "                        OVO_HOME = os.path.abspath(p)\n",
    "                        break\n",
    "                if OVO_HOME:\n",
    "                    break\n",
    "            if not OVO_HOME:\n",
    "                OVO_HOME = None\n",
    "        designs = None\n",
    "        tiene_datos = False\n",
    "        if OVO_HOME:\n",
    "            try:\n",
    "                from ovo import db\n",
    "                from ovo.core.logic import project_logic, descriptor_logic\n",
    "                proj = project_logic.get_or_create_project('Nuevas proteinas flujo')\n",
    "                round_ids = list(db.Round.select_values('id', project_id=proj.id))\n",
    "                pool_ids = list(db.Pool.select_values('id', round_id__in=round_ids))\n",
    "                designs = db.Design.select_dataframe(pool_id__in=pool_ids)\n",
    "                if len(designs) > 0:\n",
    "                    desc = descriptor_logic.get_wide_descriptor_table(pool_ids=pool_ids)\n",
    "                    designs = designs.join(desc)\n",
    "                    tiene_datos = True\n",
    "                    jobs_path = _np_jobs\n",
    "                    data_dir = RESULTS_DIR\n",
    "                    print('Diseños desde OVO (proyecto Nuevas proteinas flujo):', len(designs), 'diseños')\n",
    "            except Exception as e:\n",
    "                print('OVO proyecto Nuevas proteinas:', e)\n",
    "        if not tiene_datos or designs is None or len(designs) == 0:\n",
    "            candidatos_results = [RESULTS_DIR, os.environ.get('OVO_RESULTS_DIR'), os.path.join(os.getcwd(), 'jupyter_notebooks_example', 'data', 'results'), os.path.join(os.getcwd(), '..', 'jupyter_notebooks_example', 'data', 'results')]\n",
    "            data_dir = None\n",
    "            for d in candidatos_results:\n",
    "                if d and os.path.isdir(d):\n",
    "                    p = os.path.join(d, 'ovo_examples_all.csv.gz')\n",
    "                    if os.path.isfile(p):\n",
    "                        data_dir = os.path.abspath(d)\n",
    "                        break\n",
    "            designs_path = os.path.join(data_dir, 'ovo_examples_all.csv.gz') if data_dir else None\n",
    "            jobs_path = os.path.join(data_dir, 'ovo_publication_examples_1_jobs.csv') if data_dir else os.path.join(RESULTS_DIR, 'ovo_publication_examples_1_jobs.csv')\n",
    "            if designs_path and os.path.isfile(designs_path):\n",
    "                designs = pd.read_csv(designs_path, index_col=0, low_memory=False)\n",
    "                tiene_datos = True\n",
    "                print('Datos de EJEMPLO del paper:', len(designs), 'diseños. Para ver TUS diseños: ejecuta 4c (generar) y 4b (exportar).')\n",
    "            else:\n",
    "                tiene_datos = False\n",
    "                designs = None\n",
    "                print('Sin diseños nuevos ni CSV del paper. Ejecuta 4c (generar con tus proteínas) y 4b (exportar).')\n",
    "\n",
    "if tiene_datos and designs is not None:\n",
    "    n_aceptados = int(designs['accepted'].sum()) if 'accepted' in designs.columns else 0\n",
    "    print('Aceptados (filtro OVO):', n_aceptados)\n",
    "    print(designs.groupby('pool_id').agg({'accepted': 'sum'}).rename(columns={'accepted': 'aceptados'}))\n",
    "    jobs = None\n",
    "    if 'OVO_HOME' in dir() and OVO_HOME and os.path.isdir(OVO_HOME):\n",
    "        try:\n",
    "            from ovo.core.logic import design_logic, project_logic\n",
    "            proj = project_logic.get_or_create_project('Nuevas proteinas flujo')\n",
    "            jobs = design_logic.get_design_jobs_table(proj.id)\n",
    "            if jobs is not None and not jobs.empty and ('Pool', 'name') in jobs.columns:\n",
    "                jobs = jobs.sort_values(by=('Pool', 'name'))\n",
    "        except Exception:\n",
    "            pass\n",
    "    if jobs is None and os.path.isfile(jobs_path):\n",
    "        jobs = pd.read_csv(jobs_path, index_col=0, header=[0, 1])\n",
    "    print('\\n--- PREDICCIONES GENERADAS Y FILTRADO ---')\n",
    "    resumen = designs.groupby('pool_id').agg(total=('pool_id', 'count'), aceptados=('accepted', 'sum')).reset_index()\n",
    "    resumen['tasa_%'] = (resumen['aceptados'] / resumen['total'] * 100).round(2)\n",
    "    if jobs is not None and not jobs.empty and ('Workflow', 'type') in jobs.columns:\n",
    "        resumen['workflow'] = resumen['pool_id'].map(lambda p: jobs.loc[p, ('Workflow', 'type')] if p in jobs.index else '')\n",
    "    print(resumen.to_string(index=False))\n",
    "    print('Total generados:', int(resumen['total'].sum()), '| Aceptados:', int(resumen['aceptados'].sum()))\n",
    "    print('\\n--- DESCRIPTORES (medias por pool) ---')\n",
    "    for col in ['AF2 PAE', 'AF2 pLDDT', 'AF2 Design RMSD', 'AF2 Native Motif RMSD', 'AF2 iPAE', 'Rosetta ddG']:\n",
    "        if col in designs.columns:\n",
    "            print(designs.groupby('pool_id')[col].mean().round(4).to_string(), '\\n')\n",
    "    resumen.to_csv(os.path.join(RESULTS_DIR, 'resumen_ovo_predicciones_filtrado.csv'), index=False)\n",
    "    print('Resumen guardado en results/resumen_ovo_predicciones_filtrado.csv')\n",
]

for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "candidatos_results" in src and "ovo_examples_all.csv.gz" in src and "_ya_tiene" in src:
        c["source"] = nuevo_source
        print("Sección 5: prioridad a diseños nuevos (nuevas_proteinas / proyecto Nuevas proteinas flujo).")
        break

# Aumentar num_designs en 4c para generar más diseños por proteína (50 en lugar de 20)
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "num_designs=20" in src and "RFdiffusionScaffoldDesignWorkflow" in src:
        c["source"] = [L.replace("num_designs=20", "num_designs=50") for L in c["source"]]
        print("4c: num_designs aumentado a 50 por proteína (más diseños).")
        break

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook guardado.")
