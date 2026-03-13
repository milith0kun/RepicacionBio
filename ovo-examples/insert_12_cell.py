# -*- coding: utf-8 -*-
import json
with open("ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

code_12_lines = [
    "# Mismo codigo que Notebook 01 seccion 1.2 (generacion de disenos)\n",
    "ovo_home = os.environ.get('OVO_HOME')\n",
    "if not ovo_home:\n",
    "    print('OVO_HOME no definido. Salta esta celda o define OVO_HOME.')\n",
    "else:\n",
    "    from ovo.core.logic import project_logic, design_logic\n",
    "    from ovo.core.database.models_rfdiffusion import (RFdiffusionParams, ProteinMPNNParams, RefoldingParams, RFdiffusionScaffoldDesignWorkflow, RFdiffusionBinderDesignWorkflow)\n",
    "    from ovo import db\n",
    "    project, round_obj = project_logic.get_or_create_project_round('OVO Publication Examples 1', 'Round 1')\n",
    "    round_ids = list(db.Round.select_values('id', project_id=project.id))\n",
    "    pool_ids = list(db.Pool.select_values('id', round_id__in=round_ids))\n",
    "    designs_df = db.Design.select_dataframe(pool_id__in=pool_ids)\n",
    "    accepted = designs_df.get('accepted')\n",
    "    n_accepted = int(accepted.sum()) if accepted is not None and accepted.dtype == bool else 0\n",
    "    n_total = len(designs_df)\n",
    "    print('Disenos en el proyecto:', n_total, 'total,', n_accepted, 'aceptados (tesis: 361).')\n",
    "    if n_accepted >= 361:\n",
    "        print('Ya hay 361+ aceptados. No se envian nuevos workflows.')\n",
    "    else:\n",
    "        try:\n",
    "            pdb_1a4i = os.path.join(ovo_home, 'inputs/oxidoreductase/1A4I.pdb')\n",
    "            if os.path.isfile(pdb_1a4i):\n",
    "                w1 = RFdiffusionScaffoldDesignWorkflow(rfdiffusion_params=RFdiffusionParams(input_pdb_paths=[pdb_1a4i], contigs=['10-100/A56-56/10-100/A100-100/10-100/A125-125/2-2/0/0'], num_designs=50, timesteps=50), protein_mpnn_params=ProteinMPNNParams(num_sequences=5, sampling_temp=0.1), refolding_params=RefoldingParams(primary_test='af2_model_1_ptm_ft_3rec'))\n",
    "                job1, pool1 = design_logic.submit_design_workflow(w1, scheduler_key='nextflow', round_id=round_obj.id, pool_name='1A4I scaffold (paper)', pool_description='Scaffold 56,100,125')\n",
    "                print('Enviado 1A4I:', job1.id)\n",
    "            pdb_5ius = os.path.join(ovo_home, 'inputs/pd1/5IUS.pdb')\n",
    "            if os.path.isfile(pdb_5ius):\n",
    "                w2 = RFdiffusionScaffoldDesignWorkflow(rfdiffusion_params=RFdiffusionParams(input_pdb_paths=[pdb_5ius], contigs=['0-30/A119-140/15-40/A63-82/0-30/0'], num_designs=200, timesteps=50), protein_mpnn_params=ProteinMPNNParams(num_sequences=5, sampling_temp=0.1), refolding_params=RefoldingParams(primary_test='af2_model_1_ptm_ft_3rec'))\n",
    "                job2, pool2 = design_logic.submit_design_workflow(w2, scheduler_key='nextflow', round_id=round_obj.id, pool_name='5IUS scaffold PD-1 (paper)', pool_description='Segmentos 63-82, 119-140')\n",
    "                print('Enviado 5IUS:', job2.id)\n",
    "            pdb_4zxb = os.path.join(ovo_home, 'inputs/insulin/4ZXB.pdb')\n",
    "            if os.path.isfile(pdb_4zxb):\n",
    "                w3 = RFdiffusionBinderDesignWorkflow(rfdiffusion_params=RFdiffusionParams(input_pdb_paths=[pdb_4zxb], contigs=['E6-155/0 50-100'], hotspots='E64,E88,E96', num_designs=50, timesteps=50), protein_mpnn_params=ProteinMPNNParams(num_sequences=5, sampling_temp=0.1), refolding_params=RefoldingParams(primary_test='af2_model_1_multimer_tt_3rec'))\n",
    "                job3, pool3 = design_logic.submit_design_workflow(w3, scheduler_key='nextflow', round_id=round_obj.id, pool_name='4ZXB binder (paper)', pool_description='Hotspots E64,E88,E96')\n",
    "                print('Enviado 4ZXB:', job3.id)\n",
    "            print('Workflows enviados. Procesa con design_logic.process_results(job).')\n",
    "        except Exception as e:\n",
    "            print('Error enviando workflows:', e)\n",
]

for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "4b. Mismos pasos que Notebook 01" in src and "Paso 2" in src:
        nb["cells"].insert(i + 1, {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": code_12_lines})
        nb["cells"].insert(i + 1, {"cell_type": "markdown", "metadata": {}, "source": [
            "### 1.2 Generacion de disenos (opcional)\n",
            "\n",
            "Igual que Notebook 01: enviar workflows con **design_logic.submit_design_workflow**. Si ya tienes los 361 disenos en la BD, puedes saltar esta celda.\n"
        ]})
        print("Insertadas celdas 1.2")
        break
with open("ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
