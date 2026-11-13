
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class Cart:
    def __init__(self):
        self.products = []

    def add_product(self, product, quantity):
        if quantity <= product.quantity and quantity > 0:
            self.products.append((product, quantity))
            product.quantity -= quantity
            print("Товар додано до кошика!")
        else:
            print("Недостатньо товару на складі!")

    def remove_product(self, name):
        for item in self.products:
            if item[0].name == name:
                item[0].quantity += item[1]
                self.products.remove(item)
                print("Товар видалено!")
                return
        print("Товар не знайдено!")

    def total_price(self):
        total = sum(product.price * quantity for product, quantity in self.products)
        return total

    def show_cart(self):
        for product, quantity in self.products:
            print(f"{product.name} - {quantity} шт. - {product.price * quantity} грн")
        print(f"Загальна вартість: {self.total_price()} грн")

product1 = Product("Телефон", 12000, 5)
product2 = Product("Навушники", 1500, 10)

cart = Cart()

cart.add_product(product1, 1)
cart.add_product(product2, 2)

cart.show_cart()
cart.remove_product("Навушники")
cart.show_cart()
