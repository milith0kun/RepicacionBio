# -*- coding: utf-8 -*-
"""Corrige visualización 3D, análisis y gráficos en 00_flujo_completo_nuevas_proteinas.ipynb"""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# --- 1. Celda 3D: mejorar py3Dmol (tamaño, fondo, zoom) ---
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "py3Dmol.view" in src and "itertuples" in src and "addModel" in src:
        new_src = """try:
    import py3Dmol
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'py3Dmol', '-q'])
    import py3Dmol

for r in df_targets.itertuples():
    path_pdb = os.path.join(PDB_DIR, f'{r.pdb.upper()}.pdb')
    if not os.path.isfile(path_pdb):
        continue
    with open(path_pdb, 'r', encoding='utf-8', errors='ignore') as f:
        pdb_data = f.read()
    view = py3Dmol.view(width=600, height=450, backgroundColor="white")
    view.addModel(pdb_data, 'pdb')
    view.setStyle({'cartoon': {'colorscheme': 'chain'}})
    view.zoomTo({'margin': 0.1})
    try:
        view.spin(False)
    except Exception:
        pass
    print(f"{r.pdb}: {r.nombre} ({r.aplicacion})")
    display(view)
"""
        c["source"] = [line + "\n" for line in new_src.strip().split("\n")]
        c["source"][-1] = c["source"][-1].rstrip("\n") if c["source"][-1].endswith("\n\n") else c["source"][-1]
        print("Celda 3D actualizada (width=600, height=450, backgroundColor, zoomTo margin).")
        break

# --- 2. Celda análisis: mostrar tabla resumen (display) y corregir encoding ---
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "resumen_ovo_predicciones_filtrado" in src and "PREDICCIONES GENERADAS" in src:
        lines = c["source"]
        new_lines = []
        for j, line in enumerate(lines):
            new_lines.append(line)
            if "print(resumen.to_string(index=False))" in line:
                new_lines.append("    try:\n")
                new_lines.append("        display(resumen)\n")
                new_lines.append("    except NameError:\n")
                new_lines.append("        pass\n")
            # Corregir encoding en prints
            if "dise�os" in line or "secci�n" in line:
                new_lines[-1] = line.replace("dise�os", "diseños").replace("secci�n", "sección")
        c["source"] = new_lines
        print("Celda análisis revisada (display resumen, encoding).")
        break

# --- 3. Celda gráficos: comprobar columnas y mostrar mensajes; cerrar figuras ---
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "flujo_scaffold_pae_rmsd" in src and "Sin datos" in src:
        new_src = """if not tiene_datos or designs is None:
    print('Sin datos de diseños; omitiendo gráficos.')
else:
    from matplotlib import pyplot as plt
    import seaborn as sns

    # Scaffold: PAE vs Design RMSD
    scaffold_pools = ['zuk', 'xeh', 'ogc', 'jov']
    mask = designs['pool_id'].isin(scaffold_pools)
    if mask.any() and 'AF2 PAE' in designs.columns and 'AF2 Design RMSD' in designs.columns:
        df_s = designs[mask].copy()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(df_s, x='AF2 PAE', y='AF2 Design RMSD', hue='pool_id', s=15, alpha=0.7)
        ax.axvline(5, color='red', ls='--', label='PAE<5')
        ax.axhline(2, color='orange', ls='--', label='RMSD<2')
        ax.set_title('Scaffold: PAE vs Design RMSD (Fig 2c)')
        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, 'flujo_scaffold_pae_rmsd.png'), dpi=150, bbox_inches='tight')
        plt.show()
        plt.close()
    else:
        print('Scaffold PAE vs RMSD: no hay datos o faltan columnas AF2 PAE / AF2 Design RMSD.')

    # Binder: histograma ddG
    binder_pools = ['avz', 'mmo', 'bbc']
    mask_b = designs['pool_id'].isin(binder_pools)
    if mask_b.any() and 'Rosetta ddG' in designs.columns:
        df_b = designs[mask_b].dropna(subset=['Rosetta ddG'])
        if len(df_b) > 0:
            fig, ax = plt.subplots(figsize=(8, 4))
            df_b['Rosetta ddG'].hist(ax=ax, bins=30, edgecolor='white')
            ax.axvline(-30, color='red', ls='--', label='ddG<-30')
            ax.set_xlabel('Rosetta ddG')
            ax.set_ylabel('Frecuencia')
            ax.set_title('Binder: distribución ddG (Fig 3)')
            ax.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(RESULTS_DIR, 'flujo_binder_ddg.png'), dpi=150, bbox_inches='tight')
            plt.show()
            plt.close()
        else:
            print('Binder ddG: no hay valores no nulos en Rosetta ddG.')
    else:
        print('Binder ddG: no hay pools binder o falta columna Rosetta ddG.')

    # Scaffold: PAE vs Native Motif RMSD
    if mask.any() and 'AF2 Native Motif RMSD' in designs.columns and 'AF2 PAE' in designs.columns:
        df_s = designs[mask].copy()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(df_s, x='AF2 PAE', y='AF2 Native Motif RMSD', hue='pool_id', s=15, alpha=0.7)
        ax.axvline(5, color='red', ls='--', label='PAE<5')
        ax.axhline(2, color='orange', ls='--', label='Motif RMSD<2')
        ax.set_title('Scaffold: PAE vs Native Motif RMSD (tesis)')
        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, 'flujo_scaffold_pae_motif_rmsd.png'), dpi=150, bbox_inches='tight')
        plt.show()
        plt.close()
    else:
        print('Scaffold PAE vs Native Motif RMSD: no hay datos o falta columna.')

    # Binder: iPAE vs Target-aligned Binder RMSD
    if mask_b.any() and 'AF2 iPAE' in designs.columns and 'AF2 Target-aligned Binder RMSD' in designs.columns:
        df_b2 = designs[mask_b].dropna(subset=['AF2 iPAE', 'AF2 Target-aligned Binder RMSD'])
        if len(df_b2) > 0:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.scatterplot(df_b2, x='AF2 iPAE', y='AF2 Target-aligned Binder RMSD', hue='pool_id', s=20, alpha=0.7)
            ax.axvline(10, color='red', ls='--', label='iPAE<10')
            ax.axhline(2, color='orange', ls='--', label='Binder RMSD<2')
            ax.set_title('Binder: iPAE vs Target-aligned Binder RMSD (tesis)')
            ax.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(RESULTS_DIR, 'flujo_binder_ipae_rmsd.png'), dpi=150, bbox_inches='tight')
            plt.show()
            plt.close()
        else:
            print('Binder iPAE vs RMSD: no hay filas con ambos valores.')
    else:
        print('Binder iPAE vs RMSD: no hay datos o faltan columnas AF2 iPAE / AF2 Target-aligned Binder RMSD.')
"""
        c["source"] = [line + "\n" for line in new_src.strip().split("\n")]
        c["source"][-1] = c["source"][-1].rstrip("\n")
        print("Celda gráficos actualizada (comprobación columnas, plt.close, mensajes).")
        break

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook guardado.")
