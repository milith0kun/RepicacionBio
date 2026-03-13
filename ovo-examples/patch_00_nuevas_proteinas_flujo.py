# -*- coding: utf-8 -*-
"""
Modifica notebook 00 para:
- Usar proteínas DESCARGADAS (no datos tesis)
- Copiar PDBs a estructura OVO (ovo_home/inputs)
- Crear proyecto "Nuevas proteinas flujo" y generar diseños NUEVOS
- Guardar en BD OVO, filtrar y verificar con módulos OVO (mismo comportamiento que tesis, no replicar datos)
"""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# --- 1. Insertar después de celda de descarga (cell 7): sección 3b Preparar inputs OVO ---
# Buscar celda que tiene "Descargados:" y "df_descarga"
idx_after_download = None
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "urllib.request.urlretrieve" in src and "df_targets" in src and "RCSB" in src:
        idx_after_download = i + 1
        break
if idx_after_download is None:
    for i, c in enumerate(nb["cells"]):
        src = "".join(c.get("source", []))
        if "Descargados:" in src and "PDB_DIR" in src:
            idx_after_download = i + 1
            break

md_3b = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 3b. Preparar proteínas descargadas para OVO (estructura correcta)\n",
        "\n",
        "Copiamos los PDB descargados a **OVO** (`ovo_home/inputs/nuevas_proteinas/`) para que los workflows los usen. Creamos el proyecto **Nuevas proteinas flujo** en la BD OVO. Así los diseños se generan con *tus* proteínas y se guardan en la base de datos con la estructura correcta."
    ]
}

code_3b = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Copiar PDBs a OVO y crear proyecto (comportamiento como tesis; datos nuevos)\n",
        "import shutil\n",
        "OVO_HOME = os.environ.get('OVO_HOME')\n",
        "if not OVO_HOME:\n",
        "    for base in [os.getcwd(), os.path.join(os.getcwd(), '..'), os.path.join(os.getcwd(), '..', '..')]:\n",
        "        for name in ['ovo_home', 'ovo-home']:\n",
        "            p = os.path.join(base, name)\n",
        "            if os.path.isdir(p):\n",
        "                OVO_HOME = os.path.abspath(p)\n",
        "                break\n",
        "        if OVO_HOME:\n",
        "            break\n",
        "OVO_INPUTS = os.path.join(OVO_HOME, 'inputs', 'nuevas_proteinas') if OVO_HOME else None\n",
        "paths_for_ovo = []  # lista de rutas que usaremos en workflows\n",
        "if OVO_HOME and os.path.isdir(OVO_HOME):\n",
        "    os.makedirs(OVO_INPUTS, exist_ok=True)\n",
        "    for r in df_targets.itertuples():\n",
        "        src_pdb = os.path.join(PDB_DIR, f'{r.pdb.upper()}.pdb')\n",
        "        if os.path.isfile(src_pdb):\n",
        "            dst = os.path.join(OVO_INPUTS, f'{r.pdb.upper()}.pdb')\n",
        "            shutil.copy2(src_pdb, dst)\n",
        "            paths_for_ovo.append(dst)\n",
        "    print(f'Copiados {len(paths_for_ovo)} PDB a {OVO_INPUTS}')\n",
        "    from ovo import db\n",
        "    from ovo.core.logic import project_logic\n",
        "    project, round_obj = project_logic.get_or_create_project_round('Nuevas proteinas flujo', 'Round 1')\n",
        "    print('Proyecto OVO:', project.name, 'Round:', round_obj.name)\n",
        "else:\n",
        "    print('OVO_HOME no encontrado. Los PDB quedan solo en', PDB_DIR)\n",
        "    paths_for_ovo = [os.path.join(PDB_DIR, f'{r.pdb.upper()}.pdb') for r in df_targets.itertuples() if os.path.isfile(os.path.join(PDB_DIR, f'{r.pdb.upper()}.pdb'))]\n",
    ]
}

if idx_after_download is not None:
    nb["cells"].insert(idx_after_download, code_3b)
    nb["cells"].insert(idx_after_download, md_3b)
    print("Insertada sección 3b (preparar inputs OVO y proyecto Nuevas proteinas).")

# --- 2. Reemplazar celda 4b (índice 11) para usar proteínas descargadas y proyecto Nuevas proteinas ---
code_4b_new = [
    "# Flujo como la tesis: generar diseños NUEVOS con proteínas descargadas, guardar en BD OVO, filtrar y exportar\n",
    "OVO_HOME_4b = os.environ.get('OVO_HOME') or OVO_HOME if 'OVO_HOME' in dir() else None\n",
    "if not OVO_HOME_4b:\n",
    "    for base in [os.getcwd(), os.path.join(os.getcwd(), '..')]:\n",
    "        for name in ['ovo_home', 'ovo-home']:\n",
    "            p = os.path.join(base, name)\n",
    "            if os.path.isdir(p):\n",
    "                OVO_HOME_4b = os.path.abspath(p)\n",
    "                break\n",
    "        if OVO_HOME_4b:\n",
    "            break\n",
    "tiene_datos = False\n",
    "designs = None\n",
    "jobs = None\n",
    "\n",
    "if OVO_HOME_4b and os.path.isdir(OVO_HOME_4b):\n",
    "    os.environ['OVO_HOME'] = OVO_HOME_4b\n",
    "    print('OVO_HOME:', OVO_HOME_4b)\n",
    "    try:\n",
    "        from ovo import db\n",
    "        from ovo.core.logic import project_logic, design_logic, descriptor_logic\n",
    "        # Usar proyecto de nuevas proteínas (no tesis)\n",
    "        project, round_obj = project_logic.get_or_create_project_round('Nuevas proteinas flujo', 'Round 1')\n",
    "        round_ids = list(db.Round.select_values('id', project_id=project.id))\n",
    "        pool_ids = list(db.Pool.select_values('id', round_id__in=round_ids))\n",
    "        print('Proyecto:', project.name, '| Pools existentes:', len(pool_ids))\n",
    "        # Paso 3: jobs\n",
    "        jobs = design_logic.get_design_jobs_table(project.id)\n",
    "        if jobs is not None and not jobs.empty and ('Pool', 'name') in jobs.columns:\n",
    "            jobs = jobs.sort_values(by=('Pool', 'name'))\n",
    "            display(jobs)\n",
    "                # Paso 4: exportar jobs\n",
        "        if jobs is not None and not jobs.empty:\n",
        "            jobs.to_csv(os.path.join(RESULTS_DIR, 'nuevas_proteinas_jobs.csv'))\n",
    "        print('Jobs exportados a nuevas_proteinas_jobs.csv')\n",
    "        # Paso 5 y 6: diseños + descriptores\n",
    "        designs = db.Design.select_dataframe(pool_id__in=pool_ids)\n",
    "        if len(designs) > 0:\n",
    "            desc_table = descriptor_logic.get_wide_descriptor_table(pool_ids=pool_ids)\n",
    "            designs = designs.join(desc_table)\n",
    "            print('Diseños cargados:', len(designs), '| Columnas:', designs.shape[1])\n",
    "            display(designs.head())\n",
    "            designs.to_csv(os.path.join(RESULTS_DIR, 'nuevas_proteinas_designs.csv.gz'))\n",
    "            print('Paso 7: diseños exportados a nuevas_proteinas_designs.csv.gz')\n",
    "            tiene_datos = True\n",
    "        else:\n",
    "            print('Aún no hay diseños. Ejecuta la celda de generación (4c) con las proteínas descargadas.')\n",
    "    except Exception as e:\n",
    "        print('Error:', e)\n",
    "        import traceback\n",
    "        traceback.print_exc()\n",
    "else:\n",
    "    print('OVO_HOME no definido. Configura OVO para generar y guardar diseños en la BD.')\n",
]

for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "4b. Mismos pasos" in src and "Paso 2" in src:
        # Es el markdown 4b, no tocar
        continue
    if "get_design_jobs_table" in src and "project.id" in src and ("OVO_HOME_4b" in src or "get_or_create_project_round" in src):
        c["source"] = code_4b_new
        print("Reemplazada celda 4b: proyecto Nuevas proteinas, export nuevas_proteinas_*.csv.")
        break

# --- 3. Añadir celda 4c: Generar diseños nuevos con proteínas descargadas (submit workflows) ---
# Insertar después del markdown 4b (cell 10) una celda markdown 4c y una celda code que haga submit por cada target
md_4c = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 4c. Generar diseños nuevos (con proteínas descargadas)\n",
        "\n",
        "Envía workflows OVO usando los **PDB descargados** (rutas en `paths_for_ovo` o PDB_DIR). Crea un pool por proteína. Parámetros compatibles con el flujo de la tesis (RFdiffusion + ProteinMPNN + refolding); los diseños se filtran con los mismos umbrales OVO (PAE, pLDDT, RMSD). Requiere Nextflow/scheduler configurado."
    ]
}

code_4c_lines = [
    "# Generar diseños NUEVOS con proteínas descargadas; guardar en BD OVO (mismo comportamiento que tesis)\n",
    "ovo_home = os.environ.get('OVO_HOME') or (OVO_HOME_4b if 'OVO_HOME_4b' in dir() else None)\n",
    "if not ovo_home or not os.path.isdir(ovo_home):\n",
    "    print('OVO_HOME no definido. Ejecuta antes la sección 3b.')\n",
    "else:\n",
    "    from ovo.core.logic import project_logic, design_logic\n",
    "    from ovo.core.database.models_rfdiffusion import RFdiffusionParams, ProteinMPNNParams, RefoldingParams, RFdiffusionScaffoldDesignWorkflow, RFdiffusionBinderDesignWorkflow\n",
    "    project, round_obj = project_logic.get_or_create_project_round('Nuevas proteinas flujo', 'Round 1')\n",
    "    inputs_dir = os.path.join(ovo_home, 'inputs', 'nuevas_proteinas')\n",
    "    if not os.path.isdir(inputs_dir):\n",
    "        inputs_dir = PDB_DIR\n",
    "    n_submitted = 0\n",
    "    for r in df_targets.itertuples():\n",
    "        pdb_path = os.path.join(inputs_dir, f'{r.pdb.upper()}.pdb')\n",
    "        if not os.path.isfile(pdb_path):\n",
    "            pdb_path = os.path.join(PDB_DIR, f'{r.pdb.upper()}.pdb')\n",
    "        if not os.path.isfile(pdb_path):\n",
    "            continue\n",
    "        uso = str(r.uso).lower()\n",
    "        try:\n",
    "            if 'scaffold' in uso:\n",
    "                w = RFdiffusionScaffoldDesignWorkflow(rfdiffusion_params=RFdiffusionParams(input_pdb_paths=[pdb_path], contigs=['10-80/0'], num_designs=20, timesteps=50), protein_mpnn_params=ProteinMPNNParams(num_sequences=5, sampling_temp=0.1), refolding_params=RefoldingParams(primary_test='af2_model_1_ptm_ft_3rec'))\n",
    "            else:\n",
    "                w = RFdiffusionBinderDesignWorkflow(rfdiffusion_params=RFdiffusionParams(input_pdb_paths=[pdb_path], contigs=['E1-150/0 50-100'], num_designs=20, timesteps=50), protein_mpnn_params=ProteinMPNNParams(num_sequences=5, sampling_temp=0.1), refolding_params=RefoldingParams(primary_test='af2_model_1_multimer_tt_3rec'))\n",
    "            job, pool = design_logic.submit_design_workflow(w, scheduler_key='nextflow', round_id=round_obj.id, pool_name=f'{r.pdb} {r.uso}', pool_description=r.nombre)\n",
    "            print('Enviado:', r.pdb, pool.id)\n",
    "            n_submitted += 1\n",
    "        except Exception as e:\n",
    "            print(r.pdb, 'error:', e)\n",
    "    print('Workflows enviados:', n_submitted, '. Tras completar Nextflow, ejecuta process_results(job) y la celda 4b para cargar diseños.')\n",
]

code_4c = {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": code_4c_lines}

# Insert 4c after 4b markdown (index 10)
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "4b. Mismos pasos" in src and "Paso 2" in src:
        nb["cells"].insert(i + 1, code_4c)
        nb["cells"].insert(i + 1, md_4c)
        print("Insertadas celdas 4c (generar diseños con proteínas descargadas).")
        break

# --- 4. Actualizar sección 5: cargar también nuevas_proteinas_designs.csv.gz ---
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "candidatos_results" in src and "ovo_examples_all.csv.gz" in src:
        lines = c["source"]
        # Añadir en candidatos_results búsqueda de nuevas_proteinas_designs.csv.gz
        new_lines = []
        for j, L in enumerate(lines):
            new_lines.append(L)
            if "ovo_examples_all.csv.gz" in L and "p = os.path.join(d," in lines[j-1] if j > 0 else False:
                pass
            # En el bloque donde se asigna data_dir, también buscar nuevas_proteinas_designs.csv.gz
        # Buscar "p = os.path.join(d, \"ovo_examples_all.csv.gz\")" y añadir antes búsqueda de nuevas_proteinas
        for j, L in enumerate(lines):
            if 'p = os.path.join(d, "ovo_examples_all.csv.gz")' in L or "ovo_examples_all.csv.gz" in L and "os.path.join" in L:
                # Añadir antes: intentar primero nuevas_proteinas_designs.csv.gz en RESULTS_DIR
                if not any("nuevas_proteinas_designs" in x for x in lines):
                    # Insertar al inicio del else: buscar también RESULTS_DIR/nuevas_proteinas_designs.csv.gz
                    pass
                break
        # Más simple: en la lista candidatos_results ya está RESULTS_DIR; el código busca ovo_examples_all. Añadir después de "data_dir = None" un intento de cargar nuevas_proteinas_designs desde RESULTS_DIR
        break

# Añadir al inicio de la lógica de carga: si existe nuevas_proteinas_designs.csv.gz en RESULTS_DIR, usarlo
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "_ya_tiene" in src and "candidatos_results" in src:
        lines = c["source"]
        # Después de "if _ya_tiene:" block, en el else, la primera búsqueda: también comprobar RESULTS_DIR/nuevas_proteinas_designs.csv.gz
        for j, L in enumerate(lines):
            if "data_dir = None" in L and "for d in candidatos_results" in "".join(lines[j:j+5]):
                # Añadir antes del for: comprobar RESULTS_DIR/nuevas_proteinas_designs.csv.gz
                idx = j
                extra = [
                    "    # Prioridad: diseños de nuevas proteínas (este flujo)\n",
                    "    _np = os.path.join(RESULTS_DIR, 'nuevas_proteinas_designs.csv.gz')\n",
                    "    if os.path.isfile(_np):\n",
                    "        data_dir = RESULTS_DIR\n",
                    "        designs_path = _np\n",
                    "        jobs_path = os.path.join(RESULTS_DIR, 'nuevas_proteinas_jobs.csv')\n",
                    "    else:\n",
                ]
                # Indentar el bloque desde "candidatos_results" hasta "if os.path.isfile(designs_path):" (excl.) con 4 espacios más
                rest = lines[idx+1:]
                indented = []
                for line in rest:
                    if "if tiene_datos and designs is not None:" in line and line.strip() and not line.startswith("    " * 2):
                        break
                    indented.append("    " + line if line.strip() else line)
                new_rest = []
                in_block = False
                for k, line in enumerate(rest):
                    if "if tiene_datos and designs is not None:" in line:
                        new_rest = rest[k:]
                        break
                    new_rest.append("    " + line if line.strip() else line)
                c["source"] = lines[:idx+1] + extra + new_rest
                print("Sección 5: prioridad a nuevas_proteinas_designs.csv.gz")
                break
        break

# --- 5. Cambiar designs_path cuando data_dir es RESULTS_DIR y existe nuevas_proteinas ---
# (ya añadido arriba) Falta: al cargar desde CSV, usar designs_path que puede ser nuevas_proteinas_designs
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "designs_path = os.path.join(data_dir" in src and "ovo_examples_all" in src:
        lines = c["source"]
        for j, L in enumerate(lines):
            if "designs_path = os.path.join(data_dir, \"ovo_examples_all.csv.gz\")" in L:
                lines[j] = "    designs_path = os.path.join(data_dir, 'nuevas_proteinas_designs.csv.gz') if os.path.isfile(os.path.join(data_dir or '', 'nuevas_proteinas_designs.csv.gz')) else os.path.join(data_dir, 'ovo_examples_all.csv.gz')\n"
                print("Ajuste designs_path para nuevas_proteinas")
                break
        c["source"] = lines
        break

# --- 6. Reemplazar 5c Verificación vs paper por Verificación con umbrales OVO ---
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "5c" in src and "Verificación vs paper" in src:
        c["source"] = [
            "## 5c. Verificación con umbrales OVO (módulos de OVO)\n",
            "\n",
            "Mismo **comportamiento** que la tesis: aplicar umbrales de calidad (PAE<5, pLDDT>80, Design RMSD<2, etc.) y contar cuántos diseños pasan. No se replican los datos del paper; se analizan los diseños generados en este flujo."
        ]
        print("Actualizado 5c: Verificación con umbrales OVO.")
        break

for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "verify_paper_data" in src or ("paper_esperado" in src and "361" in src):
        # Reemplazar por verificación solo con umbrales
        c["source"] = [
            "# Verificación con módulos OVO: umbrales de calidad (comportamiento como tesis)\n",
            "if tiene_datos and designs is not None and 'accepted' in designs.columns:\n",
            "    print('='*70)\n",
            "    print('VERIFICACIÓN CON UMBRALES OVO (diseños generados en este flujo)')\n",
            "    print('='*70)\n",
            "    total = len(designs)\n",
            "    aceptados = int(designs['accepted'].sum())\n",
            "    print(f'Total diseños: {total} | Aceptados (filtro OVO): {aceptados}')\n",
            "    print('Por pool:')\n",
            "    for pid in designs['pool_id'].unique():\n",
            "        sub = designs[designs['pool_id']==pid]\n",
            "        print(f'  {pid}: {int(sub[\"accepted\"].sum())} / {len(sub)} aceptados')\n",
            "    print('='*70)\n",
            "else:\n",
            "    print('Sin datos de diseños o columna accepted. Genera diseños en 4c y ejecuta 4b.')\n",
        ]
        print("Reemplazada celda verificación: umbrales OVO, sin comparar con paper.")
        break

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook guardado.")
