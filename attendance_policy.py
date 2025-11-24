class AttendancePolicy:
    DEFAULT_PENALTY = 3.0

    def __init__(self, penalty_points: float = DEFAULT_PENALTY):
        if not isinstance(penalty_points, (int, float)):
            raise ValueError("Los puntos de penalización deben ser un número")
        if penalty_points < 0:
            raise ValueError("Los puntos de penalización no pueden ser negativos")
        self.penalty_points = float(penalty_points)

    def calculate_penalty(self, hasReachedMinimumClasses: bool) -> float:
        if not isinstance(hasReachedMinimumClasses, bool):
            raise ValueError("hasReachedMinimumClasses debe ser un valor booleano")
        return 0.0 if hasReachedMinimumClasses else self.penalty_points

