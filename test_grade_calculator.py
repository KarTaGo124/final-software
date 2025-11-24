"""
Tests unitarios para el sistema CS-GradeCalculator.
Cumple con los requisitos de pruebas automatizadas del examen.
"""

import unittest
from evaluation import Evaluation
from attendance_policy import AttendancePolicy
from extra_points_policy import ExtraPointsPolicy
from grade_calculator import GradeCalculator


class TestEvaluation(unittest.TestCase):
    """Tests para la clase Evaluation."""

    def test_shouldCreateEvaluationWithValidData(self):
        """Debe crear una evaluación con datos válidos."""
        evaluation = Evaluation("Parcial 1", 15.5, 0.3)
        self.assertEqual(evaluation.name, "Parcial 1")
        self.assertEqual(evaluation.grade, 15.5)
        self.assertEqual(evaluation.weight, 0.3)

    def test_shouldCalculateWeightedGradeCorrectly(self):
        """Debe calcular correctamente la nota ponderada."""
        evaluation = Evaluation("Parcial 1", 16.0, 0.3)
        self.assertAlmostEqual(evaluation.get_weighted_grade(), 4.8, places=2)

    def test_shouldRaiseErrorWhenGradeIsNegative(self):
        """Debe lanzar error cuando la nota es negativa."""
        with self.assertRaises(ValueError):
            Evaluation("Parcial 1", -5, 0.3)

    def test_shouldRaiseErrorWhenGradeExceedsMaximum(self):
        """Debe lanzar error cuando la nota excede el máximo."""
        with self.assertRaises(ValueError):
            Evaluation("Parcial 1", 25, 0.3)

    def test_shouldRaiseErrorWhenWeightIsNegative(self):
        """Debe lanzar error cuando el peso es negativo."""
        with self.assertRaises(ValueError):
            Evaluation("Parcial 1", 15, -0.1)

    def test_shouldRaiseErrorWhenWeightExceedsOne(self):
        """Debe lanzar error cuando el peso excede 1."""
        with self.assertRaises(ValueError):
            Evaluation("Parcial 1", 15, 1.5)

    def test_shouldRaiseErrorWhenNameIsEmpty(self):
        """Debe lanzar error cuando el nombre está vacío."""
        with self.assertRaises(ValueError):
            Evaluation("", 15, 0.3)


class TestAttendancePolicy(unittest.TestCase):
    """Tests para la clase AttendancePolicy."""

    def test_shouldReturnZeroPenaltyWhenAttendanceIsMet(self):
        """Debe retornar penalización cero cuando se cumple asistencia."""
        policy = AttendancePolicy(3.0)
        penalty = policy.calculate_penalty(True)
        self.assertEqual(penalty, 0.0)

    def test_shouldReturnFullPenaltyWhenAttendanceIsNotMet(self):
        """Debe retornar penalización completa cuando no se cumple asistencia."""
        policy = AttendancePolicy(3.0)
        penalty = policy.calculate_penalty(False)
        self.assertEqual(penalty, 3.0)

    def test_shouldUseDefaultPenaltyWhenNotSpecified(self):
        """Debe usar penalización por defecto cuando no se especifica."""
        policy = AttendancePolicy()
        penalty = policy.calculate_penalty(False)
        self.assertEqual(penalty, AttendancePolicy.DEFAULT_PENALTY)

    def test_shouldRaiseErrorWhenPenaltyIsNegative(self):
        """Debe lanzar error cuando la penalización es negativa."""
        with self.assertRaises(ValueError):
            AttendancePolicy(-1.0)


class TestExtraPointsPolicy(unittest.TestCase):
    """Tests para la clase ExtraPointsPolicy."""

    def test_shouldReturnExtraPointsWhenPolicyIsActive(self):
        """Debe retornar puntos extra cuando la política está activa."""
        policy = ExtraPointsPolicy(True, 2.0)
        extra = policy.calculate_extra_points()
        self.assertEqual(extra, 2.0)

    def test_shouldReturnZeroWhenPolicyIsInactive(self):
        """Debe retornar cero cuando la política está inactiva."""
        policy = ExtraPointsPolicy(False, 2.0)
        extra = policy.calculate_extra_points()
        self.assertEqual(extra, 0.0)

    def test_shouldUseDefaultPointsWhenNotSpecified(self):
        """Debe usar puntos por defecto cuando no se especifican."""
        policy = ExtraPointsPolicy(True)
        extra = policy.calculate_extra_points()
        self.assertEqual(extra, ExtraPointsPolicy.DEFAULT_EXTRA_POINTS)

    def test_shouldRaiseErrorWhenExtraPointsAreNegative(self):
        """Debe lanzar error cuando los puntos extra son negativos."""
        with self.assertRaises(ValueError):
            ExtraPointsPolicy(True, -1.0)


class TestGradeCalculator(unittest.TestCase):
    """Tests para la clase GradeCalculator."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.attendance_policy = AttendancePolicy(3.0)
        self.extra_points_policy = ExtraPointsPolicy(False, 2.0)
        self.calculator = GradeCalculator(self.attendance_policy, self.extra_points_policy)

    def test_shouldCalculateNormalGradeCorrectly(self):
        """Debe calcular correctamente una nota normal."""
        evaluations = [
            Evaluation("Parcial 1", 16.0, 0.3),
            Evaluation("Parcial 2", 14.0, 0.3),
            Evaluation("Final", 18.0, 0.4)
        ]
        final_grade = self.calculator.calculate_final_grade(evaluations, True)
        expected = 16.0 * 0.3 + 14.0 * 0.3 + 18.0 * 0.4
        self.assertAlmostEqual(final_grade, expected, places=2)

    def test_shouldApplyPenaltyWhenAttendanceIsNotMet(self):
        """Debe aplicar penalización cuando no se cumple asistencia mínima."""
        evaluations = [
            Evaluation("Parcial 1", 16.0, 0.5),
            Evaluation("Parcial 2", 14.0, 0.5)
        ]
        final_grade = self.calculator.calculate_final_grade(evaluations, False)
        expected = (16.0 * 0.5 + 14.0 * 0.5) - 3.0
        self.assertAlmostEqual(final_grade, expected, places=2)

    def test_shouldApplyExtraPointsWhenPolicyIsActive(self):
        """Debe aplicar puntos extra cuando la política está activa."""
        policy_with_extra = ExtraPointsPolicy(True, 2.0)
        calculator = GradeCalculator(self.attendance_policy, policy_with_extra)
        evaluations = [
            Evaluation("Parcial 1", 16.0, 0.5),
            Evaluation("Parcial 2", 14.0, 0.5)
        ]
        final_grade = calculator.calculate_final_grade(evaluations, True)
        expected = (16.0 * 0.5 + 14.0 * 0.5) + 2.0
        self.assertAlmostEqual(final_grade, expected, places=2)

    def test_shouldNotApplyExtraPointsWhenPolicyIsInactive(self):
        """No debe aplicar puntos extra cuando la política está inactiva."""
        evaluations = [
            Evaluation("Parcial 1", 16.0, 0.5),
            Evaluation("Parcial 2", 14.0, 0.5)
        ]
        final_grade = self.calculator.calculate_final_grade(evaluations, True)
        expected = 16.0 * 0.5 + 14.0 * 0.5
        self.assertAlmostEqual(final_grade, expected, places=2)

    def test_shouldHandleBorderCaseWithZeroEvaluations(self):
        """Debe manejar caso borde con cero evaluaciones."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_final_grade([], True)

    def test_shouldHandleBorderCaseWithMaximumEvaluations(self):
        """Debe manejar caso borde con máximo de evaluaciones permitidas."""
        evaluations = [
            Evaluation(f"Eval {i}", 15.0, 0.1)
            for i in range(GradeCalculator.MAX_EVALUATIONS)
        ]
        final_grade = self.calculator.calculate_final_grade(evaluations, True)
        self.assertIsNotNone(final_grade)
        self.assertGreaterEqual(final_grade, 0)
        self.assertLessEqual(final_grade, 20)

    def test_shouldRaiseErrorWhenExceedingMaximumEvaluations(self):
        """Debe lanzar error cuando se excede el máximo de evaluaciones."""
        evaluations = [
            Evaluation(f"Eval {i}", 15.0, 0.1)
            for i in range(GradeCalculator.MAX_EVALUATIONS + 1)
        ]
        with self.assertRaises(ValueError):
            self.calculator.calculate_final_grade(evaluations, True)

    def test_shouldHandleBorderCaseWithInvalidWeights(self):
        """Debe manejar caso borde con pesos inválidos en evaluaciones."""
        with self.assertRaises(ValueError):
            evaluations = [Evaluation("Test", 15.0, -0.1)]
            self.calculator.calculate_final_grade(evaluations, True)

    def test_shouldCapFinalGradeAtMaximum(self):
        """Debe limitar la nota final al máximo permitido."""
        policy_with_extra = ExtraPointsPolicy(True, 10.0)
        calculator = GradeCalculator(self.attendance_policy, policy_with_extra)
        evaluations = [
            Evaluation("Perfect", 20.0, 1.0)
        ]
        final_grade = calculator.calculate_final_grade(evaluations, True)
        self.assertEqual(final_grade, 20.0)

    def test_shouldCapFinalGradeAtMinimum(self):
        """Debe limitar la nota final al mínimo permitido."""
        policy_high_penalty = AttendancePolicy(25.0)
        calculator = GradeCalculator(policy_high_penalty, self.extra_points_policy)
        evaluations = [
            Evaluation("Low", 5.0, 1.0)
        ]
        final_grade = calculator.calculate_final_grade(evaluations, False)
        self.assertEqual(final_grade, 0.0)

    def test_shouldReturnCalculationDetailsCorrectly(self):
        """Debe retornar detalles del cálculo correctamente."""
        evaluations = [
            Evaluation("Parcial 1", 16.0, 0.5),
            Evaluation("Parcial 2", 14.0, 0.5)
        ]
        details = self.calculator.get_calculation_details(evaluations, True)

        self.assertIn('weighted_average', details)
        self.assertIn('attendance_penalty', details)
        self.assertIn('extra_points', details)
        self.assertIn('final_grade', details)
        self.assertIn('evaluations_detail', details)
        self.assertEqual(len(details['evaluations_detail']), 2)

    def test_shouldBeConsistentAcrossMultipleCalls(self):
        """Debe ser consistente en múltiples llamadas (determinismo RNF03)."""
        evaluations = [
            Evaluation("Parcial 1", 16.0, 0.3),
            Evaluation("Parcial 2", 14.0, 0.3),
            Evaluation("Final", 18.0, 0.4)
        ]

        grade1 = self.calculator.calculate_final_grade(evaluations, True)
        grade2 = self.calculator.calculate_final_grade(evaluations, True)
        grade3 = self.calculator.calculate_final_grade(evaluations, True)

        self.assertEqual(grade1, grade2)
        self.assertEqual(grade2, grade3)

    def test_shouldHandleDecimalGradesCorrectly(self):
        """Debe manejar correctamente notas con decimales."""
        evaluations = [
            Evaluation("Test", 15.75, 0.6),
            Evaluation("Quiz", 13.25, 0.4)
        ]
        final_grade = self.calculator.calculate_final_grade(evaluations, True)
        expected = 15.75 * 0.6 + 13.25 * 0.4
        self.assertAlmostEqual(final_grade, expected, places=2)


class TestGradeCalculatorIntegration(unittest.TestCase):
    """Tests de integración para casos completos del sistema."""

    def test_shouldCalculateCompleteScenarioWithAllFactors(self):
        """Debe calcular escenario completo con todos los factores."""
        attendance_policy = AttendancePolicy(3.0)
        extra_points_policy = ExtraPointsPolicy(True, 2.0)
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        evaluations = [
            Evaluation("Parcial 1", 15.0, 0.25),
            Evaluation("Parcial 2", 16.0, 0.25),
            Evaluation("Proyecto", 17.0, 0.30),
            Evaluation("Final", 14.0, 0.20)
        ]

        final_grade = calculator.calculate_final_grade(evaluations, True)

        # Verificar que el resultado está en el rango válido
        self.assertGreaterEqual(final_grade, 0.0)
        self.assertLessEqual(final_grade, 20.0)

        # Verificar detalles
        details = calculator.get_calculation_details(evaluations, True)
        self.assertEqual(details['extra_points'], 2.0)
        self.assertEqual(details['attendance_penalty'], 0.0)

    def test_shouldCalculateWorstCaseScenario(self):
        """Debe calcular correctamente el peor escenario posible."""
        attendance_policy = AttendancePolicy(5.0)
        extra_points_policy = ExtraPointsPolicy(False, 0.0)
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        evaluations = [
            Evaluation("Test", 5.0, 1.0)
        ]

        final_grade = calculator.calculate_final_grade(evaluations, False)
        self.assertEqual(final_grade, 0.0)  # 5 - 5 = 0 (capped at 0)

    def test_shouldCalculateBestCaseScenario(self):
        """Debe calcular correctamente el mejor escenario posible."""
        attendance_policy = AttendancePolicy(0.0)
        extra_points_policy = ExtraPointsPolicy(True, 5.0)
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        evaluations = [
            Evaluation("Perfect", 20.0, 1.0)
        ]

        final_grade = calculator.calculate_final_grade(evaluations, True)
        self.assertEqual(final_grade, 20.0)  # 20 + 5 = 25, capped at 20


def run_tests():
    """Ejecuta todos los tests y muestra el reporte."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestEvaluation))
    suite.addTests(loader.loadTestsFromTestCase(TestAttendancePolicy))
    suite.addTests(loader.loadTestsFromTestCase(TestExtraPointsPolicy))
    suite.addTests(loader.loadTestsFromTestCase(TestGradeCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestGradeCalculatorIntegration))

    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Reporte de cobertura
    print("\n" + "=" * 70)
    print("REPORTE DE TESTS")
    print("=" * 70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print(f"Tasa de éxito: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
