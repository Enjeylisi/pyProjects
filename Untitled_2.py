class Employee:
    def __init__(self, name: str, position: str, salary: float):
        self.name = name
        self.position = position
        self.salary = salary

    def get_salary_info(self) -> str:
        return f"Заробітна плата {self.name}: {self.salary}"