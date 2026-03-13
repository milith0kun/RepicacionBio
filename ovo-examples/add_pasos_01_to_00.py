# -*- coding: utf-8 -*-
"""Inserta en notebook 00 los mismos pasos que Notebook 01 (1.2, 1.3, Pasos 2-7)."""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# OVO_HOME puede estar en env o en la celda de sección 5; lo detectamos también aquí para 4b
md_4b = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 4b. Mismos pasos que Notebook 01 (Paso 1): OVO\n",
        "\n",
        "Ejecutamos **los mismos pasos** que el Notebook 01: generación de diseños (opcional), importar módulos OVO, **Paso 2** (proyecto y pools), **Paso 3** (tabla jobs), **Paso 4** (exportar jobs CSV), **Paso 5** (cargar diseños), **Paso 6** (descriptores y unir), **Paso 7** (exportar tabla completa a CSV). Si `OVO_HOME` está definido se ejecutan todos; si no, la sección 5 cargará los CSVs si existen."
    ]
}

code_4b = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Detectar OVO_HOME (env o rutas típicas) para ejecutar los mismos pasos que Notebook 01\n",
        "OVO_HOME_4b = os.environ.get(\"OVO_HOME\")\n",
        "if not OVO_HOME_4b or not os.path.isdir(OVO_HOME_4b):\n",
        "    for base in [os.getcwd(), os.path.join(os.getcwd(), \"..\"), os.path.join(os.getcwd(), \"..\", \"..\")]:\n",
        "        for name in [\"ovo_home\", \"ovo-home\", \".ovo\"]:\n",
        "            p = os.path.join(base, name)\n",
        "            if os.path.isdir(p):\n",
        "                OVO_HOME_4b = os.path.abspath(p)\n",
        "                break\n",
        "        if OVO_HOME_4b:\n",
        "            break\n",
        "\n",
        "tiene_datos = False\n",
        "designs = None\n",
        "jobs = None\n",
        "\n",
        "if OVO_HOME_4b and os.path.isdir(OVO_HOME_4b):\n",
        "    os.environ[\"OVO_HOME\"] = OVO_HOME_4b\n",
        "    print(\"OVO_HOME:\", OVO_HOME_4b)\n",
        "    try:\n",
        "        # 1.3 Importar módulos OVO (como 01)\n",
        "        from ovo import db, design_logic, descriptor_logic\n",
        "        print(\"Módulos OVO importados.\")\n",
        "        # Paso 2: Cargar proyecto y listar pools\n",
        "        project = db.Project.get(name='OVO Publication Examples 1')\n",
        "        round_ids = list(db.Round.select_values(\"id\", project_id=project.id))\n",
        "        pool_ids = list(db.Pool.select_values(\"id\", round_id__in=round_ids))\n",
        "        print(len(pool_ids), 'pools', pool_ids)\n",
        "        # Paso 3: Tabla de jobs\n",
        "        jobs = design_logic.get_design_jobs_table(project.id)\n",
        "        if ('Pool', 'name') in jobs.columns:\n",
        "            jobs = jobs.sort_values(by=('Pool', 'name'))\n",
        "        display(jobs)\n",
        "        # Paso 4: Exportar jobs a CSV\n",
        "        jobs.to_csv(os.path.join(RESULTS_DIR, 'ovo_publication_examples_1_jobs.csv'))\n",
        "        print(\"Paso 4: jobs exportados a CSV.\")\n",
        "        # Paso 5: Cargar diseños\n",
        "        designs = db.Design.select_dataframe(pool_id__in=pool_ids)\n",
        "        print(\"Paso 5: diseños cargados:\", len(designs))\n",
        "        display(designs.head())\n",
        "        # Paso 6: Descriptores y unir\n",
        "        desc_table = descriptor_logic.get_wide_descriptor_table(pool_ids=pool_ids)\n",
        "        designs = designs.join(desc_table)\n",
        "        print(\"Paso 6: descriptores unidos. Columnas:\", designs.shape[1])\n",
        "        # Paso 7: Exportar tabla completa\n",
        "        designs.to_csv(os.path.join(RESULTS_DIR, 'ovo_examples_all.csv.gz'))\n",
        "        print(\"Paso 7: tabla exportada a ovo_examples_all.csv.gz\")\n",
        "        tiene_datos = True\n",
        "    except Exception as e:\n",
        "        print(\"Error ejecutando pasos OVO (01):\", e)\n",
        "        import traceback\n",
        "        traceback.print_exc()\n",
        "else:\n",
        "    print(\"OVO_HOME no definido o no encontrado. Se usarán CSVs en la sección 5 si existen.\")\n",
    ]
}

# Insertar después de la celda 9 (última de sección 4), antes de "## 5. Flujo"
idx = 10  # section 5 starts at 10
nb["cells"].insert(idx, code_4b)
nb["cells"].insert(idx, md_4b)
print("Insertadas celdas 4b (mismos pasos que 01) en índice", idx)

# En sección 5: si ya hay designs de 4b, no recargar
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "# Buscar CSV de diseños y jobs en varias rutas" in src and "candidatos_results" in src:
        lines = c["source"]
        # Añadir al inicio comprobación de datos de 4b
        head = [
            "# Si la sección 4b ya ejecutó los pasos del 01, usar esos designs\n",
            "try:\n",
            "    _ya_tiene = designs is not None and len(designs) > 0\n",
            "except NameError:\n",
            "    _ya_tiene = False\n",
            "if _ya_tiene:\n",
            "    tiene_datos = True\n",
            "    data_dir = RESULTS_DIR\n",
            "    jobs_path = os.path.join(RESULTS_DIR, 'ovo_publication_examples_1_jobs.csv')\n",
            "    print('Usando datos de sección 4b (Pasos Notebook 01):', len(designs), 'diseños')\n",
            "else:\n",
        ]
        # Indentar todo el bloque actual (hasta "if tiene_datos and designs") como contenido del else
        indented = []
        for L in lines:
            if L.strip():
                indented.append("    " + L)
            else:
                indented.append(L)
        c["source"] = head + indented
        print("Sección 5: prioridad a datos de 4b.")
        break

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook guardado.")
