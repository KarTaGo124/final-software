from typing import List, Dict, Any
from evaluation import Evaluation
from attendance_policy import AttendancePolicy
from extra_points_policy import ExtraPointsPolicy


class GradeCalculator:
    MAX_EVALUATIONS = 10
    MAX_FINAL_GRADE = 20.0
    MIN_FINAL_GRADE = 0.0

    def __init__(self, attendance_policy: AttendancePolicy, extra_points_policy: ExtraPointsPolicy):
        if not isinstance(attendance_policy, AttendancePolicy):
            raise ValueError("attendance_policy debe ser una instancia de AttendancePolicy")
        if not isinstance(extra_points_policy, ExtraPointsPolicy):
            raise ValueError("extra_points_policy debe ser una instancia de ExtraPointsPolicy")

        self.attendance_policy = attendance_policy
        self.extra_points_policy = extra_points_policy

    def calculate_final_grade(self, examsStudents: List[Evaluation], hasReachedMinimumClasses: bool) -> float:
        self._validate_evaluations(examsStudents)

        if not isinstance(hasReachedMinimumClasses, bool):
            raise ValueError("hasReachedMinimumClasses debe ser un valor booleano")

        weighted_average = self._calculate_weighted_average(examsStudents)
        attendance_penalty = self.attendance_policy.calculate_penalty(hasReachedMinimumClasses)
        extra_points = self.extra_points_policy.calculate_extra_points()

        final_grade = weighted_average - attendance_penalty + extra_points
        final_grade = max(self.MIN_FINAL_GRADE, min(self.MAX_FINAL_GRADE, final_grade))

        return round(final_grade, 2)

    def get_calculation_details(self, examsStudents: List[Evaluation], hasReachedMinimumClasses: bool) -> Dict[str, Any]:
        self._validate_evaluations(examsStudents)

        weighted_average = self._calculate_weighted_average(examsStudents)
        attendance_penalty = self.attendance_policy.calculate_penalty(hasReachedMinimumClasses)
        extra_points = self.extra_points_policy.calculate_extra_points()
        final_grade = self.calculate_final_grade(examsStudents, hasReachedMinimumClasses)

        evaluations_detail = [
            {
                "name": evaluation.name,
                "grade": evaluation.grade,
                "weight": evaluation.weight,
                "weighted_grade": evaluation.get_weighted_grade()
            }
            for evaluation in examsStudents
        ]

        return {
            "weighted_average": round(weighted_average, 2),
            "attendance_penalty": round(attendance_penalty, 2),
            "extra_points": round(extra_points, 2),
            "final_grade": final_grade,
            "hasReachedMinimumClasses": hasReachedMinimumClasses,
            "evaluations_detail": evaluations_detail,
            "total_evaluations": len(examsStudents)
        }

    def _calculate_weighted_average(self, examsStudents: List[Evaluation]) -> float:
        if not examsStudents:
            return 0.0

        total_weighted = sum(evaluation.get_weighted_grade() for evaluation in examsStudents)
        total_weight = sum(evaluation.weight for evaluation in examsStudents)

        if total_weight > 0:
            return total_weighted / total_weight * (total_weight if total_weight <= 1 else 1)

        return 0.0

    def _validate_evaluations(self, examsStudents: List[Evaluation]) -> None:
        if not isinstance(examsStudents, list):
            raise ValueError("examsStudents debe ser una lista")
        if len(examsStudents) > self.MAX_EVALUATIONS:
            raise ValueError(f"El número máximo de evaluaciones es {self.MAX_EVALUATIONS}")
        if len(examsStudents) == 0:
            raise ValueError("Debe haber al menos una evaluación")
        for evaluation in examsStudents:
            if not isinstance(evaluation, Evaluation):
                raise ValueError("Todos los elementos deben ser instancias de Evaluation")
