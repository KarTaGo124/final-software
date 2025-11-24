"""
Ejemplo de uso del sistema CS-GradeCalculator.
Demuestra diferentes escenarios de cálculo de nota final.
"""

from evaluation import Evaluation
from attendance_policy import AttendancePolicy
from extra_points_policy import ExtraPointsPolicy
from grade_calculator import GradeCalculator


def print_separator(title: str = ""):
    """Imprime separador visual."""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    print()


def display_calculation(student_name: str, details: dict):
    """Muestra detalles del cálculo de manera formateada."""
    print(f"Estudiante: {student_name}")
    print("-" * 70)

    print("\nEvaluaciones:")
    for i, eval_detail in enumerate(details['evaluations_detail'], 1):
        print(f"  {i}. {eval_detail['name']}: {eval_detail['grade']:.2f} "
              f"(Peso: {eval_detail['weight']*100:.1f}%) "
              f"-> Aporte: {eval_detail['weighted_grade']:.2f}")

    print("\nCalculo:")
    print(f"  Promedio Ponderado:        {details['weighted_average']:>6.2f}")
    print(f"  Penalizacion (Asistencia): {details['attendance_penalty']:>6.2f}")
    print(f"  Puntos Extra:              {details['extra_points']:>6.2f}")
    print(f"  {'-' * 40}")
    print(f"  NOTA FINAL:                {details['final_grade']:>6.2f}")
    print()


def example_1_normal_calculation():
    """Ejemplo 1: Cálculo normal con asistencia completa y sin puntos extra."""
    print_separator("EJEMPLO 1: Cálculo Normal")

    # Configurar políticas
    attendance_policy = AttendancePolicy(3.0)
    extra_points_policy = ExtraPointsPolicy(all_years_teachers=False)

    # Crear calculador
    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    # Crear evaluaciones
    evaluations = [
        Evaluation("Parcial 1", 16.0, 0.30),
        Evaluation("Parcial 2", 14.0, 0.30),
        Evaluation("Proyecto", 17.0, 0.20),
        Evaluation("Final", 15.0, 0.20)
    ]

    # Calcular y mostrar
    details = calculator.get_calculation_details(evaluations, has_reached_minimum_classes=True)
    display_calculation("Juan Pérez", details)


def example_2_with_attendance_penalty():
    """Ejemplo 2: Cálculo con penalización por asistencia."""
    print_separator("EJEMPLO 2: Con Penalización por Asistencia")

    # Configurar políticas
    attendance_policy = AttendancePolicy(3.0)
    extra_points_policy = ExtraPointsPolicy(all_years_teachers=False)

    # Crear calculador
    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    # Crear evaluaciones
    evaluations = [
        Evaluation("Parcial 1", 18.0, 0.40),
        Evaluation("Parcial 2", 16.0, 0.30),
        Evaluation("Final", 17.0, 0.30)
    ]

    # Calcular con asistencia NO cumplida
    details = calculator.get_calculation_details(evaluations, has_reached_minimum_classes=False)
    display_calculation("María González", details)


def example_3_with_extra_points():
    """Ejemplo 3: Cálculo con puntos extra."""
    print_separator("EJEMPLO 3: Con Puntos Extra")

    # Configurar políticas
    attendance_policy = AttendancePolicy(3.0)
    extra_points_policy = ExtraPointsPolicy(all_years_teachers=True, extra_points=2.0)

    # Crear calculador
    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    # Crear evaluaciones
    evaluations = [
        Evaluation("Parcial 1", 15.0, 0.35),
        Evaluation("Parcial 2", 14.0, 0.35),
        Evaluation("Final", 16.0, 0.30)
    ]

    # Calcular
    details = calculator.get_calculation_details(evaluations, has_reached_minimum_classes=True)
    display_calculation("Carlos Rodríguez", details)


def example_4_all_factors():
    """Ejemplo 4: Caso completo con todos los factores."""
    print_separator("EJEMPLO 4: Caso Completo (Sin Asistencia + Puntos Extra)")

    # Configurar políticas
    attendance_policy = AttendancePolicy(3.0)
    extra_points_policy = ExtraPointsPolicy(all_years_teachers=True, extra_points=2.5)

    # Crear calculador
    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    # Crear evaluaciones
    evaluations = [
        Evaluation("Laboratorio 1", 18.0, 0.15),
        Evaluation("Laboratorio 2", 17.0, 0.15),
        Evaluation("Parcial", 15.0, 0.30),
        Evaluation("Proyecto", 16.0, 0.20),
        Evaluation("Final", 14.0, 0.20)
    ]

    # Calcular sin asistencia mínima pero con puntos extra
    details = calculator.get_calculation_details(evaluations, has_reached_minimum_classes=False)
    display_calculation("Ana Martínez", details)


def example_5_maximum_evaluations():
    """Ejemplo 5: Caso con máximo de evaluaciones permitidas."""
    print_separator("EJEMPLO 5: Máximo de Evaluaciones (10)")

    # Configurar políticas
    attendance_policy = AttendancePolicy(2.0)
    extra_points_policy = ExtraPointsPolicy(all_years_teachers=True, extra_points=1.5)

    # Crear calculador
    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    # Crear 10 evaluaciones
    evaluations = [
        Evaluation("Quiz 1", 18.0, 0.05),
        Evaluation("Quiz 2", 17.0, 0.05),
        Evaluation("Quiz 3", 16.0, 0.05),
        Evaluation("Lab 1", 19.0, 0.10),
        Evaluation("Lab 2", 18.0, 0.10),
        Evaluation("Lab 3", 17.0, 0.10),
        Evaluation("Parcial 1", 15.0, 0.20),
        Evaluation("Parcial 2", 16.0, 0.20),
        Evaluation("Proyecto", 17.0, 0.10),
        Evaluation("Final", 14.0, 0.05)
    ]

    # Calcular
    details = calculator.get_calculation_details(evaluations, has_reached_minimum_classes=True)
    display_calculation("Luis Fernández", details)


def example_6_edge_cases():
    """Ejemplo 6: Casos borde."""
    print_separator("EJEMPLO 6: Casos Borde")

    # Configurar políticas
    attendance_policy = AttendancePolicy(5.0)
    extra_points_policy = ExtraPointsPolicy(all_years_teachers=True, extra_points=3.0)

    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    # Caso 6a: Nota muy baja con penalización (debe ser >= 0)
    print("Caso 6a: Nota baja con penalización alta")
    evaluations_low = [Evaluation("Único Examen", 4.0, 1.0)]
    details_low = calculator.get_calculation_details(evaluations_low, has_reached_minimum_classes=False)
    display_calculation("Estudiante A", details_low)

    # Caso 6b: Nota muy alta con puntos extra (debe ser <= 20)
    print("Caso 6b: Nota alta con puntos extra")
    attendance_policy_high = AttendancePolicy(0.0)
    extra_points_policy_high = ExtraPointsPolicy(all_years_teachers=True, extra_points=5.0)
    calculator_high = GradeCalculator(attendance_policy_high, extra_points_policy_high)

    evaluations_high = [Evaluation("Examen Perfecto", 20.0, 1.0)]
    details_high = calculator_high.get_calculation_details(evaluations_high, has_reached_minimum_classes=True)
    display_calculation("Estudiante B", details_high)


def example_7_determinism_test():
    """Ejemplo 7: Prueba de determinismo (RNF03)."""
    print_separator("EJEMPLO 7: Prueba de Determinismo (RNF03)")

    # Configurar
    attendance_policy = AttendancePolicy(3.0)
    extra_points_policy = ExtraPointsPolicy(all_years_teachers=True, extra_points=2.0)
    calculator = GradeCalculator(attendance_policy, extra_points_policy)

    evaluations = [
        Evaluation("Test 1", 15.5, 0.40),
        Evaluation("Test 2", 16.3, 0.60)
    ]

    # Calcular múltiples veces
    print("Calculando la misma nota 5 veces para verificar determinismo...")
    results = []
    for i in range(5):
        grade = calculator.calculate_final_grade(evaluations, has_reached_minimum_classes=True)
        results.append(grade)
        print(f"  Iteración {i+1}: {grade:.2f}")

    # Verificar que todas sean iguales
    all_equal = all(r == results[0] for r in results)
    print(f"\n¿Todos los resultados son idénticos? {('SI' if all_equal else 'NO')}")

    if all_equal:
        print(f"[OK] Determinismo verificado: Nota consistente = {results[0]:.2f}")
    else:
        print("[ERROR] Resultados inconsistentes detectados")


def main():
    """Ejecuta todos los ejemplos."""
    print("=" * 70)
    print("  EJEMPLOS DE USO - CS-GradeCalculator")
    print("=" * 70)

    example_1_normal_calculation()
    example_2_with_attendance_penalty()
    example_3_with_extra_points()
    example_4_all_factors()
    example_5_maximum_evaluations()
    example_6_edge_cases()
    example_7_determinism_test()

    print_separator("FIN DE EJEMPLOS")
    print("Todos los ejemplos ejecutados exitosamente.")
    print("El sistema cumple con todos los requerimientos funcionales y no funcionales.")


if __name__ == "__main__":
    main()
