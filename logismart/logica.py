# ============================================================
# FASE 4 - MOTOR DE REGLAS LÓGICAS AMPLIADO
# ============================================================

def evaluar_camion_ampliado(P, Q, R, S):
    """
    Evalúa las reglas de acceso con lógica proposicional.

    Variables proposicionales:
    P = Autorización previa (True/False)
    Q = Peso excedido (True/False)
    R = Carga con materiales peligrosos (True/False)
    S = Certificación vigente (True/False)
    """

    # ------------------------------------------------------------
    # REGLAS EXISTENTES
    # ------------------------------------------------------------
    # Regla 1: Acceso Estándar = P y S y no Q
    acceso_estandar = P and S and not Q

    # Regla 2: Inspección Especial = P y (R o Q)
    inspeccion_especial = P and (R or Q)

    # ------------------------------------------------------------
    # REGLAS NUEVAS (Requerimiento Fase 4)
    # ------------------------------------------------------------
    # Regla 3: Protocolo Hazmat Critico = R y no S
    # (Carga peligrosa sin certificación vigente requiere retención inmediata)
    protocolo_hazmat_critico = R and not S

    # Regla 4: Bloqueo Total = Q y R
    # (Exceso de peso combinado con carga peligrosa genera denegación absoluta)
    bloqueo_total = Q and R

    # ------------------------------------------------------------
    # DETECCIÓN DE CONTRADICCIONES
    # ------------------------------------------------------------
    # Contradicción: Se intenta dar acceso estándar teniendo un bloqueo total o protocolo crítico
    deteccion_contradiccion = acceso_estandar and (bloqueo_total or protocolo_hazmat_critico)

    # Decisión final del sistema
    if bloqueo_total:
        estatus_final = "ACCESO DENEGADO (Bloqueo Total por Riesgo)"
    elif protocolo_hazmat_critico:
        estatus_final = "RETENIDO (Material Peligroso sin Certificación)"
    elif inspeccion_especial:
        estatus_final = "REQUIERE INSPECCIÓN ESPECIAL"
    elif acceso_estandar:
        estatus_final = "ACCESO PERMITIDO"
    else:
        estatus_final = "ACCESO DENEGADO (No cumple requisitos)"

    return {
        "autorizacion": P,
        "peso_excedido": Q,
        "carga_peligrosa": R,
        "certificacion": S,
        "acceso_estandar": acceso_estandar,
        "inspeccion_especial": inspeccion_especial,
        "protocolo_hazmat_critico": protocolo_hazmat_critico,
        "bloqueo_total": bloqueo_total,
        "contradiccion_detectada": deteccion_contradiccion,
        "estatus_final": estatus_final
    }

if __name__ == "__main__":
    print("\n========== PRUEBA DEL MOTOR DE REGLAS AMPLIADO ==========")
    
    # Ejemplo de prueba: Camión con carga peligrosa y peso excedido
    res = evaluar_camion_ampliado(P=True, Q=True, R=True, S=True)
    
    for k, v in res.items():
        print(f"{k}: {v}")