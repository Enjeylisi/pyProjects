class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    def calculate_total_price(self) -> float:
        return self.price * self.quantity

    def display_info(self):
        print(f"Товар: {self.name} | Ціна: {self.price} | Кількість: {self.quantity} | Загальна вартість: {self.calculate_total_price()}")