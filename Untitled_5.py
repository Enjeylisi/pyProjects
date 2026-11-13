
class Task:
    def __init__(self, name, description, deadline):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.completed = False

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print("Завдання додано!")

    def delete_task(self, name):
        for task in self.tasks:
            if task.name == name:
                self.tasks.remove(task)
                print("Завдання видалено!")
                return
        print("Завдання не знайдено!")

    def complete_task(self, name):
        for task in self.tasks:
            if task.name == name:
                task.completed = True
                print("Завдання виконано!")
                return
        print("Завдання не знайдено!")

    def show_tasks(self):
        for task in self.tasks:
            status = "Виконано" if task.completed else "Не виконано"
            print(f"Назва: {task.name}")
            print(f"Опис: {task.description}")
            print(f"Дедлайн: {task.deadline}")
            print(f"Стан: {status}")
            print("-" * 30)

manager = TaskManager()

manager.add_task(Task("Математика", "Виконати вправи", "15.11.2026"))
manager.add_task(Task("Python", "Написати програму", "17.11.2026"))

manager.complete_task("Математика")
manager.show_tasks()
