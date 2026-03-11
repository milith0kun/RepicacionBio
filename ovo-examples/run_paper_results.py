"""
OVO Paper Results - Replicación de Figuras
Basado en: 02_stats_and_plots.ipynb del repositorio ovo-examples
Paper: "OVO: de novo protein design ecosystem" (bioRxiv 2025)

Este script carga los datos del paper y genera las figuras/análisis.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para guardar las figuras
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 10

# Directorio base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'jupyter_notebooks_example', 'data')
RESULTS_DIR = os.path.join(DATA_DIR, 'results')
OUTPUT_DIR = os.path.join(BASE_DIR, 'paper_figures_output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("OVO Paper - Replicación de Resultados")
print("=" * 70)

# =====================================================================
# PASO 1: Cargar datos generales
# =====================================================================
print("\n[1/6] Cargando datos generales...")
designs = pd.read_csv(
    os.path.join(RESULTS_DIR, 'ovo_examples_all.csv.gz'),
    index_col=0,
    low_memory=False
)
print(f"  → Datos cargados: {designs.shape[0]} diseños × {designs.shape[1]} columnas")
print(f"  → Pools: {designs['pool_id'].unique().tolist()}")
print(f"  → Diseños aceptados: {designs['accepted'].sum()}")

jobs = pd.read_csv(
    os.path.join(RESULTS_DIR, 'ovo_publication_examples_1_jobs.csv'),
    header=[0, 1],
    index_col=0
)
print(f"  → Jobs del paper: {len(jobs)} pools")

# =====================================================================
# PASO 2: Análisis de Scaffold Design - Oxidoreductase (Figura 2a)
# =====================================================================
print("\n[2/6] Scaffold Design - Oxidoreductase 1A41 (Figura 2a)")
print("-" * 50)

scaffold_results = pd.read_csv(
    os.path.join(RESULTS_DIR, '02_rfdiffusion_motif_scaffolding', 'descriptors.csv'),
    index_col=0
)
print(f"  → Diseños aceptados: {len(scaffold_results)}")

# Pools de scaffolding
ogc_designs = designs[designs['pool_id'] == 'ogc']  # ActiveSite weights
jov_designs = designs[designs['pool_id'] == 'jov']  # Default weights

print(f"  → Pool ogc (ActiveSite weights): {len(ogc_designs)} total, {ogc_designs['accepted'].sum()} aceptados")
print(f"  → Pool jov (Default weights): {len(jov_designs)} total, {jov_designs['accepted'].sum()} aceptados")

# Figura 2a: Scaffold design comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, pool_id, title, color in [
    (axes[0], 'ogc', 'ActiveSite Weights (ogc)\n26 aceptados / 4800', 'tab:blue'),
    (axes[1], 'jov', 'Default Weights (jov)\n0 aceptados / 1200', 'tab:orange')
]:
    pool_data = designs[designs['pool_id'] == pool_id].copy()
    if 'AF2 Design RMSD' in pool_data.columns and 'AF2 PAE' in pool_data.columns:
        accepted = pool_data[pool_data['accepted'] == True]
        rejected = pool_data[pool_data['accepted'] == False]
        
        ax.scatter(rejected['AF2 Design RMSD'], rejected['AF2 PAE'],
                   alpha=0.3, s=10, color='gray', label='Rechazado')
        ax.scatter(accepted['AF2 Design RMSD'], accepted['AF2 PAE'],
                   alpha=0.8, s=30, color=color, label='Aceptado', edgecolors='black', linewidths=0.5)
        
        ax.set_xlabel('AF2 Design RMSD (Å)')
        ax.set_ylabel('AF2 PAE')
        ax.set_title(title)
        ax.legend()

fig.suptitle('Figura 2a: Scaffold Design - Oxidoreductase (PDB 1A41)', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_2a_scaffold_design.png'), bbox_inches='tight')
print(f"  → Guardada: figura_2a_scaffold_design.png")

# =====================================================================
# PASO 3: Análisis de PD1 Interface Scaffolding (Figura 2d)
# =====================================================================
print("\n[3/6] PD1 Interface Scaffolding - PDB 5IUS (Figura 2d)")
print("-" * 50)

pd1_results = pd.read_csv(
    os.path.join(RESULTS_DIR, '03_rfdiffusion_pd1_interface_scaffolding', 'descriptors.csv'),
    index_col=0
)

xeh_designs = designs[designs['pool_id'] == 'xeh']  # Con inpaint_seq
zuk_designs = designs[designs['pool_id'] == 'zuk']  # Sin inpaint

print(f"  → Pool xeh (con inpaint_seq): {len(xeh_designs)} total, {xeh_designs['accepted'].sum()} aceptados")
print(f"  → Pool zuk (sin inpaint): {len(zuk_designs)} total, {zuk_designs['accepted'].sum()} aceptados")

# Figura 2d: PD1 Interface - inpaint vs no-inpaint
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, (pool_id, label, color) in zip(axes, [
    ('xeh', 'Con Inpaint Seq (xeh)\n275 aceptados / 5000', 'tab:blue'),
    ('zuk', 'Sin Inpaint (zuk)\n1 aceptado / 5000', 'tab:orange')
]):
    pool_data = designs[designs['pool_id'] == pool_id].copy()
    if 'AF2 Native Motif RMSD' in pool_data.columns and 'AF2 PAE' in pool_data.columns:
        accepted = pool_data[pool_data['accepted'] == True]
        rejected = pool_data[pool_data['accepted'] == False]
        
        ax.scatter(rejected['AF2 Native Motif RMSD'], rejected['AF2 PAE'],
                   alpha=0.3, s=10, color='gray', label='Rechazado')
        ax.scatter(accepted['AF2 Native Motif RMSD'], accepted['AF2 PAE'],
                   alpha=0.8, s=30, color=color, label='Aceptado', edgecolors='black', linewidths=0.5)
        
        ax.set_xlabel('AF2 Native Motif RMSD (Å)')
        ax.set_ylabel('AF2 PAE')
        ax.set_title(label)
        ax.legend()

fig.suptitle('Figura 2d: PD1 Interface Scaffolding (PDB 5IUS)', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_2d_pd1_interface.png'), bbox_inches='tight')
print(f"  → Guardada: figura_2d_pd1_interface.png")

# =====================================================================
# PASO 4: Análisis de Binder Design - Insulin Receptor (Figura 3)
# =====================================================================
print("\n[4/6] Binder Design - Insulin Receptor 4ZXB (Figura 3)")
print("-" * 50)

binder_results = pd.read_csv(
    os.path.join(RESULTS_DIR, '04_rfdiffusion_binder_design', 'descriptors.csv'),
    index_col=0
)
print(f"  → Diseños aceptados (RFdiffusion binder): {len(binder_results)}")

bindcraft_results = pd.read_csv(
    os.path.join(RESULTS_DIR, '05_bindcraft_binder_design', 'descriptors.csv'),
    index_col=0
)
print(f"  → Diseños aceptados (BindCraft): {len(bindcraft_results)}")

# Pools de binder design
binder_pools = ['avz', 'mmo', 'bbc', 'qki', 'rsj']
for pool_id in binder_pools:
    pool_data = designs[designs['pool_id'] == pool_id]
    accepted = pool_data['accepted'].sum()
    total = len(pool_data)
    print(f"  → Pool {pool_id}: {accepted} aceptados / {total} total ({100*accepted/total if total > 0 else 0:.2f}%)")

# Figura 3: Binder Design - iPAE vs RMSD
fig, ax = plt.subplots(figsize=(10, 8))

binder_pool_ids = ['avz', 'mmo', 'bbc', 'qki']
colors = {'avz': 'tab:blue', 'mmo': 'tab:red', 'bbc': 'tab:green', 'qki': 'tab:purple'}
labels = {
    'avz': 'Default weights (avz)',
    'mmo': 'Beta sheet (mmo)',
    'bbc': 'LigandMPNN (bbc)',
    'qki': 'Diversification (qki)'
}

for pool_id in binder_pool_ids:
    pool_data = designs[designs['pool_id'] == pool_id].copy()
    if 'AF2 iPAE' in pool_data.columns and 'AF2 Target-aligned Binder RMSD' in pool_data.columns:
        rejected = pool_data[pool_data['accepted'] == False]
        accepted = pool_data[pool_data['accepted'] == True]
        
        ax.scatter(
            rejected['AF2 Target-aligned Binder RMSD'],
            rejected['AF2 iPAE'],
            alpha=0.15, s=8, color=colors[pool_id]
        )
        ax.scatter(
            accepted['AF2 Target-aligned Binder RMSD'],
            accepted['AF2 iPAE'],
            alpha=0.9, s=40, color=colors[pool_id],
            label=f'{labels[pool_id]} ({accepted.shape[0]} aceptados)',
            edgecolors='black', linewidths=0.5
        )

ax.set_xlabel('AF2 Target-aligned Binder RMSD (Å)', fontsize=12)
ax.set_ylabel('AF2 iPAE', fontsize=12)
ax.set_title('Figura 3: Binder Design - Insulin Receptor (PDB 4ZXB)', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)

# Añadir umbrales del paper
ax.axhline(y=10, color='red', linestyle='--', alpha=0.5, label='Threshold iPAE ≤ 10')
ax.axvline(x=2, color='red', linestyle='--', alpha=0.5, label='Threshold RMSD ≤ 2')

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_3_binder_design.png'), bbox_inches='tight')
print(f"  → Guardada: figura_3_binder_design.png")

# =====================================================================
# PASO 5: Métricas detalladas de diseños aceptados
# =====================================================================
print("\n[5/6] Métricas de Diseños Aceptados")
print("-" * 50)

# Binder design metrics
if 'AF2 iPAE' in binder_results.columns:
    print(f"\n  BINDER DESIGN (Insulin Receptor):")
    print(f"  {'Métrica':<40} {'Min':>8} {'Mean':>8} {'Max':>8}")
    print(f"  {'-'*40} {'-'*8} {'-'*8} {'-'*8}")
    
    metrics = ['AF2 iPAE', 'AF2 Target-aligned Binder RMSD', 'AF2 Binder pLDDT', 'Rosetta ddG', 'Sequence length']
    for m in metrics:
        if m in binder_results.columns:
            vals = pd.to_numeric(binder_results[m], errors='coerce').dropna()
            if len(vals) > 0:
                print(f"  {m:<40} {vals.min():>8.2f} {vals.mean():>8.2f} {vals.max():>8.2f}")

# Scaffold design metrics
if 'AF2 Design RMSD' in scaffold_results.columns:
    print(f"\n  SCAFFOLD DESIGN (Oxidoreductase):")
    print(f"  {'Métrica':<40} {'Min':>8} {'Mean':>8} {'Max':>8}")
    print(f"  {'-'*40} {'-'*8} {'-'*8} {'-'*8}")
    
    metrics = ['AF2 Design RMSD', 'AF2 Native Motif RMSD', 'AF2 PAE', 'AF2 pLDDT', 'Sequence length']
    for m in metrics:
        if m in scaffold_results.columns:
            vals = pd.to_numeric(scaffold_results[m], errors='coerce').dropna()
            if len(vals) > 0:
                print(f"  {m:<40} {vals.min():>8.2f} {vals.mean():>8.2f} {vals.max():>8.2f}")

# =====================================================================
# PASO 6: Figura de Comparación de Tasas de Éxito
# =====================================================================
print("\n[6/6] Comparación de Tasas de Éxito")
print("-" * 50)

fig, ax = plt.subplots(figsize=(12, 6))

pool_stats = []
pool_labels = {
    'avz': 'Binder\nDefault',
    'mmo': 'Binder\nBeta-sheet',
    'bbc': 'Binder\nLigandMPNN',
    'qki': 'Binder\nDiversification',
    'rsj': 'BindCraft',
    'ogc': 'Scaffold\nActiveSite',
    'jov': 'Scaffold\nDefault',
    'xeh': 'PD1\nInpaint',
    'zuk': 'PD1\nNo-inpaint'
}

pool_colors = {
    'avz': '#4C72B0', 'mmo': '#DD8452', 'bbc': '#55A868', 'qki': '#C44E52',
    'rsj': '#8172B3', 'ogc': '#937860', 'jov': '#DA8BC3', 'xeh': '#8C8C8C', 'zuk': '#CCB974'
}

for pool_id in ['avz', 'mmo', 'bbc', 'qki', 'rsj', 'ogc', 'jov', 'xeh', 'zuk']:
    pool_data = designs[designs['pool_id'] == pool_id]
    total = len(pool_data)
    accepted = pool_data['accepted'].sum()
    rate = 100 * accepted / total if total > 0 else 0
    pool_stats.append({
        'pool': pool_id,
        'label': pool_labels.get(pool_id, pool_id),
        'total': total,
        'accepted': accepted,
        'rate': rate,
        'color': pool_colors.get(pool_id, 'gray')
    })
    print(f"  → {pool_labels.get(pool_id, pool_id).replace(chr(10), ' ')}: {accepted}/{total} ({rate:.2f}%)")

stats_df = pd.DataFrame(pool_stats)
bars = ax.bar(range(len(stats_df)), stats_df['rate'], color=stats_df['color'], edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(stats_df)))
ax.set_xticklabels(stats_df['label'], fontsize=9)
ax.set_ylabel('Tasa de Aceptación (%)', fontsize=12)
ax.set_title('Comparación de Tasas de Éxito por Pool', fontsize=14, fontweight='bold')

# Añadir etiquetas sobre barras
for bar, row in zip(bars, stats_df.itertuples()):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
            f'{row.accepted}/{row.total}',
            ha='center', va='bottom', fontsize=8)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'comparacion_tasas_exito.png'), bbox_inches='tight')
print(f"  → Guardada: comparacion_tasas_exito.png")

# =====================================================================
# Resumen Final
# =====================================================================
print("\n" + "=" * 70)
print("RESUMEN FINAL")
print("=" * 70)
print(f"\nTotal de diseños analizados: {len(designs)}")
print(f"Total de diseños aceptados: {designs['accepted'].sum()}")
print(f"\nFiguras generadas en: {OUTPUT_DIR}")
for f in os.listdir(OUTPUT_DIR):
    fpath = os.path.join(OUTPUT_DIR, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  📊 {f} ({size_kb:.1f} KB)")

print("\n✅ Replicación completada exitosamente!")
print("=" * 70)
