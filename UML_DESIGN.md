# Diseño UML - CS-GradeCalculator

## Diagrama de Clases

```
┌─────────────────────────────────┐
│        Evaluation               │
├─────────────────────────────────┤
│ - name: str                     │
│ - grade: float                  │
│ - weight: float                 │
│ + MAX_GRADE: float = 20.0       │
│ + MIN_GRADE: float = 0.0        │
├─────────────────────────────────┤
│ + __init__(name, grade, weight) │
│ + get_weighted_grade(): float   │
└─────────────────────────────────┘


┌─────────────────────────────────┐
│      AttendancePolicy           │
├─────────────────────────────────┤
│ - penalty_points: float         │
│ + DEFAULT_PENALTY: float = 3.0  │
├─────────────────────────────────┤
│ + __init__(penalty_points)      │
│ + calculate_penalty(bool): float│
└─────────────────────────────────┘


┌─────────────────────────────────┐
│     ExtraPointsPolicy           │
├─────────────────────────────────┤
│ - all_years_teachers: bool      │
│ - extra_points: float           │
│ + DEFAULT_EXTRA_POINTS = 2.0    │
├─────────────────────────────────┤
│ + __init__(bool, extra_points)  │
│ + calculate_extra_points():float│
└─────────────────────────────────┘


┌───────────────────────────────────────────┐
│          GradeCalculator                  │
├───────────────────────────────────────────┤
│ - attendance_policy: AttendancePolicy     │
│ - extra_points_policy: ExtraPointsPolicy  │
│ + MAX_EVALUATIONS: int = 10               │
│ + MAX_FINAL_GRADE: float = 20.0           │
│ + MIN_FINAL_GRADE: float = 0.0            │
├───────────────────────────────────────────┤
│ + __init__(attendance, extra_points)      │
│ + calculate_final_grade(List[Evaluation], │
│                         bool): float      │
│ + get_calculation_details(...): dict      │
│ - _calculate_weighted_average(...): float │
│ - _validate_evaluations(...): void        │
└───────────────────────────────────────────┘
           │                │
           │ uses           │ uses
           ▼                ▼
   AttendancePolicy   ExtraPointsPolicy


┌───────────────────────────────────────────┐
│       GradeCalculatorApp                  │
├───────────────────────────────────────────┤
│ - calculator: GradeCalculator             │
├───────────────────────────────────────────┤
│ + run(): void                             │
│ - _get_student_id(): str                  │
│ - _configure_attendance_policy():         │
│     AttendancePolicy                      │
│ - _configure_extra_points_policy():       │
│     ExtraPointsPolicy                     │
│ - _register_evaluations():                │
│     List[Evaluation]                      │
│ - _input_evaluation(): Evaluation         │
│ - _register_attendance(): bool            │
│ - _display_results(str, dict): void       │
└───────────────────────────────────────────┘
           │
           │ uses
           ▼
    GradeCalculator
           │
           │ manages
           ▼
       Evaluation
```
