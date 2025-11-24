from typing import List
from evaluation import Evaluation
from attendance_policy import AttendancePolicy
from extra_points_policy import ExtraPointsPolicy
from grade_calculator import GradeCalculator


class GradeCalculatorApp:
    def __init__(self):
        self.calculator = None

    def run(self) -> None:
        print("=" * 60)
        print("Sistema CS-GradeCalculator - UTEC")
        print("Calculo de Nota Final de Estudiantes")
        print("=" * 60)
        print()

        try:
            student_id = self._get_student_id()
            print(f"\nProcesando estudiante: {student_id}")
            print("-" * 60)

            attendance_policy = self._configure_attendance_policy()
            extra_points_policy = self._configure_extra_points_policy()

            self.calculator = GradeCalculator(attendance_policy, extra_points_policy)

            examsStudents = self._register_evaluations()
            hasReachedMinimumClasses = self._register_attendance()

            print("\n" + "=" * 60)
            print("CALCULANDO NOTA FINAL...")
            print("=" * 60)

            details = self.calculator.get_calculation_details(examsStudents, hasReachedMinimumClasses)

            self._display_results(student_id, details)

        except KeyboardInterrupt:
            print("\n\nOperacion cancelada por el usuario.")
        except Exception as error:
            print(f"\n\nError: {error}")

    def _get_student_id(self) -> str:
        while True:
            student_id = input("Ingrese el codigo del estudiante: ").strip()
            if student_id:
                return student_id
            print("Error: El codigo no puede estar vacio.\n")

    def _configure_attendance_policy(self) -> AttendancePolicy:
        print("\n--- Configuracion de Politica de Asistencia ---")
        while True:
            try:
                penalty = input(f"Penalizacion por inasistencia [default: {AttendancePolicy.DEFAULT_PENALTY}]: ").strip()
                if not penalty:
                    return AttendancePolicy()
                penalty_value = float(penalty)
                return AttendancePolicy(penalty_value)
            except ValueError as error:
                print(f"Error: {error}. Intente nuevamente.\n")

    def _configure_extra_points_policy(self) -> ExtraPointsPolicy:
        print("\n--- Configuracion de Politica de Puntos Extra ---")

        while True:
            response = input("Los docentes estan de acuerdo en otorgar puntos extra? (s/n): ").strip().lower()
            if response in ['s', 'n']:
                allYearsTeachers = response == 's'
                break
            print("Error: Responda 's' para si o 'n' para no.\n")

        if allYearsTeachers:
            while True:
                try:
                    points = input(f"Cantidad de puntos extra [default: {ExtraPointsPolicy.DEFAULT_EXTRA_POINTS}]: ").strip()
                    if not points:
                        return ExtraPointsPolicy(True)
                    points_value = float(points)
                    return ExtraPointsPolicy(True, points_value)
                except ValueError as error:
                    print(f"Error: {error}. Intente nuevamente.\n")
        else:
            return ExtraPointsPolicy(False)

    def _register_evaluations(self) -> List[Evaluation]:
        print("\n--- Registro de Evaluaciones ---")
        print(f"Maximo {GradeCalculator.MAX_EVALUATIONS} evaluaciones permitidas")

        evaluations = []

        while True:
            try:
                count = int(input("\nCuantas evaluaciones desea registrar? "))
                if count < 1:
                    print("Error: Debe registrar al menos una evaluacion.")
                    continue
                if count > GradeCalculator.MAX_EVALUATIONS:
                    print(f"Error: Maximo {GradeCalculator.MAX_EVALUATIONS} evaluaciones permitidas.")
                    continue
                break
            except ValueError:
                print("Error: Ingrese un numero valido.")

        print()
        for i in range(count):
            print(f"\nEvaluacion {i + 1}:")
            evaluation = self._input_evaluation()
            evaluations.append(evaluation)

        total_weight = sum(e.weight for e in evaluations)
        print(f"\nPeso total de evaluaciones: {total_weight:.2f}")
        if abs(total_weight - 1.0) > 0.01:
            print(f"Advertencia: Los pesos deberian sumar 1.0 (actual: {total_weight:.2f})")
            confirm = input("Desea continuar de todas formas? (s/n): ").strip().lower()
            if confirm != 's':
                return self._register_evaluations()

        return evaluations

    def _input_evaluation(self) -> Evaluation:
        while True:
            try:
                name = input("  Nombre de la evaluacion: ").strip()
                grade = float(input("  Nota obtenida (0-20): "))
                weight = float(input("  Peso sobre nota final (0-1): "))
                return Evaluation(name, grade, weight)
            except ValueError as error:
                print(f"  Error: {error}. Intente nuevamente.\n")

    def _register_attendance(self) -> bool:
        print("\n--- Registro de Asistencia ---")
        while True:
            response = input("El estudiante cumplio con la asistencia minima? (s/n): ").strip().lower()
            if response in ['s', 'n']:
                return response == 's'
            print("Error: Responda 's' para si o 'n' para no.\n")

    def _display_results(self, student_id: str, details: dict) -> None:
        print("\n" + "=" * 60)
        print(f"RESULTADOS - ESTUDIANTE: {student_id}")
        print("=" * 60)

        print("\nDETALLE DE EVALUACIONES:")
        print("-" * 60)
        for i, eval_detail in enumerate(details['evaluations_detail'], 1):
            print(f"{i}. {eval_detail['name']}")
            print(f"   Nota: {eval_detail['grade']:.2f}")
            print(f"   Peso: {eval_detail['weight'] * 100:.1f}%")
            print(f"   Aporte: {eval_detail['weighted_grade']:.2f}")
            print()

        print("CALCULO DE NOTA FINAL:")
        print("-" * 60)
        print(f"Promedio Ponderado:        {details['weighted_average']:>6.2f}")

        if details['attendance_penalty'] > 0:
            print(f"Penalizacion (Asistencia): {details['attendance_penalty']:>6.2f} (-)")
        else:
            print(f"Penalizacion (Asistencia): {details['attendance_penalty']:>6.2f}")

        if details['extra_points'] > 0:
            print(f"Puntos Extra:              {details['extra_points']:>6.2f} (+)")
        else:
            print(f"Puntos Extra:              {details['extra_points']:>6.2f}")

        print("-" * 60)
        print(f"NOTA FINAL:                {details['final_grade']:>6.2f}")
        print("=" * 60)

        print("\nINFORMACION ADICIONAL:")
        print(f"- Total de evaluaciones: {details['total_evaluations']}")
        print(f"- Asistencia minima cumplida: {'Si' if details['hasReachedMinimumClasses'] else 'No'}")
        print()


def main():
    app = GradeCalculatorApp()
    app.run()


if __name__ == "__main__":
    main()
