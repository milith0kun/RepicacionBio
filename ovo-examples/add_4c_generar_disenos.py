# -*- coding: utf-8 -*-
"""Inserta sección 4c: copiar PDBs a OVO y enviar workflows para crear pools y diseños."""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Encontrar índice de la celda de código 4b (la que tiene "Sin diseños aún. Genera diseños")
idx_4b_end = None
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "Sin diseños aún. Genera diseños con tus proteínas" in src and "get_or_create_project_round" in src:
        idx_4b_end = i + 1  # insertar después de esta celda
        break
if idx_4b_end is None:
    for i, c in enumerate(nb["cells"]):
        src = "".join(c.get("source", []))
        if "Nuevas proteinas flujo" in src and "round_ids = list(db.Round" in src:
            idx_4b_end = i + 1
            break
if idx_4b_end is None:
    idx_4b_end = 12
# Insertar 4c justo después de la celda de código 4b
idx_insert = idx_4b_end

md_4c = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 4c. Generar diseños (enviar workflows con tus proteínas)\n",
        "\n",
        "Copia los PDB descargados a `ovo_home/inputs/nuevas_proteinas/` y envía **un workflow de scaffold por proteína** al proyecto **Nuevas proteinas flujo**. Así se crean pools y, cuando Nextflow termine, tendrás diseños. Requiere **Nextflow** (en Windows usar WSL2). Si falla, verás instrucciones al final."
    ],
}

code_4c = {
    "cell_type": "code",
    "metadata": {},
    "outputs": [],
    "source": [
        "# Copiar PDBs a OVO y enviar un workflow por proteína (crea pools y diseños)\n",
        "import shutil\n",
        "OVO_HOME = os.environ.get(\"OVO_HOME\")\n",
        "if not OVO_HOME or not os.path.isdir(OVO_HOME):\n",
        "    for base in [os.getcwd(), os.path.join(os.getcwd(), \"..\"), os.path.join(os.getcwd(), \"..\", \"..\")]:\n",
        "        for name in [\"ovo_home\", \"ovo-home\", \".ovo\"]:\n",
        "            p = os.path.join(base, name)\n",
        "            if os.path.isdir(p):\n",
        "                OVO_HOME = os.path.abspath(p)\n",
        "                break\n",
        "        if OVO_HOME:\n",
        "            break\n",
        "\n",
        "if not OVO_HOME or not os.path.isdir(OVO_HOME):\n",
        "    print(\"OVO_HOME no encontrado. Ejecuta antes la celda 4b o define OVO_HOME.\")\n",
        "else:\n",
        "    os.environ[\"OVO_HOME\"] = OVO_HOME\n",
        "    inputs_dir = os.path.join(OVO_HOME, \"inputs\", \"nuevas_proteinas\")\n",
        "    os.makedirs(inputs_dir, exist_ok=True)\n",
        "    n_copied = 0\n",
        "    for r in df_targets.itertuples():\n",
        "        pdb_id = getattr(r, \"pdb\", getattr(r, \"id\", str(r)[:4])).upper()\n",
        "        if len(pdb_id) > 4:\n",
        "            pdb_id = pdb_id[:4]\n",
        "        src_pdb = os.path.join(PDB_DIR, f\"{pdb_id}.pdb\")\n",
        "        if os.path.isfile(src_pdb):\n",
        "            dst = os.path.join(inputs_dir, f\"{pdb_id}.pdb\")\n",
        "            shutil.copy2(src_pdb, dst)\n",
        "            n_copied += 1\n",
        "    print(f\"Copiados {n_copied} PDB a {inputs_dir}\")\n",
        "\n",
        "    try:\n",
        "        from ovo.core.logic import project_logic, design_logic\n",
        "        from ovo.core.database.models_rfdiffusion import (\n",
        "            RFdiffusionParams,\n",
        "            ProteinMPNNParams,\n",
        "            RefoldingParams,\n",
        "            RFdiffusionScaffoldDesignWorkflow,\n",
        "        )\n",
        "        project, round_obj = project_logic.get_or_create_project_round(\"Nuevas proteinas flujo\", \"Round 1\")\n",
        "        enviados = 0\n",
        "        for r in df_targets.itertuples():\n",
        "            pdb_id = getattr(r, \"pdb\", getattr(r, \"id\", str(r)[:4])).upper()\n",
        "            if len(pdb_id) > 4:\n",
        "                pdb_id = pdb_id[:4]\n",
        "            pdb_path = os.path.join(inputs_dir, f\"{pdb_id}.pdb\")\n",
        "            if not os.path.isfile(pdb_path):\n",
        "                continue\n",
        "            w = RFdiffusionScaffoldDesignWorkflow(\n",
        "                rfdiffusion_params=RFdiffusionParams(\n",
        "                    input_pdb_paths=[pdb_path],\n",
        "                    contigs=[\"10-80/0\"],\n",
        "                    num_designs=5,\n",
        "                    timesteps=50,\n",
        "                ),\n",
        "                protein_mpnn_params=ProteinMPNNParams(num_sequences=3, sampling_temp=0.1),\n",
        "                refolding_params=RefoldingParams(primary_test=\"af2_model_1_ptm_ft_3rec\"),\n",
        "            )\n",
        "            job, pool = design_logic.submit_design_workflow(\n",
        "                w, scheduler_key=\"nextflow\", round_id=round_obj.id,\n",
        "                pool_name=f\"{pdb_id} scaffold (nuevas proteinas)\",\n",
        "                pool_description=f\"Scaffold para {pdb_id}\",\n",
        "            )\n",
        "            print(f\"Enviado {pdb_id}: job {job.id}, pool {pool.id}\")\n",
        "            enviados += 1\n",
        "        if enviados > 0:\n",
        "            print(f\"\\n{enviados} workflows enviados. Cuando Nextflow termine, re-ejecuta la celda 4b para exportar diseños.\")\n",
        "        else:\n",
        "            print(\"No se envió ningún workflow (revisa que los PDB estén en\", inputs_dir, \").\")\n",
        "    except Exception as e:\n",
        "        print(\"Error al enviar workflows:\", e)\n",
        "        print(\"\\nEn Windows hace falta WSL2 y Nextflow. Alternativa: copia los PDB a\", os.path.join(OVO_HOME, \"inputs\", \"nuevas_proteinas\"), \"y ejecuta los workflows desde Linux/Colab con el proyecto 'Nuevas proteinas flujo'.\")\n",
        "        import traceback\n",
        "        traceback.print_exc()\n",
    ],
}

nb["cells"].insert(idx_insert, code_4c)
nb["cells"].insert(idx_insert, md_4c)
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Sección 4c insertada. Si 4b muestra 0 pools, ejecuta 4c para enviar workflows; luego vuelve a ejecutar 4b.")
