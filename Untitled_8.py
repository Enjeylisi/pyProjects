
class Employee:
    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary

class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        print("Співробітника додано!")

    def remove_employee(self, name):
        for employee in self.employees:
            if employee.name == name:
                self.employees.remove(employee)
                print("Співробітника видалено!")
                return
        print("Співробітника не знайдено!")

    def total_salary(self):
        total = sum(employee.salary for employee in self.employees)
        return total

    def show_employees(self):
        print(f"Відділ: {self.name}")

        for employee in self.employees:
            print(f"Ім'я: {employee.name}")
            print(f"Посада: {employee.position}")
            print(f"Зарплата: {employee.salary} грн")
            print("-" * 30)

        print(f"Загальна зарплата: {self.total_salary()} грн")

department = Department("IT-відділ")

department.add_employee(Employee("Іван", "Програміст", 30000))
department.add_employee(Employee("Петро", "Дизайнер", 25000))
department.add_employee(Employee("Олег", "Тестувальник", 20000))

department.show_employees()

department.remove_employee("Петро")

department.show_employees()
