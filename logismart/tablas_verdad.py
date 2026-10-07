# ============================================================
# FASE 4 - TABLA DE VERDAD COMPLETA
# ============================================================

from itertools import product
from logismart.logica import evaluar_camion_ampliado

def generar_tabla_verdad_completa():
    print("\n==========================================================================")
    print("                        TABLA DE VERDAD AMPLIADA")
    print("==========================================================================")
    print("P Q R S | A (Estándar) | E (Inspec.) | H (Hazmat C.) | B (Bloqueo) | Estatus")
    print("-" * 74)

    for P, Q, R, S in product([False, True], repeat=4):
        res = evaluar_camion_ampliado(P, Q, R, S)
        print(
            f"{int(P)} {int(Q)} {int(R)} {int(S)} | "
            f"      {int(res['acceso_estandar'])}        | "
            f"     {int(res['inspeccion_especial'])}      | "
            f"      {int(res['protocolo_hazmat_critico'])}       | "
            f"     {int(res['bloqueo_total'])}     | "
            f"{res['estatus_final'][:18]}"
        )

if __name__ == "__main__":
    generar_tabla_verdad_completa()