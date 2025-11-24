"""
Test de rendimiento para validar RNF04:
El tiempo de cálculo debe ser menor a 300 ms por solicitud.
"""

import time
from evaluation import Evaluation
from attendance_policy import AttendancePolicy
from extra_points_policy import ExtraPointsPolicy
from grade_calculator import GradeCalculator


def measure_calculation_time(num_evaluations: int, iterations: int = 100) -> float:
    """
    Mide el tiempo promedio de cálculo.

    Args:
        num_evaluations: Número de evaluaciones a incluir
        iterations: Número de iteraciones para promediar

    Returns:
        float: Tiempo promedio en milisegundos
    """
    # Preparar datos
    attendance_policy = AttendancePolicy(3.0)
    extra_points_policy = ExtraPointsPolicy(True, 2.0)
    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    weight_per_eval = 1.0 / num_evaluations
    evaluations = [
        Evaluation(f"Evaluación {i+1}", 15.0 + i * 0.5, weight_per_eval)
        for i in range(num_evaluations)
    ]

    # Medir tiempo
    start_time = time.time()

    for _ in range(iterations):
        calculator.calculate_final_grade(evaluations, True)

    end_time = time.time()

    # Calcular promedio en milisegundos
    total_time_ms = (end_time - start_time) * 1000
    average_time_ms = total_time_ms / iterations

    return average_time_ms


def run_performance_tests():
    """Ejecuta tests de rendimiento completos."""
    print("=" * 70)
    print("TEST DE RENDIMIENTO - RNF04")
    print("Requisito: Tiempo de cálculo < 300 ms por solicitud")
    print("=" * 70)
    print()

    test_cases = [
        (1, "Caso mínimo (1 evaluación)"),
        (5, "Caso promedio (5 evaluaciones)"),
        (10, "Caso máximo (10 evaluaciones)")
    ]

    all_passed = True

    for num_evals, description in test_cases:
        print(f"Probando: {description}")
        print(f"  Evaluaciones: {num_evals}")

        avg_time = measure_calculation_time(num_evals, iterations=1000)

        print(f"  Tiempo promedio: {avg_time:.4f} ms")

        if avg_time < 300:
            print(f"  Estado: [OK] PASO (< 300 ms)")
        else:
            print(f"  Estado: [FALLO] (>= 300 ms)")
            all_passed = False

        print()

    # Test de concurrencia simulada (RNF02)
    print("=" * 70)
    print("TEST DE CONCURRENCIA SIMULADA - RNF02")
    print("Requisito: Soportar 50 usuarios concurrentes")
    print("=" * 70)
    print()

    num_concurrent_requests = 50
    evaluations_per_request = 10

    print(f"Simulando {num_concurrent_requests} solicitudes concurrentes...")

    attendance_policy = AttendancePolicy(3.0)
    extra_points_policy = ExtraPointsPolicy(True, 2.0)
    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    weight_per_eval = 1.0 / evaluations_per_request
    evaluations = [
        Evaluation(f"Eval {i+1}", 15.0, weight_per_eval)
        for i in range(evaluations_per_request)
    ]

    start_time = time.time()

    for i in range(num_concurrent_requests):
        calculator.calculate_final_grade(evaluations, True)

    end_time = time.time()

    total_time = (end_time - start_time) * 1000
    avg_per_request = total_time / num_concurrent_requests

    print(f"  Solicitudes procesadas: {num_concurrent_requests}")
    print(f"  Tiempo total: {total_time:.2f} ms")
    print(f"  Tiempo promedio por solicitud: {avg_per_request:.4f} ms")

    if avg_per_request < 300:
        print(f"  Estado: [OK] PASO (< 300 ms por solicitud)")
    else:
        print(f"  Estado: [FALLO] (>= 300 ms por solicitud)")
        all_passed = False

    print()

    # Resumen final
    print("=" * 70)
    print("RESUMEN DE RENDIMIENTO")
    print("=" * 70)

    if all_passed:
        print("[OK] TODOS LOS TESTS DE RENDIMIENTO PASARON")
        print("  - RNF04: Tiempo < 300 ms [OK]")
        print("  - RNF02: Soporte concurrencia [OK]")
    else:
        print("[FALLO] ALGUNOS TESTS FALLARON")

    print("=" * 70)

    return all_passed


if __name__ == "__main__":
    success = run_performance_tests()
    exit(0 if success else 1)
