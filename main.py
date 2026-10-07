# ============================================================
# LOGISMART PYTHON SUITE - PROYECTO INTEGRADOR (FASE 6)
# ============================================================

from logismart.peas import AgenteLogiSmart
from logismart.logica import evaluar_camion_ampliado
from logismart.incidentes import (
    clasificar_incidente_hibrido,
    enviar_correo_soporte
)
from logismart.riesgos import EvaluadorRiesgosIA


def main():

    print("\n")
    print("=" * 60)
    print("             LOGISMART PYTHON SUITE (INTEGRADO)")
    print("=" * 60)

    # 1. PEAS
    agente = AgenteLogiSmart()
    agente.mostrar_peas()

    # 2. MOTOR DE REGLAS AMPLIADO
    print("\n\n========== MOTOR DE REGLAS AMPLIADO ==========")
    resultado = evaluar_camion_ampliado(
        P=True,
        Q=True,
        R=True,
        S=False
    )

    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")

    # 3. CLASIFICACIÓN DE INCIDENTE & PERSISTENCIA MONGO
    print("\n\n========== CLASIFICACIÓN E INSERCIÓN EN MONGODB ==========")
    incidente = clasificar_incidente_hibrido(
        placa="XYZ-789",
        tipo="Control de acceso",
        descripcion="Vehículo detectado con exceso de peso y carga peligrosa",
        nivel=9,
        guardar_db=True
    )

    print(incidente)

    enviar_correo_soporte(
        destinatario="soporte@logismart.com",
        asunto="Incidente Crítico Detectado",
        mensaje=incidente
    )

    # 4. EVALUACIÓN DE RIESGOS
    print("\n\n========== EVALUACIÓN DE RIESGOS ==========")
    evaluador = EvaluadorRiesgosIA()

    evaluador.registrar_riesgo(
        modulo="Cámara de detección",
        riesgo="Sesgo en condiciones nocturnas",
        categoria="Sesgo",
        impacto="Alto",
        probabilidad="Media",
        mitigacion="Realizar pruebas con diferentes condiciones de iluminación"
    )

    evaluador.registrar_riesgo(
        modulo="Sistema de vigilancia",
        riesgo="Uso inadecuado de información personal",
        categoria="Privacidad",
        impacto="Alto",
        probabilidad="Media",
        mitigacion="Aplicar controles de acceso y políticas de retención"
    )

    evaluador.mostrar_riesgos()
    evaluador.exportar_reporte("reportes/reporte_riesgos.json")

    print("\n")
    print("=" * 60)
    print("             SISTEMA FINALIZADO CON ÉXITO")
    print("=" * 60)


if __name__ == "__main__":
    main()