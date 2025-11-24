class Evaluation:
    MAX_GRADE = 20.0
    MIN_GRADE = 0.0

    def __init__(self, name: str, grade: float, weight: float):
        if not name or not isinstance(name, str):
            raise ValueError("El nombre de la evaluación debe ser una cadena no vacía")
        if not isinstance(grade, (int, float)):
            raise ValueError("La nota debe ser un número")
        if grade < self.MIN_GRADE or grade > self.MAX_GRADE:
            raise ValueError(f"La nota debe estar entre {self.MIN_GRADE} y {self.MAX_GRADE}")
        if not isinstance(weight, (int, float)):
            raise ValueError("El peso debe ser un número")
        if weight < 0 or weight > 1:
            raise ValueError("El peso debe estar entre 0 y 1")

        self.name = name
        self.grade = float(grade)
        self.weight = float(weight)

    def get_weighted_grade(self) -> float:
        return self.grade * self.weight
