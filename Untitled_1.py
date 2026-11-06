class Car:
    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year

    def get_info(self) -> str:
        return f"{self.year} {self.make} {self.model}"