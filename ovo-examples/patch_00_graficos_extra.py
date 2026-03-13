# -*- coding: utf-8 -*-
"""Añade gráficos extra (PAE vs Native Motif RMSD; iPAE vs Binder RMSD) y conclusiones con totales OVO."""
import json

path = "ovo-examples/executed_notebooks/00_flujo_completo_nuevas_proteinas.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Celda de gráficos (section 6): añadir después del bloque binder ddG
graficos_extra = [
    "\n",
    "    # Scaffold: PAE vs Native Motif RMSD (Fig 2c tesis)\n",
    "    if mask.any() and 'AF2 Native Motif RMSD' in designs.columns:\n",
    "        fig, ax = plt.subplots(figsize=(8, 6))\n",
    "        sns.scatterplot(df_s, x='AF2 PAE', y='AF2 Native Motif RMSD', hue='pool_id', s=15, alpha=0.7)\n",
    "        ax.axvline(5, color='red', ls='--', label='PAE<5')\n",
    "        ax.axhline(2, color='orange', ls='--', label='Motif RMSD<2')\n",
    "        ax.set_title('Scaffold: PAE vs Native Motif RMSD (tesis)')\n",
    "        ax.legend()\n",
    "        plt.tight_layout()\n",
    "        plt.savefig(os.path.join(RESULTS_DIR, 'flujo_scaffold_pae_motif_rmsd.png'), dpi=150, bbox_inches='tight')\n",
    "        plt.show()\n",
    "\n",
    "    # Binder: iPAE vs Target-aligned Binder RMSD (Fig 3 tesis)\n",
    "    if mask_b.any() and 'AF2 iPAE' in designs.columns and 'AF2 Target-aligned Binder RMSD' in designs.columns:\n",
    "        df_b2 = designs[mask_b].dropna(subset=['AF2 iPAE', 'AF2 Target-aligned Binder RMSD'])\n",
    "        if len(df_b2) > 0:\n",
    "            fig, ax = plt.subplots(figsize=(8, 6))\n",
    "            sns.scatterplot(df_b2, x='AF2 iPAE', y='AF2 Target-aligned Binder RMSD', hue='pool_id', s=20, alpha=0.7)\n",
    "            ax.axvline(10, color='red', ls='--', label='iPAE<10')\n",
    "            ax.axhline(2, color='orange', ls='--', label='Binder RMSD<2')\n",
    "            ax.set_title('Binder: iPAE vs Target-aligned Binder RMSD (tesis)')\n",
    "            ax.legend()\n",
    "            plt.tight_layout()\n",
    "            plt.savefig(os.path.join(RESULTS_DIR, 'flujo_binder_ipae_rmsd.png'), dpi=150, bbox_inches='tight')\n",
    "            plt.show()\n",
]

for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "flujo_binder_ddg.png" in src and "plt.show()" in src and "tiene_datos" in src:
        lines = c["source"]
        # Insertar antes del cierre del else (antes de la última línea que puede ser plt.show())
        # Buscar la última ocurrencia de plt.show() en el bloque binder y añadir después
        new_lines = lines + graficos_extra
        c["source"] = new_lines
        print("Celda graficos (section 6) actualizada.")
        break
else:
    print("Celda graficos no encontrada.")

# Conclusiones: añadir lectura de resumen OVO si existe
for i, c in enumerate(nb["cells"]):
    src = "".join(c.get("source", []))
    if "CONCLUSIONES" in src and "RECOMENDACIONES" in src and "targets_seleccionados.csv" in src:
        lines = c["source"]
        # Añadir al inicio del bloque que imprime (después del primer print) la carga del resumen
        ins = None
        for j, line in enumerate(lines):
            if "TARGETS SELECCIONADOS" in line and "print" in line:
                ins = j
                break
        if ins is not None:
            extra = [
                "resumen_path = os.path.join(RESULTS_DIR, 'resumen_ovo_predicciones_filtrado.csv')\n",
                "if os.path.isfile(resumen_path):\n",
                "    resumen_ovo = pd.read_csv(resumen_path)\n",
                "    print('0. RESUMEN OVO (predicciones generadas y filtrado)')\n",
                "    print(resumen_ovo.to_string(index=False))\n",
                "    print('Total predicciones generadas:', int(resumen_ovo['total'].sum()))\n",
                "    print('Total aceptadas (filtrado umbrales paper):', int(resumen_ovo['aceptados'].sum()))\n",
                "    print()\n",
            ]
            c["source"] = lines[:ins] + extra + lines[ins:]
            print("Celda conclusiones actualizada con resumen OVO.")
        break
else:
    print("Celda conclusiones no encontrada.")

with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook guardado.")
