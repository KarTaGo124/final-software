class ExtraPointsPolicy:
    DEFAULT_EXTRA_POINTS = 2.0

    def __init__(self, allYearsTeachers: bool, extra_points: float = DEFAULT_EXTRA_POINTS):
        if not isinstance(allYearsTeachers, bool):
            raise ValueError("allYearsTeachers debe ser un valor booleano")
        if not isinstance(extra_points, (int, float)):
            raise ValueError("Los puntos extra deben ser un número")
        if extra_points < 0:
            raise ValueError("Los puntos extra no pueden ser negativos")

        self.allYearsTeachers = allYearsTeachers
        self.extra_points = float(extra_points)

    def calculate_extra_points(self) -> float:
        return self.extra_points if self.allYearsTeachers else 0.0
