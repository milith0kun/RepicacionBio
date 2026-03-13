# -*- coding: utf-8 -*-
"""
Verificacion de datos OVO vs Paper
Usa el CSV completo (ovo_examples_all.csv.gz) y la tabla de jobs.
Ruta: OVO_RESULTS_DIR o jupyter_notebooks_example/data/results.
"""
import pandas as pd
import os

def _find_results_dir():
    candidates = [
        os.environ.get("OVO_RESULTS_DIR"),
        os.path.join(os.getcwd(), "jupyter_notebooks_example", "data", "results"),
        os.path.join(os.getcwd(), "..", "jupyter_notebooks_example", "data", "results"),
        os.path.abspath(os.path.join(os.path.dirname(__file__) or ".", "jupyter_notebooks_example", "data", "results")),
    ]
    for p in candidates:
        if p and os.path.isdir(p):
            return os.path.abspath(p)
    return os.path.abspath(os.path.join(os.getcwd(), "jupyter_notebooks_example", "data", "results"))

data_dir = _find_results_dir()
designs = pd.read_csv(os.path.join(data_dir, "ovo_examples_all.csv.gz"), index_col=0)
jobs = pd.read_csv(os.path.join(data_dir, "ovo_publication_examples_1_jobs.csv"), index_col=0, header=[0, 1])

print("RESULTS_DIR:", data_dir)
print('=' * 70)
print('VERIFICACION SISTEMATICA: DATOS OVO vs PAPER')
print('Fuente: ovo_examples_all.csv.gz (CSV completo con todos los disenos)')
print('=' * 70)

# Verificar estructura del CSV
print(f'\nCSV tiene {len(designs)} filas y {len(designs.columns)} columnas')
print(f'Pools unicos: {sorted(designs["pool_id"].unique())}')
print(f'Columnas disponibles: {list(designs.columns[:20])}...')

# Check if 'accepted' column exists and its values
if 'accepted' in designs.columns:
    print(f'Columna "accepted": Tipos={designs["accepted"].dtype}, Valores unicos={designs["accepted"].unique()}')
else:
    print('ADVERTENCIA: No hay columna "accepted" en el CSV')

results = []

def check(label, paper_val, data_val):
    match = paper_val == data_val
    symbol = "+" if match else "!"
    status = "OK" if match else "DIFERENTE"
    print(f'   [{symbol}] {label}: Paper={paper_val}, Datos={data_val} -> {status}')
    results.append(match)
    return match

# ============================================================
print('\n--- INFO DE POOLS ---')
for pid in sorted(designs['pool_id'].unique()):
    pool = designs[designs['pool_id'] == pid]
    total = len(pool)
    accepted = int(pool['accepted'].sum()) if 'accepted' in pool.columns else 'N/A'
    name = jobs.loc[pid, ('Pool', 'name')] if pid in jobs.index else 'desconocido'
    wf_type = jobs.loc[pid, ('Workflow', 'type')] if pid in jobs.index else 'N/A'
    print(f'  {pid}: "{name}" [{wf_type}]')
    print(f'       Total={total}, Aceptados={accepted}')

# ============================================================
# 1. OXIDOREDUCTASE (ogc, jov)
# ============================================================
print('\n' + '=' * 70)
print('1. OXIDOREDUCTASE MOTIF SCAFFOLDING (Figura 2, Methods)')
print('   PDB: 1A4I, Chain A, Fixed residues: 56, 100, 125')
print('=' * 70)

ogc = designs[designs['pool_id'] == 'ogc']
ogc_total = len(ogc)
ogc_accepted = int(ogc['accepted'].sum())
print(f'\n  Pool ogc (ActiveSite weights):')
print(f'    Paper: 100 backbones x 6 permutations x 8 seqs = 4800 total')
print(f'    Paper: "resulting in 13 accepted designs"')
print(f'    Paper Thresholds: PAE<5, pLDDT>80, Design RMSD<2, Native Motif RMSD<1.5')
check('ogc total', 4800, ogc_total)
check('ogc accepted', 13, ogc_accepted)
if ogc_accepted != 13:
    print(f'    [NOTA] Paper Methods = 13, pero datos muestran {ogc_accepted}.')
    print(f'    Paper dice "361 accepted" total. Verificamos: ')
    s = 0
    for p in ['ogc','jov','xeh','zuk','avz','mmo','bbc','qki','rsj']:
        a = int(designs[designs['pool_id']==p]['accepted'].sum()) if p in designs['pool_id'].values else 0
        s += a
    print(f'    Suma real de aceptados: {s}')
    if s == 361:
        print(f'    -> La suma de aceptados DA 361, lo que requiere ogc={ogc_accepted}')
        print(f'    -> Paper Methods probablemente tiene error tipografico')

jov = designs[designs['pool_id'] == 'jov']
jov_total = len(jov)
jov_accepted = int(jov['accepted'].sum())
print(f'\n  Pool jov (Default weights):')
print(f'    Paper: 100 backbones x 6 permutations x 2 seqs = 1200 total')
print(f'    Paper: "Running the same workflow with default weights yielded no accepted designs"')
check('jov total', 1200, jov_total)
check('jov accepted', 0, jov_accepted)

# ============================================================
# 2. PD-1 INTERFACE (xeh, zuk)
# ============================================================
print('\n' + '=' * 70)
print('2. PD-1 INTERFACE SCAFFOLDING (Figura 2d-e, Methods)')
print('   PDB: 5IUS, Chain A, segments 119-140 and 63-82')
print('=' * 70)

xeh = designs[designs['pool_id'] == 'xeh']
xeh_total = len(xeh)
xeh_accepted = int(xeh['accepted'].sum())
xeh_rate = xeh_accepted / xeh_total * 100 if xeh_total > 0 else 0
print(f'\n  Pool xeh (With sequence inpainting):')
print(f'    Paper: 1000 backbones x 5 seqs = 5000 total, 275 accepted')
check('xeh total', 5000, xeh_total)
check('xeh accepted', 275, xeh_accepted)
print(f'    Success rate: {xeh_rate:.2f}% (paper: 5.50%)')

zuk = designs[designs['pool_id'] == 'zuk']
zuk_total = len(zuk)
zuk_accepted = int(zuk['accepted'].sum())
print(f'\n  Pool zuk (Without inpainting):')
print(f'    Paper: 1000 backbones x 5 seqs = 5000 total, 1 accepted')
check('zuk total', 5000, zuk_total)
check('zuk accepted', 1, zuk_accepted)

# ============================================================
# 3. BINDER DESIGN (avz, mmo, bbc)
# ============================================================
print('\n' + '=' * 70)
print('3. BINDER DESIGN - INSULIN RECEPTOR (Figura 3, Methods)')
print('   PDB: 4ZXB, Chain E res 6-155, Hotspots: 64, 88, 96')
print('=' * 70)

avz = designs[designs['pool_id'] == 'avz']
avz_total = len(avz)
avz_accepted = int(avz['accepted'].sum())
avz_rate = avz_accepted / avz_total * 100 if avz_total > 0 else 0
print(f'\n  Pool avz (Default weights, ProteinMPNN + FastRelax):')
print(f'    Paper: 1000 backbones x 4 designs = 4000 total, 5 accepted')
print(f'    Thresholds: iPAE<10, pLDDT>80, Binder RMSD<2, ddG<-20')
check('avz total', 4000, avz_total)
check('avz accepted', 5, avz_accepted)
print(f'    Success rate: {avz_rate:.3f}% (paper: ~0.125%)')

mmo = designs[designs['pool_id'] == 'mmo']
mmo_total = len(mmo)
mmo_accepted = int(mmo['accepted'].sum())
print(f'\n  Pool mmo (Complex_beta sheet weights):')
print(f'    Paper: "1 accepted design with 20% of the structure forming beta sheets"')
check('mmo total', 4000, mmo_total)
check('mmo accepted', 1, mmo_accepted)

bbc = designs[designs['pool_id'] == 'bbc']
bbc_total = len(bbc)
bbc_accepted = int(bbc['accepted'].sum())
print(f'\n  Pool bbc (LigandMPNN, ProteinMPNN weights):')
print(f'    Paper: "4 designs per backbone...yielded 3 accepted designs"')
check('bbc total', 4000, bbc_total)
check('bbc accepted', 3, bbc_accepted)

# ============================================================
# 4. PARTIAL DIFFUSION (qki)
# ============================================================
print('\n' + '=' * 70)
print('4. BINDER DIVERSIFICATION - PARTIAL DIFFUSION (Figura 4, Methods)')
print('   Partial diffusion of top 3 most AF2 confident RFdiffusion designs')
print('=' * 70)

qki = designs[designs['pool_id'] == 'qki']
qki_total = len(qki)
qki_accepted = int(qki['accepted'].sum())
qki_rate = qki_accepted / qki_total * 100 if qki_total > 0 else 0
print(f'\n  Pool qki (Partial diffusion, T=20):')
print(f'    Paper: "50 backbones x 2 fastrelax steps" = ~450 total')
print(f'    Paper: "37 out of 450 designs were accepted...8.2% success rate"')
check('qki total', 450, qki_total)
check('qki accepted', 37, qki_accepted)
print(f'    Success rate: {qki_rate:.1f}% (paper: 8.2%)')
check('Success rate ~8.2%', 8.2, round(qki_rate, 1))

# ============================================================
# 5. BINDCRAFT (rsj)
# ============================================================
print('\n' + '=' * 70)
print('5. BINDCRAFT BINDER DESIGN (Figura 3d-e, Methods)')
print('   PDB: 4ZXB, Chain E, 50-100 residues, Hotspots: 64, 88, 96')
print('=' * 70)

rsj = designs[designs['pool_id'] == 'rsj']
rsj_total = len(rsj)
rsj_accepted = int(rsj['accepted'].sum())
rsj_rejected = rsj_total - rsj_accepted
rsj_rate = rsj_accepted / rsj_total * 100 if rsj_total > 0 else 0
print(f'\n  Pool rsj (BindCraft, 6h on A10G GPU):')
print(f'    Paper: "13 designs accepted...and 95 designs rejected" = 108 total')
check('rsj total', 108, rsj_total)
check('rsj accepted', 13, rsj_accepted)
check('rsj rejected', 95, rsj_rejected)
print(f'    Success rate: {rsj_rate:.2f}% (13/108 = 12.04%)')

# ============================================================
# 6. PROTEINQC TOTAL
# ============================================================
print('\n' + '=' * 70)
print('6. PROTEINQC TOTAL ACCEPTED (Figura 5)')
print('=' * 70)

total_accepted = int(designs['accepted'].sum())
total_designs = len(designs)
print(f'\n  Paper: "361 accepted de novo designs combined from the three example tasks"')
print(f'  Datos: {total_accepted} accepted de {total_designs} total designs')
check('Total accepted', 361, total_accepted)

print(f'\n  Breakdown por pool:')
breakdown = {}
for pid in ['ogc','jov','xeh','zuk','avz','mmo','bbc','qki','rsj']:
    pool = designs[designs['pool_id'] == pid]
    acc = int(pool['accepted'].sum())
    tot = len(pool)
    breakdown[pid] = (acc, tot)
    rate_str = f'{acc/tot*100:.2f}%' if tot > 0 else 'N/A'
    print(f'    {pid}: {acc:>4} / {tot:>5} aceptados ({rate_str})')
print(f'    {"TOTAL":>4}: {sum(a for a,_ in breakdown.values()):>4} / {sum(t for _,t in breakdown.values()):>5}')

# ============================================================
# 7. THRESHOLDS
# ============================================================
print('\n' + '=' * 70)
print('7. VERIFICACION DE THRESHOLDS (desde OVO DB)')
print('=' * 70)

threshold_cols = [c for c in jobs.columns if 'Thresholds' in str(c)]
for pid in ['ogc','jov','xeh','zuk','avz','mmo','bbc','qki','rsj']:
    if pid in jobs.index:
        name = jobs.loc[pid, ("Pool","name")]
        if isinstance(name, str):
            name = name.encode('ascii', 'replace').decode('ascii')
        print(f'\n  {pid} ({name}):')
        for col in threshold_cols:
            val = jobs.loc[pid, col]
            if pd.notna(val):
                val_str = str(val).encode('ascii', 'replace').decode('ascii')
                print(f'    {col[1]}: {val_str}')

# ============================================================
# RESUMEN
# ============================================================
print('\n' + '=' * 70)
print('RESUMEN FINAL DE VERIFICACION')
print('=' * 70)
total_checks = len(results)
passed = sum(results)
failed = total_checks - passed
print(f'  Total verificaciones: {total_checks}')
print(f'  Coinciden:            {passed}/{total_checks}')
print(f'  Diferencias:          {failed}/{total_checks}')

if failed == 0:
    print('\n  *** TODOS LOS VALORES COINCIDEN EXACTAMENTE CON EL PAPER ***')
elif failed <= 2:
    print(f'\n  La mayoria de datos coinciden con el paper.')
    print(f'  Se encontraron {failed} diferencia(s) menor(es).')
print('=' * 70)
